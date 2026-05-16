import ollama
from ollama import Client

class RAGEngine:
    def __init__(self, db_manager, embed_model, gen_model, ollama_url):
        self.db = db_manager
        self.embed_model = embed_model
        self.gen_model = gen_model
        self.client = Client(host=ollama_url)

    def _get_embedding(self, text):
        response = self.client.embed(model=self.embed_model, input=text)
        return response['embeddings'][0]

    def ingest(self, text, source):
        """Stores text in SQLite and its vector in Milvus."""
        doc_id = self.db.save_document(text, source)
        vector = self._get_embedding(text)
        self.db.milvus_client.insert(
            collection_name=self.db.collection_name,
            data=[{
                "id": doc_id, 
                "vector": vector, 
                "text": text 
            }]
        )

    def retrieve_context(self, query, limit=3):
        """Finds the top matching text chunks from Milvus."""
        query_vector = self._get_embedding(query)
        results = self.db.milvus_client.search(
            collection_name=self.db.collection_name,
            data=[query_vector],
            limit=limit,
            output_fields=["text"]
        )
        return "\n".join([res['entity']['text'] for res in results[0]])

    def generate_answer(self, question):
        """Retrieves context and generates a response via Ollama."""
        context = self.retrieve_context(question)
        prompt = f"""
        You are a helpful assistant. Use the provided context to answer the user's question accurately.
        If the answer is not in the context, politely state that you do not know.
        CONTEXT:
        {context}
        USER QUESTION:
        {question}
        """
        print(f"Generated Prompt:\n{prompt}\n--- End of Prompt ---")
        
        response = self.client.generate(
            model=self.gen_model, 
            prompt=prompt,
            options={"temperature": 0.2}
        )
        return response['response']