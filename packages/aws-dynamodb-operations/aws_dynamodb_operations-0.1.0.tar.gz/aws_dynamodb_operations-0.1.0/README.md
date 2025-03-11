# AWS DynamoDB Operations

A Python package for interacting with AWS DynamoDB.

## Installation

pip install aws-dynamodb-operations


## Usage

```python
from aws_dynamodb_operations import DynamoDBOperations

dynamo = DynamoDBOperations()
dynamo.insert_data_via_dict("my_table", {"id": "123", "name": "Test"}, "id")
dynamo.retrieve_data(table_name="my_table", 
                     partition_key="id", 
                     partition_key_value="123",
                     limit=10)

