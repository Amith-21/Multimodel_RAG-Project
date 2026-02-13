import faiss


class FAISSRetriever:
    def __init__(self, embeddings, metadata):
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.metadata = metadata

    def search(self, query_embedding, top_k=5, filter_type=None):
        _, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            meta = self.metadata[idx]

            if filter_type and meta["type"] != filter_type:
                continue

            results.append(idx)

        return results
