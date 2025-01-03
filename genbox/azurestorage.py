from azure.data.tables import TableServiceClient, TableEntity
import os
from dotenv import load_dotenv
from utils import get_flat_date

load_dotenv()
# Configuration
connection_string = os.getenv('connection_string')
table_name = os.getenv('genbox_table_name') 

# Create a TableServiceClient
service_client = TableServiceClient.from_connection_string(conn_str=connection_string)

# Get a reference to the table client
table_client = service_client.get_table_client(table_name)

def insert_history(role, content):

    rowkey = get_flat_date()
    # Define the entity (row) to insert
    entity = {
        "PartitionKey": role,  # Logical grouping for entities
        "RowKey": rowkey,                # Unique identifier within the partition
        "role": role,
        "content": content
    }
    # Insert the entity
    try:
        table_client.create_entity(entity=entity)
        print("Row inserted successfully!")
    except Exception as e:
        print(f"Error inserting row: {e}")
        # if "EntityAlreadyExists" in str(e):
        #     entity["RowKey"] = "000" + entity["RowKey"]
        #     table_client.create_entity(entity=entity)
        #     print("Row inserted successfully!")


def get_last_n_rows(n=10):
    try:
        # Query all entities
        role = "assistant"
        entities = table_client.query_entities(query_filter=f"PartitionKey eq '{role}'", results_per_page=1000)

        # Convert the entities to a sorted list by RowKey (descending order)
        sorted_entities = sorted(
            entities,
            key=lambda x: x["RowKey"],  # Sort by RowKey
            reverse=False               # Ascending order
        )

        last_n_rows = [
            {key: value for key, value in row.items() if key not in ["PartitionKey", "RowKey"]}
            for row in sorted_entities[:n]
        ]

        return last_n_rows

    except Exception as e:
        print(f"Error retrieving rows: {e}")
        return None
    

def get_row(partitionkey, rowkey):
    try:
        # Retrieve the entity (row) using the PartitionKey and RowKey
        entity = table_client.get_entity(partition_key=partitionkey, row_key=rowkey)
        print(f"Row retrieved successfully: {entity}")
        return entity
    except Exception as e:
        print(f"Error retrieving row: {e}")
        return None