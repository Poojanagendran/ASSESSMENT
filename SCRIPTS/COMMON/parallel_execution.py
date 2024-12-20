from concurrent.futures import ThreadPoolExecutor, as_completed


def thread_context(invoking_object_and_function, token, excel_data):
    # if login token is required use below
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(invoking_object_and_function, token, data): data for data in excel_data}
        for future in as_completed(futures):
            data = futures[future]
            try:
                future.result()  # This will raise an exception if the function call raised one
            except Exception as e:
                print(f"Error processing {data.get('fileName')}: {e}")


def thread_context_for_ui(invoking_object_and_function, excel_data):
    # if login token is required use below
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(invoking_object_and_function, data): data for data in excel_data}
        for future in as_completed(futures):
            data = futures[future]
            try:
                future.result()  # This will raise an exception if the function call raised one
            except Exception as e:
                print(f"Error processing {data.get('fileName')}: {e}")


def thread_context_for_ssrf_check(invoking_object_function, crpo_headers, candidate_headers, assessment_headers,
                                  source_headers, excel_data):
    # if login token is not required use below
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(invoking_object_function, crpo_headers, candidate_headers, assessment_headers,
                                   source_headers, data): data for data in excel_data}
        for future in as_completed(futures):
            data = futures[future]
            # print("This is data")
            # print(data)
            # future.result()
            try:
                future.result()  # This will raise an exception if the function call raised one
            except Exception as e:
                print(f"Error processing {data.get('fileName')}: {e}")


def thread_context_for_chaining(invoking_object_and_function, excel_data):
    # if login token is required use below
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(invoking_object_and_function, data): data for data in excel_data}
        for future in as_completed(futures):
            data = futures[future]
            future.result()
            # try:
            #     future.result()  # This will raise an exception if the function call raised one
            # except Exception as e:
            #     print(f"Error processing {data.get('fileName')}: {e}")
# Writing overall status in the Excel file
# write_excel_object.write_overall_status(testcases_count=len(excel_data))
