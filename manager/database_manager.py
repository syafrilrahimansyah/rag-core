import sqlite3
import os
from pymilvus import MilvusClient, DataType, CollectionSchema, FieldSchema

class DatabaseManager:
    def __init__(self, host, port, collection_name, dimension):
        self.db_folder = "db"
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)

        self.sqlite_path = os.path.join(self.db_folder, "metadata.db")
        self.sql_conn = sqlite3.connect(self.sqlite_path, check_same_thread=False)
        self._prepare_sqlite()
        
        self.collection_name = collection_name
        self.milvus_client = MilvusClient(uri=f"http://{host}:{port}")

        # --- ADD THESE LINES HERE ---
        print(f"Dropping collection {self.collection_name} to clear metadata...")
        try:
            self.milvus_client.drop_collection(self.collection_name)
        except Exception as e:
            print(f"Notice: Could not drop collection (it might not exist yet): {e}")
        # ----------------------------

        self._prepare_milvus(dimension)

    def _prepare_sqlite(self):
        self.sql_conn.execute("""
            CREATE TABLE IF NOT EXISTS docs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                content TEXT NOT NULL, 
                source TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.sql_conn.commit()

    def _prepare_milvus(self, dimension):
        if not self.milvus_client.has_collection(self.collection_name):
            # 1. Define Fields explicitly using FieldSchema
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
                FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension)
            ]

            # 2. Build the Schema
            schema = CollectionSchema(fields, enable_dynamic_field=True)

            # 3. Define Index Parameters
            index_params = self.milvus_client.prepare_index_params()
            index_params.add_index(
                field_name="vector",
                metric_type="L2",
                index_type="IVF_FLAT",
                params={"nlist": 128}
            )

            # 4. Create collection using the explicit schema object
            self.milvus_client.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                index_params=index_params
            )
            print(f"Collection {self.collection_name} created successfully with dim {dimension}")

    def save_document(self, text, source):
        cursor = self.sql_conn.cursor()
        cursor.execute("INSERT INTO docs (content, source) VALUES (?, ?)", (text, source))
        doc_id = cursor.lastrowid
        self.sql_conn.commit()
        return doc_id