import json

def extract_scores(data, parent_key=''):
    """
    Recursively extracts keys containing 'Score' (case-insensitive) and their values.
    Returns a list of tuples: (full_key, value)
    """
    items = []
    
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}_{k}" if parent_key else k
            
            # Check if current key contains "Score" (case-insensitive)
            if "Score" in k or "score" in k:
                 # If the value is not a dict/list, it's a leaf score
                if not isinstance(v, (dict, list)):
                     items.append((new_key, v))
            
            # Recurse
            if isinstance(v, (dict, list)):
                items.extend(extract_scores(v, new_key))
                
    elif isinstance(data, list):
        for i, item in enumerate(data):
            # Check if item has "QuestionCategory" to use as part of the key
            segment = str(i)
            if isinstance(item, dict) and "QuestionCategory" in item:
                # Sanitize category name (replace spaces with _, remove special chars if needed)
                # For simplicity, just replace spaces
                category_name = str(item["QuestionCategory"]).replace(" ", "_").replace(":", "")
                segment = f"{i}_{category_name}"
            
            new_key = f"{parent_key}_{segment}" if parent_key else segment
            items.extend(extract_scores(item, new_key))
            
    return items

def main():
    try:
        with open('sample_data.json', 'r') as f:
            data = json.load(f)
            
        score_items = extract_scores(data)
        
        # 1. List of all score keys
        # We want the leaf key name for the first list? 
        # "list all the score keys" -> implies the actual key name in the JSON like "coherence_score"
        # "then list of keys and values" -> implies the full path "InterviewDetails_DetailedFeedback_0_..."
        
        # Actually user said: "list all the score keys"
        # Use full path keys for clarity since multiple keys might have same name (e.g. overall_score)
        
        print("--- 1. List of all Score Keys (Full Path) ---")
        keys_only = [item[0] for item in score_items]
        for k in keys_only:
            print(k)
        print("\n")

        print("--- 2. List of Keys and Values ---")
        for k, v in score_items:
            print(f"{k}: {v}")
        print("\n")

        print("--- 3. List of Values Only ---")
        values_only = [item[1] for item in score_items]
        print(values_only)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
