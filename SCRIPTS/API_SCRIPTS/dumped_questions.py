# from SCRIPTS.API_SCRIPTS.test import parent_tenant_qn_details
from SCRIPTS.COMMON.write_excel_new import *
from SCRIPTS.COMMON.read_excel import *
from SCRIPTS.CRPO_COMMON.crpo_common import *
from SCRIPTS.CRPO_COMMON.credentials import *
from SCRIPTS.COMMON.io_path import *
from SCRIPTS.COMMON.parallel_execution import *
import os
import re
from urllib.parse import urlparse, parse_qs


class DumpedQuestions:

    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.row_size = 2
        write_excel_object.save_result(output_path_dumped_questions)
        self.write_headers()

    @staticmethod
    def write_headers():
        # Writing headers in the Excel file
        headers = ["Dumped Questions"]
        write_excel_object.write_headers_for_scripts(0, 0, headers, write_excel_object.black_color_bold)
        headers1 = ["Question Type", "Status", "Target Tenant", "Target Qid", "Mismatched Keys",
                    "Keys Not Available in Dumped Tenant",
                    "Extra Keys in Dumped Question", 'exp exported question id','act exported question id',
                    'exp foreign tenant', 'act foreign tenant','exp target tenant','actual target tenant',
                    'exp foreign qid', 'actual foreign qid','Parent Dump']
        write_excel_object.write_headers_for_scripts(1, 0, headers1, write_excel_object.black_color_bold)

    def normalize_url_for_comparison(self, url):
        """Normalize URL for partial comparison - extracts key parts that should match"""
        try:
            parsed = urlparse(url)
            # Extract path components
            path_parts = parsed.path.strip('/').split('/')
            # print(path_parts)
            # Extract filename (last part of path)
            filename = path_parts[-1] if path_parts else ''
            bucket = path_parts[0] if len(path_parts) > 0 else ''
            tenant = path_parts[1] if len(path_parts) > 1 else ''
            # For S3 URLs, we can compare:
            # 1. Filename (most important - the actual resource)
            # 2. Domain pattern (s3 vs s3-ap format) - normalized
            # 3. Query parameter keys (not values, as they're time-based)

            # Store actual domain (without normalization)
            domain_actual = parsed.netloc
            
            # Normalize domain for comparison (s3-ap-* -> s3.*)
            # This handles both s3-ap-southeast-1.amazonaws.com and s3.ap-southeast-1.amazonaws.com
            domain = domain_actual
            # Normalize s3-ap-* format to s3.* for comparison
            if domain.startswith('s3-ap-'):
                # s3-ap-southeast-1 -> s3.ap-southeast-1
                domain = domain.replace('s3-ap-', 's3.', 1)
            elif domain.startswith('s3.'):
                # Already in s3.* format
                pass

            # Extract query param keys (ignore values)
            query_keys = set(parse_qs(parsed.query).keys()) if parsed.query else set()

            return {
                'filename': filename,
                'domain': domain,  # Normalized for comparison
                'domain_actual': domain_actual,  # Actual domain without normalization
                'path_parts_count': len(path_parts),
                'query_keys': query_keys,
                'scheme': parsed.scheme,
                'tenant': tenant,
                'bucket': bucket

            }
        except Exception as e:
            # If URL parsing fails, return original URL
            return {'raw': url}

    def compare_urls_partially(self, url1, url2):
        """Compare URLs partially - ignoring time-based query params and tenant-specific paths"""
        if url1 is None or url2 is None:
            return url1 == url2

        if not isinstance(url1, str) or not isinstance(url2, str):
            return url1 == url2

        norm1 = self.normalize_url_for_comparison(url1)
        norm2 = self.normalize_url_for_comparison(url2)

        # If normalization failed, do exact comparison
        if 'raw' in norm1 or 'raw' in norm2:
            return url1 == url2

        # Compare key parts that should match:
        # 1. Filename (the actual resource identifier) - must match
        if norm1['filename'] != norm2['filename']:
            print("File name not mathced")
            return False

        # # 2. Domain pattern should match (normalized)
        # if norm1['domain'] != norm2['domain']:
        #     print("Domain name not mathced")
        #     return False

        # 3. Scheme should match
        if norm1['scheme'] != norm2['scheme']:
            print("Scheme name not mathced")
            return False

        # 4. Query parameter keys should match (values can differ - they're time-based)
        if norm1['query_keys'] != norm2['query_keys']:
            print("query keys name not mathced")
            return False

        # 5. Bucket should not match
        # if norm1['bucket'] == norm2['bucket']:
        #     print(norm1['bucket'])
        #     print(norm2['bucket'])
        #     print("bucket name is  mathced")
        #     return True

        # Note: We intentionally allow tenant to differ (AT vs hirepro are different tenants
        # but may refer to the same resource filename)

        # Path structure should be similar (same number of parts)
        # Allow small differences for tenant-specific paths
        if abs(norm1['path_parts_count'] - norm2['path_parts_count']) > 1:
            return False

        return True

    def extract_urls(self, text):
        """Extract URLs from a string and return the text with URLs removed"""
        # Pattern to match URLs (http:// or https://)
        url_pattern = r'https?://[^\s<>"\'{}\[\]()]+'
        # url_pattern ='muthu?://'
        urls = re.findall(url_pattern, text)
        text_without_urls = re.sub(url_pattern, '', text)
        return text_without_urls, urls

    def compare_strings_without_urls(self, str1, str2):
        """Compare two strings with partial URL comparison"""
        if not isinstance(str1, str) and not isinstance(str2, str):
            return str1 == str2

        text1, urls1 = self.extract_urls(str1 if isinstance(str1, str) else "")
        text2, urls2 = self.extract_urls(str2 if isinstance(str2, str) else "")

        # Check if both have URLs
        has_urls1 = len(urls1) > 0
        has_urls2 = len(urls2) > 0

        # If one has URL and other doesn't - mismatch
        if has_urls1 != has_urls2:
            return False

        # Compare text without URLs
        if text1.strip() != text2.strip():
            return False

        # Compare URLs partially if both have URLs
        if has_urls1 and has_urls2:
            if len(urls1) != len(urls2):
                return False
            for url1, url2 in zip(urls1, urls2):
                if not self.compare_urls_partially(url1, url2):
                    return False

        return True

    def compare_structs(self, d1, d2, path=""):
        mismatches = []
        missing_in_dict1 = []
        missing_in_dict2 = []

        if isinstance(d1, dict) and isinstance(d2, dict):
            all_keys = set(d1.keys()).union(d2.keys())
            keys_to_remove = {'createdOn', 'questionstatisticsId', 'isExported', 'createdBy', 'createdByName',
                              'authorText',
                              'authorId', 'guid', 'id', 'statistics', 'foreignQuestionDetails', 'latestHistoryJson',
                              'modifiedBy', 'modifiedOn', 'modifiedByName', 'testInfos', 'questionPaperInfos',
                              'questionId'}

            all_keys.difference_update(keys_to_remove)

            # print(all_keys)
            for key in all_keys:
                new_path = f"{path}.{key}" if path else key
                if key not in d1:
                    missing_in_dict1.append(f"{new_path}: Missing in dumped tenant")
                elif key not in d2:
                    missing_in_dict2.append(f"{new_path}: extra kv in dumped tenant")
                else:
                    sub_mismatches, sub_missing_dict1, sub_missing_dict2 = self.compare_structs(d1[key], d2[key],
                                                                                                new_path)
                    mismatches.extend(sub_mismatches)
                    missing_in_dict1.extend(sub_missing_dict1)
                    missing_in_dict2.extend(sub_missing_dict2)

        elif isinstance(d1, list) and isinstance(d2, list):
            max_len = max(len(d1), len(d2))
            for i in range(max_len):
                new_path = f"{path}[{i}]"
                if i >= len(d1):
                    missing_in_dict1.append(f"{new_path}: Missing in target tenant")
                elif i >= len(d2):
                    missing_in_dict2.append(f"{new_path}: extra kv in target tenant")
                else:
                    sub_mismatches, sub_missing_dict1, sub_missing_dict2 = self.compare_structs(d1[i], d2[i], new_path)
                    mismatches.extend(sub_mismatches)
                    missing_in_dict1.extend(sub_missing_dict1)
                    missing_in_dict2.extend(sub_missing_dict2)

        else:
            # Special handling for URL fields - compare partially (ignoring query params, tenant paths)
            if path.endswith('.url'):
                if d1 is None and d2 is None:
                    pass  # Both None, considered equal
                elif d1 is None or d2 is None:
                    mismatches.append(f"{path}: {repr(d1)} != {repr(d2)}")
                elif isinstance(d1, str) and isinstance(d2, str):
                    # Compare URLs partially
                    if not self.compare_urls_partially(d1, d2):
                        mismatches.append(f"{path}: {repr(d1)} != {repr(d2)}")
            elif isinstance(d1, str) or isinstance(d2, str):
                # For strings, compare with partial URL matching
                if not self.compare_strings_without_urls(d1, d2):
                    mismatches.append(f"{path}: {repr(d1)} != {repr(d2)}")
                    # # print("*"*120)
                    # print(path)
                    # print(d1)
                    # print(d2)
            elif (d1.strip() if isinstance(d1, str) else d1) != (d2.strip() if isinstance(d2, str) else d2):
                # this could have been simple elif d1 != d2: but in some cases need to stripe leading and trailing spaces
                mismatches.append(f"{path}: {repr(d1)} != {repr(d2)}")
                # print("*"*120)
                # print(path)
                # print(d1)
                # print(d2)

        return mismatches, missing_in_dict1, missing_in_dict2

    def process_question(self, tokens, excel_values):

        write_excel_object.current_status = "Pass"
        write_excel_object.current_status_color = write_excel_object.green_color
        dumped_tenant_login_token = tokens[0]
        parent_tenant_login_token = tokens[1]
        # print(excel_values)
        parent_question_id = int(excel_values.get('parentQuestionID'))
        parent_tenant_qn_details = crpo_common_obj.get_question_for_id(parent_tenant_login_token, parent_question_id)
        get_parent_dump_resp = crpo_common_obj.get_question_dump(parent_tenant_login_token, parent_question_id,
                                                                 excel_values.get('questionType'))
        get_parent_dump = get_parent_dump_resp.get('data')
        create_question_using_dump_resp = crpo_common_obj.create_question_using_dump(dumped_tenant_login_token,
                                                                                     get_parent_dump)
        # print(create_question_using_dump_resp)
        context_id = create_question_using_dump_resp['data']['ContextId']
        job_status = crpo_common_obj.job_status_v2(dumped_tenant_login_token, context_id)

        result_raw = job_status.get('data', {}).get('Result', '{}')

        try:
            result = json.loads(result_raw)
        except json.JSONDecodeError:
            print("Invalid JSON in Result")
            result = {}
        if "createdQuestions" in result:
            question_info = result["createdQuestions"][0]
            question_id = question_info.get("destinationQuestionId")
            is_created = question_info.get("isCreated", False)
            error_message = str(question_info.get("errorMessage"))
            if is_created and question_id:
                print(f"✅ Question created successfully. Destination ID: {question_id}")
                dumped_tenant_qn_details = crpo_common_obj.get_question_for_id(dumped_tenant_login_token,
                                                                               question_id)
                foreign_infos = dumped_tenant_qn_details.get('data', {}).get('foreignQuestionDetails', {})
                print(foreign_infos)
                foreign_qid = foreign_infos.get('foreignQuestionId')
                foreign_tenant = foreign_infos.get('foreignTenantAlias')

                parent_tenant_exported_infos = crpo_common_obj.get_exported_question_data(parent_tenant_login_token,
                                                                               parent_question_id)
                print(parent_tenant_exported_infos)
                exported_details1 = parent_tenant_exported_infos.get('data', {}).get('exportedData', {})[0]

                exported_target_qid = exported_details1.get('targetQuestionId')
                exported_tenant_alias = exported_details1.get('targetTenantAlias')
                mismatched_items, missing_in_dict1, missing_in_dict2 = self.compare_structs(dumped_tenant_qn_details,
                                                                                            parent_tenant_qn_details)
                write_excel_object.compare_results_and_write_vertically(question_id, None,
                                                                        self.row_size,
                                                                        3)
                write_excel_object.compare_results_and_write_vertically(None, str(mismatched_items), self.row_size, 4)
                write_excel_object.compare_results_and_write_vertically(None, str(missing_in_dict1),
                                                                        self.row_size, 5)
                write_excel_object.compare_results_and_write_vertically(None, str(missing_in_dict2),
                                                                        self.row_size, 6)

                write_excel_object.compare_results_and_write_vertically(exported_target_qid,question_id,
                                                                        self.row_size, 7)

                write_excel_object.compare_results_and_write_vertically(excel_values.get('parentTenant').lower(),
                                                                        foreign_tenant.lower(), self.row_size, 9)
                write_excel_object.compare_results_and_write_vertically(excel_values.get('targetTenant').lower(),
                                                                        exported_tenant_alias.lower(), self.row_size, 11)
                write_excel_object.compare_results_and_write_vertically(parent_question_id, foreign_qid,
                                                                        self.row_size, 13)



            else:
                print(f"⚠️ Question not created: {error_message}")
                write_excel_object.compare_results_and_write_vertically(error_message, None,
                                                                        self.row_size,
                                                                        3)
                write_excel_object.compare_results_and_write_vertically(None, error_message,
                                                                        self.row_size, 4)
                write_excel_object.compare_results_and_write_vertically(None, error_message,
                                                                        self.row_size, 5)
                write_excel_object.compare_results_and_write_vertically(None, error_message,
                                                                        self.row_size, 6)
                write_excel_object.compare_results_and_write_vertically(error_message, error_message,
                                                                        self.row_size, 7)
                write_excel_object.compare_results_and_write_vertically(error_message,
                                                                        error_message, self.row_size, 9)
                write_excel_object.compare_results_and_write_vertically(error_message,
                                                                        error_message, self.row_size, 11)
                write_excel_object.compare_results_and_write_vertically(error_message, error_message,
                                                                        self.row_size, 13)
                # print("⚠️ Unknown question creation status")
        else:
            error_message = str(result.get('error'))
            print(f"⚠️ Question not created: {error_message}")
            write_excel_object.compare_results_and_write_vertically(error_message, None,
                                                                    self.row_size,
                                                                    3)
            write_excel_object.compare_results_and_write_vertically(None, error_message,
                                                                    self.row_size, 4)
            write_excel_object.compare_results_and_write_vertically(None, error_message,
                                                                    self.row_size, 5)
            write_excel_object.compare_results_and_write_vertically(None, error_message,
                                                                    self.row_size, 6)
            write_excel_object.compare_results_and_write_vertically(error_message, error_message,
                                                                    self.row_size, 7)
            write_excel_object.compare_results_and_write_vertically(error_message,
                                                                    error_message, self.row_size, 9)
            write_excel_object.compare_results_and_write_vertically(error_message,
                                                                    error_message, self.row_size, 11)
            write_excel_object.compare_results_and_write_vertically(error_message, error_message,
                                                                    self.row_size, 13)
            print("⚠️ Unknown question creation status")
        write_excel_object.compare_results_and_write_vertically(excel_values.get('questionType'), None, self.row_size,
                                                                0)
        write_excel_object.compare_results_and_write_vertically(write_excel_object.current_status, None,
                                                                self.row_size,
                                                                1)
        write_excel_object.compare_results_and_write_vertically(excel_values.get('targetTenant'), None,
                                                                self.row_size,
                                                                2)
        write_excel_object.compare_results_and_write_vertically(str(get_parent_dump), None,
                                                                self.row_size,
                                                                15)

        self.row_size += 1


dump_qn_obj = DumpedQuestions()

# Logging in to CRPO
dumped_tenant_login_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_at.get('user'),
                                                          cred_crpo_admin_at.get('password'),
                                                          cred_crpo_admin_at.get('tenant'))

parent_tenant_login_token = crpo_common_obj.login_to_crpo(cred_crpo_admin_hirepro.get('user'),
                                                          cred_crpo_admin_hirepro.get('password'),
                                                          cred_crpo_admin_hirepro.get('tenant'))

# Reading data from Excel file
excel_read_obj.excel_read(inpiut_dump_questions, 0)
excel_data = excel_read_obj.details

# Process questions in parallel using thread context
tokens = [dumped_tenant_login_token, parent_tenant_login_token]
thread_context(dump_qn_obj.process_question, tokens, excel_data)
write_excel_object.write_overall_status(testcases_count=len(excel_data))


