import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


CATALOG_PATH = "data/processed/clean_catalog.json"

INDEX_PATH = "data/processed/faiss.index"


class SHLRetriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.index = faiss.read_index(
            INDEX_PATH
        )

        with open(
            CATALOG_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            self.catalog = json.load(f)

    def search(
        self,
        query,
        top_k=5
    ):

        query_embedding = self.model.encode(
            [query]
        ).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.catalog):

                results.append(
                    self.catalog[idx]
                )

        return results


if __name__ == "__main__":

    retriever = SHLRetriever()

    results = retriever.search(
        "Java developer with communication skills"
    )

    for r in results:

        print("=" * 50)
        print(r["name"])
        print(r["url"])