a = {'time_taken_by_sql_query_in_ms_2': 2.21, 'time_taken_by_sql_query_in_ms_3': 0.74,
     'time_taken_by_sql_query_in_ms_4': 0.67, 'time_taken_by_sql_query_in_ms_5': 0.61,
     'time_taken_by_sql_query_in_ms_6': 9.08, 'time_taken_by_sql_query_in_ms_7': 5.99,
     'time_taken_by_sql_query_in_ms_8': 1.05, 'time_taken_by_sql_query_in_ms_9': 2.17,
     'time_taken_by_sql_query_in_ms_10': 6.37, 'time_taken_by_sql_query_in_ms_11': 0.7,
     'time_taken_by_sql_query_in_ms_12': 0.64, 'time_taken_by_sql_query_in_ms_13': 0.52,
     'time_taken_by_sql_query_in_ms_14': 1.22}
b = 0
for key, value in a.items():
    b = b + value
    print(b)
