def simple_rerank(query, docs):
    scored = []

    for doc in docs:
        score = sum(1 for w in query.lower().split() if w in doc.lower())
        scored.append((score, doc))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [d for _, d in scored]
