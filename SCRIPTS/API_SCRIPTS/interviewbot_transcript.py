import os
import sys
import time
import logging
import pandas as pd
import concurrent.futures
from pathlib import Path
from sentence_transformers import SentenceTransformer, util


# Import framework dependencies
from SCRIPTS.COMMON.write_excel_new import write_excel_object
from SCRIPTS.CRPO_COMMON.crpo_common import crpo_common_obj
from SCRIPTS.CRPO_COMMON.credentials import cred_crpo_admin_at
from SCRIPTS.COMMON.io_path import output_common_dir, input_common_dir


# Configure basic logging for the console and a file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("interviewbot_transcript.log"), logging.StreamHandler()])




# Define Output Path
output_path_interviewbot_transcript = os.path.join(output_common_dir, "InterviewBot")
Path(output_path_interviewbot_transcript).mkdir(parents=True, exist_ok=True)


class InterviewBotTranscript:
    def __init__(self):
        self.max_wait_time_seconds = 3600  # 60 minutes
        self.poll_interval_seconds = 30
        self.similarity_threshold = 0.60  # Minimum cosine similarity for text to pass
        logging.info("Loading sentence-transformers model (all-MiniLM-L6-v2)...")
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        logging.info("Semantic model loaded successfully.")

    def trigger_feedback(self, token, interview_id):
        """
        Triggers the generate_feedback API and returns a boolean indicating success.
        """
        try:
            logging.info(f"[{interview_id}] Calling generate_feedback API...")
            response = crpo_common_obj.generate_feedback(token, interview_id)
            if response.get("status") == "OK":
                return True
            else:
                logging.error(f"[{interview_id}] generate_feedback failed: {response}")
                return False
        except Exception as e:
            logging.error(f"[{interview_id}] Exception in trigger_feedback: {e}")
            return False

    def get_data_with_retry(self, token, interview_id):
        """
        Polls the get_interview_by_id API until the DetailedFeedback is completely generated.
        Returns the full JSON dictionary or None if it times out.
        """
        start_time = time.time()
        
        while (time.time() - start_time) < self.max_wait_time_seconds:
            try:
                response = crpo_common_obj.get_interview_by_id(token, interview_id)
                if response.get("status") == "OK":
                    details = response.get("InterviewDetails", {})
                    feedback = details.get("DetailedFeedback")
                    
                    if feedback and isinstance(feedback, list) and len(feedback) > 0:
                        logging.info(f"[{interview_id}] Full feedback generated in {int(time.time() - start_time)}s.")
                        return response
                        
                logging.info(f"[{interview_id}] Polling... waiting for DetailedFeedback.")
                time.sleep(self.poll_interval_seconds)
                
            except Exception as e:
                logging.error(f"[{interview_id}] Error in get_data_with_retry loop: {e}")
                time.sleep(self.poll_interval_seconds)
                
        logging.error(f"[{interview_id}] Timed out waiting for data.")
        return None

    def extract_scores(self, data, parent_key=''):
        """
        Recursively extracts 'Score' keys and their values. Returns a dict.
        """
        items = {}
        try:
            if isinstance(data, dict):
                for k, v in data.items():
                    new_key = f"{parent_key}_{k}" if parent_key else k
                    if "Score" in k or "score" in k:
                        if not isinstance(v, (dict, list)):
                             items[new_key] = v
                    if isinstance(v, (dict, list)):
                        items.update(self.extract_scores(v, new_key))
                        
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    segment = str(i)
                    if isinstance(item, dict) and "QuestionCategory" in item:
                        category_name = str(item["QuestionCategory"]).replace(" ", "_").replace(":", "")
                        segment = f"{i}_{category_name}"
                    new_key = f"{parent_key}_{segment}" if parent_key else segment
                    items.update(self.extract_scores(item, new_key))
                    
        except Exception as e:
            logging.error(f"Error in extract_scores recursively: {e}")
            
        return items

    def _find_best_matching_key(self, expected_key, actual_keys):
        """
        Checks if the expected key exists in the actual keys extracted from the API.
        Returns the exact key if found, otherwise 'Not Found'.
        """
        if expected_key in actual_keys:
            return expected_key
        return "Not Found"

    def _is_within_tolerance(self, expected_val, actual_val, tolerance=0.30):
        """
        Checks if actual_val is within +-tolerance (30%) of expected_val.
        Handles float/int type differences (e.g., 4.0 vs 4).
        Returns (is_numeric, is_pass).
        """
        try:
            exp_num = float(expected_val)
            act_num = float(actual_val)
        except (ValueError, TypeError):
            return False, False

        # Both are numeric — check if they are equal or within tolerance
        if exp_num == act_num:
            return True, True

        if exp_num == 0:
            # For zero expected, use a small absolute threshold
            return True, abs(act_num) <= 0.5

        diff_pct = abs(act_num - exp_num) / abs(exp_num)
        return True, diff_pct <= tolerance

    def _check_semantic_similarity(self, text1, text2):
        """
        Computes cosine similarity between two text strings using sentence embeddings.
        Returns the similarity score (0.0 to 1.0).
        """
        try:
            embeddings = self.semantic_model.encode([str(text1), str(text2)], convert_to_tensor=True)
            similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
            return round(similarity, 4)
        except Exception as e:
            logging.error(f"Error computing semantic similarity: {e}")
            return 0.0

    def validate_scores(self, interview_id, expected_scores_dict, actual_json_data):
        """
        Extracts keys from the final API JSON and compares them to the expected dictionary.
        - Numeric values: +-30% tolerance with float/int handling.
        - Text values: Cosine similarity >= 0.60 using sentence-transformers.
        Returns a list of validation result dictionaries.
        """
        results = []
        try:
            actual_scores = self.extract_scores(actual_json_data)
            actual_keys = list(actual_scores.keys())
            
            for expected_key, expected_val in expected_scores_dict.items():
                actual_val = actual_scores.get(expected_key)
                matched_api_key = self._find_best_matching_key(expected_key, actual_keys)
                similarity_score = None  # Only populated for text comparisons
                
                if actual_val is None:
                    status = "N/A"
                else:
                    is_numeric, is_pass = self._is_within_tolerance(expected_val, actual_val)
                    if is_numeric:
                        status = "Pass" if is_pass else "Fail"
                    else:
                        # Text comparison: use semantic similarity
                        similarity_score = self._check_semantic_similarity(expected_val, actual_val)
                        status = "Pass" if similarity_score >= self.similarity_threshold else "Fail"
                        logging.info(f"[{interview_id}] Text similarity for '{expected_key}': {similarity_score} -> {status}")
                    
                results.append({
                    "Interview ID": interview_id,
                    "JSON Key": expected_key,
                    "Matched API Key": matched_api_key,
                    "Expected Value": expected_val,
                    "Actual Value": actual_val,
                    "Similarity": similarity_score,
                    "Status": status
                })
        except Exception as e:
            logging.error(f"[{interview_id}] Error during validate_scores: {e}")
            
        return results

    def process_single_interview(self, interview_id, login_token, expected_scores_dict):
        """
        Orchestrates the entire flow for a single interview ID. Designed for parallel generic use.
        Returns the list of final result dictionaries.
        """
        try:
            logging.info(f"[{interview_id}] Starting automation flow.")
            
            # 1. Trigger feedback
            if not self.trigger_feedback(login_token, interview_id):
                 return [{"Interview ID": interview_id, "Status": "Fail", "Error": "generate_feedback failed"}]
            
            # 1.5 Wait 300 seconds for feedback to start generating
            logging.info(f"[{interview_id}] Waiting 300 seconds before polling for data...")
            time.sleep(300)
                 
            # 2. Wait for data
            final_json = self.get_data_with_retry(login_token, interview_id)
            if not final_json:
                 return [{"Interview ID": interview_id, "Status": "Fail", "Error": "Timeout waiting for feedback"}]
                 
            # 3. Validate
            return self.validate_scores(interview_id, expected_scores_dict, final_json)
            
        except Exception as e:
            logging.exception(f"[{interview_id}] Unexpected error in process_single_interview: {e}")
            return [{"Interview ID": interview_id, "Status": "Fail", "Error": str(e)}]


def main():
    try:
        # 1. Take Login Token
        login_token = crpo_common_obj.login_to_crpo(
            cred_crpo_admin_at.get('user'),
            cred_crpo_admin_at.get('password'),
            cred_crpo_admin_at.get('tenant')
        )
        if not login_token:
            logging.error("Failed to fetch login token. Exiting.")
            sys.exit(1)

        # 2. Fetch Interview IDs
        input_file = os.path.join(input_common_dir, "InterviewBot", "bot_interview_ids_amsin.txt")
        if not os.path.exists(input_file):
            logging.error(f"Input ids file not found: {input_file}")
            sys.exit(1)
            
        with open(input_file, 'r') as f:
            interview_ids = [line.strip() for line in f if line.strip()]
            
        # 3. Load Expected Scores Reference
        expected_excel_path = os.path.join(input_common_dir, "InterviewBot", "extracted_json_scores.xlsx")
        if not os.path.exists(expected_excel_path):
             logging.error(f"Expected excel file missing: {expected_excel_path}")
             sys.exit(1)
             
        df_expected = pd.read_excel(expected_excel_path)
        expected_scores_dict = dict(zip(df_expected['Key'], df_expected['Value']))
        
        # Output Excel Setup
        bot = InterviewBotTranscript()
        output_file = os.path.join(output_path_interviewbot_transcript, "InterviewBot_Parallel_Results_")
        write_excel_object.save_result(output_file)
        
        headers = ["Interview ID", "JSON Key", "Matched API Key", "Expected Value", "Actual Value", "Similarity", "Status"]
        write_excel_object.write_headers_for_scripts(1, 0, headers, write_excel_object.black_color_bold)
        write_excel_object.ws.write(0, 0, "InterviewBot Parallel Execution", write_excel_object.black_color_bold)

        # 4. Parallel Subprocess Execution
        all_results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(interview_ids), 10)) as executor:
            future_to_id = {
                executor.submit(bot.process_single_interview, iid, login_token, expected_scores_dict): iid 
                for iid in interview_ids
            }
            
            for future in concurrent.futures.as_completed(future_to_id):
                iid = future_to_id[future]
                try:
                    data = future.result()
                    all_results.extend(data)
                except Exception as exc:
                    logging.exception(f"[{iid}] Thread raised exception: {exc}")

        # 5. Write to Excel
        row_idx = 2
        for result in all_results:
            col_idx = 0
            write_excel_object.ws.write(row_idx, col_idx, result.get("Interview ID"), write_excel_object.black_color)
            col_idx += 1
            
            if "Error" in result:
                 write_excel_object.ws.write(row_idx, col_idx, result.get("Error"), write_excel_object.red_color)
                 write_excel_object.ws.write(row_idx, col_idx+5, "Fail", write_excel_object.red_color)
                 write_excel_object.overall_status = "Fail"
                 write_excel_object.overall_status_color = write_excel_object.red_color
            else:
                 write_excel_object.ws.write(row_idx, col_idx, result.get("JSON Key"), write_excel_object.black_color)
                 col_idx += 1
                 write_excel_object.ws.write(row_idx, col_idx, result.get("Matched API Key"), write_excel_object.black_color)
                 
                 expected_val = str(result.get("Expected Value"))
                 actual_val = str(result.get("Actual Value")) if result.get("Actual Value") is not None else "N/A"
                 
                 write_excel_object.compare_results_and_write_vertically(expected_val, actual_val, row_idx, col_idx+1)
                 
                 # Write similarity score if available
                 similarity = result.get("Similarity")
                 sim_col = col_idx + 3
                 if similarity is not None:
                     write_excel_object.ws.write(row_idx, sim_col, str(similarity), write_excel_object.black_color)
                 else:
                     write_excel_object.ws.write(row_idx, sim_col, "-", write_excel_object.black_color)
                 
                 status = result.get("Status")
                 status_col = col_idx+4
                 
                 if status == "Pass":
                     write_excel_object.ws.write(row_idx, status_col, status, write_excel_object.green_color)
                 elif status == "N/A":
                     write_excel_object.ws.write(row_idx, status_col, status, write_excel_object.orange_color)
                 else:
                     write_excel_object.ws.write(row_idx, status_col, status, write_excel_object.red_color)
                     write_excel_object.overall_status = "Fail"
                     write_excel_object.overall_status_color = write_excel_object.red_color
            row_idx += 1
            
        write_excel_object.write_overall_status(len(all_results))
        logging.info("Execution Finished. Output excel report written successfully.")

    except Exception as e:
        logging.exception(f"Critical error in main: {e}")


if __name__ == "__main__":
    main()