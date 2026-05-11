import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

INPUT_PATH = "data/processed/clean_catalog.json"

INDEX_PATH = "data/processed/faiss.index"

EMBEDDINGS_PATH = "data/processed/embeddings.npy"


class EmbeddingBuilder:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def load_catalog(self):

        with open(
            INPUT_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def build_documents(self, items):

        docs = []

        for item in items:

            text = f"""
            Name: {item['name']}
            Description: {item['description']}
            Content: {item['content']}
            """

            docs.append(text)

        return docs

    def generate_embeddings(self, docs):

        embeddings = self.model.encode(
            docs,
            show_progress_bar=True
        )

        return np.array(
            embeddings,
            dtype="float32"
        )

    def build_faiss_index(self, embeddings):

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(dimension)

        index.add(embeddings)

        return index

    def save(self, embeddings, index):

        np.save(
            EMBEDDINGS_PATH,
            embeddings
        )

        faiss.write_index(
            index,
            INDEX_PATH
        )

    def run(self):

        print("Loading catalog...")

        items = self.load_catalog()

        print(f"Loaded {len(items)} items")

        print("Building documents...")

        docs = self.build_documents(items)

        print("Generating embeddings...")

        embeddings = self.generate_embeddings(docs)

        print("Building FAISS index...")

        index = self.build_faiss_index(
            embeddings
        )

        print("Saving index...")

        self.save(
            embeddings,
            index
        )

        print("Done!")


if __name__ == "__main__":

    builder = EmbeddingBuilder()

    builder.run()