from elasticsearch import Elasticsearch
import datetime

# Connect to Elasticsearch
es = Elasticsearch([{'host': '15.207.94.29', 'port': '9200'}])
#  IP address of Elastic search and port of the server
# client should have access to the remote system and port number 9200.

# ex_index = 'livelogsnew-2025.03.14'
current_date = datetime.datetime.now()
date = current_date.strftime("-%Y.%m.%d")
live_index = 'livelogsnew' + date

# must query is used to combine multiple filters, match_phrase matches the document and returns the result
# aggregate function is used to aggregate the results, its a built in function.
query = {
    "query": {
        "bool": {
            "must": [
                {
                    "match_phrase": {  # Search condition for 'ngx_api'
                        "hp_guid_client": "c3650698-9dea-4657-83f5-850d22b640ab"
                    }
                }, {
                    "match_phrase": {  # Filter based on the 'hp_guid_client' field
                        "ngx_api": "/py/rpo/get_all_candidates/"
                    }
                }
            ],
      "filter": [
        {
          "range": {
            "hp_handled_requests_count": {
              "gte": 3
            }
          }
        }
      ]
        }
    },
    "aggs": {
        "average_time_taken": {
            "avg": {
                "field": "ngx_inner_time_taken"  # Aggregation for the average of 'ngx_total_time_taken'
            }
        },
        "min_time_taken": {
            "min": {
                "field": "ngx_inner_time_taken"  # Aggregation for the minimum value of 'ngx_total_time_taken'
            }
        },
        "max_time_taken": {
            "max": {
                "field": "ngx_inner_time_taken"  # Aggregation for the maximum value of 'ngx_total_time_taken'
            }
        }
    },
    "size": 1  # You can adjust the number of documents to return
}

# Perform the search with aggregation
response = es.search(index=live_index, body=query)

# Access the search results (hits)
hits = response['hits']['hits']

# Access the aggregation result
average_time_taken = response['aggregations']['average_time_taken']['value']
min_time_taken = response['aggregations']['min_time_taken']['value']
max_time_taken = response['aggregations']['max_time_taken']['value']

# Print the aggregation results
print(f"Average ngx_total_time_taken: {average_time_taken}")
print(f"Min ngx_total_time_taken: {min_time_taken}")
print(f"Max ngx_total_time_taken: {max_time_taken}")

# Print the top 10 matching documents
# print("\nTop 10 matching documents:")
# for hit in hits:
#     ngx_total_time_taken = hit['_source'].get('ngx_total_time_taken')
#     print(f"Document ID: {hit['_id']}, ngx_total_time_taken: {ngx_total_time_taken}")
