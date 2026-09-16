"""
Grounds replies in real history: find past customer messages similar to the
incoming one, and surface how AdobeCare actually resolved those.

Uses TF-IDF cosine similarity rather than a neural embedding model, because
neural embedding models (sentence-transformers etc.) live on huggingface.co,
which isn't reachable in a locked-down/offline environment. TF-IDF is a fair,
fully-local baseline for this — note in the report that swapping in real
embeddings is a likely quick win (see "what I'd do with one more week").
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src import config


class HistoryRetriever:
    def __init__(self, history_df: pd.DataFrame):
        """history_df needs columns: customer_text, brand_reply_text"""
        # Drop rows with missing/empty text — TF-IDF can't vectorize NaN, and an
        # empty "past resolution" is useless as retrieval context anyway.
        df = history_df.copy()
        df["customer_text"] = df["customer_text"].fillna("").astype(str)
        df["brand_reply_text"] = df["brand_reply_text"].fillna("").astype(str)
        df = df[df["customer_text"].str.strip() != ""]
        self.df = df.reset_index(drop=True)
        self.vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")
        self.matrix = self.vec.fit_transform(self.df["customer_text"].astype(str))

    def retrieve(self, query: str, k: int = config.TOP_K_RETRIEVAL):
        q_vec = self.vec.transform([query])
        sims = cosine_similarity(q_vec, self.matrix)[0]
        top_idx = sims.argsort()[::-1][:k]
        return [
            {
                "customer_text": self.df.iloc[i]["customer_text"],
                "brand_reply_text": self.df.iloc[i]["brand_reply_text"],
                "similarity": float(sims[i]),
            }
            for i in top_idx
        ]
