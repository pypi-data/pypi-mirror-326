import boto3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("dynamodb_operations.log"),  # Logs to file
        logging.StreamHandler()  # Logs to console
    ]
)

class DynamoDBOperations:
    """
    A class to interact with AWS DynamoDB, providing methods to insert and retrieve data.

    Attributes:
    -----------
    dynamodb : boto3.resource
        A DynamoDB resource for interacting with the AWS DynamoDB service.
    """

    def __init__(self):
        """Initialize a DynamoDB resource using boto3."""
        try:
            self.dynamodb = boto3.resource('dynamodb')
            logging.info("DynamoDB resource initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing DynamoDB resource: {str(e)}")
            raise

    def insert_data_via_dict(self, table_name: str, data_store: dict, partition_key_name: str) -> dict:
        """
        Inserts a dictionary of data into the specified DynamoDB table.

        Parameters:
        -----------
        table_name : str
            The name of the DynamoDB table where the data will be inserted.
        data_store : dict
            The data to be inserted, formatted as a dictionary.
        partition_key_name : str
            The name of the partition key used to identify the record.

        Returns:
        --------
        dict
            A response indicating the status of the insertion operation.
        """
        try:
            table = self.dynamodb.Table(table_name)
        except Exception as e:
            logging.error(f"Error accessing DynamoDB table '{table_name}': {str(e)}")
            return {
                'statusCode': 500,
                'body': f"Error accessing DynamoDB table '{table_name}': {str(e)}"
            }

        try:
            logging.info(f"Inserting data into table '{table_name}': {data_store}")
            response = table.put_item(Item=data_store)
            logging.info(f"Data inserted successfully into '{table_name}' with partition key '{partition_key_name}'.")

            return {
                'statusCode': 200,
                'body': f"Data inserted successfully with partition key: {partition_key_name}"
            }
        except Exception as e:
            logging.error(f"Error inserting data into table '{table_name}': {str(e)}")
            return {
                'statusCode': 500,
                'body': f"Error inserting data into table '{table_name}': {str(e)}"
            }

    def retrieve_data(self, table_name: str,
                      partition_key_name: str,
                      partition_key_value: str,
                      limit=10) -> dict:
        """
        Retrieves the last 10 records from a DynamoDB table for a given partition key.

        Parameters:
        -----------
        table_name : str
            The name of the DynamoDB table from which data will be retrieved.
        partition_key_name : str
            The name of the partition key to filter records.
        partition_key_value : str
            The value of the partition key to retrieve the corresponding records.
        limit : int
            Default =10
            Limit the number of items that can be return by the dynamodb query

        Returns:
        --------
        dict
            A dictionary containing either the retrieved records or an error message.
        """
        try:
            table = self.dynamodb.Table(table_name)
        except Exception as e:
            logging.error(f"Error accessing DynamoDB table '{table_name}': {str(e)}")
            return {
                'statusCode': 500,
                'body': f"Error accessing DynamoDB table '{table_name}': {str(e)}"
            }

        try:
            logging.info(f"Retrieving data from '{table_name}' for partition key '{partition_key_name}' = '{partition_key_value}'.")
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key(partition_key_name).eq(partition_key_value),
                ScanIndexForward=False,  # Retrieve in descending order
                Limit=limit  # Retrieve up to the last 10 items
            )
            items = response.get('Items', [])

            logging.info(f"Retrieved {len(items)} records from table '{table_name}'.")
            return {'statusCode': 200, 'body': items}
        except Exception as e:
            logging.error(f"Error retrieving items from table '{table_name}': {str(e)}")
            return {'statusCode': 500, 'body': f"Error retrieving items from table '{table_name}': {str(e)}"}
