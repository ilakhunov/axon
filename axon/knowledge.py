import numpy as np
import json
from typing import List, Optional
from dataclasses import dataclass
from openai import OpenAI, AsyncOpenAI

@dataclass
class Document:
    content: str
    metadata: dict = None

class VectorDB:
    """
    Simple in-memory Vector Store using OpenAI Embeddings.
    """
    def __init__(self, client: OpenAI = None):
        self.documents: List[Document] = []
        self.vectors: Optional[np.ndarray] = None
        self.client = client or OpenAI()
        
    def add_documents(self, texts: List[str]):
        """Embed and store documents."""
        if not texts:
            return
            
        print(f"🧠 Embedding {len(texts)} documents...")
        
        # Batch embedding
        response = self.client.embeddings.create(
            input=texts,
            model="text-embedding-3-small"
        )
        
        new_vectors = np.array([d.embedding for d in response.data])
        
        # Store
        for text in texts:
            self.documents.append(Document(content=text))
            
        if self.vectors is None:
            self.vectors = new_vectors
        else:
            self.vectors = np.vstack([self.vectors, new_vectors])
            
    def search(self, query: str, k: int = 3) -> List[str]:
        """Return top-k relevant documents."""
        if self.vectors is None or len(self.documents) == 0:
            return []
            
        # Embed query
        q_resp = self.client.embeddings.create(
            input=query,
            model="text-embedding-3-small"
        )
        q_vec = np.array(q_resp.data[0].embedding)
        
        # Cosine similarity
        scores = np.dot(self.vectors, q_vec)
        
        # Get top k indices
        top_k_indices = np.argsort(scores)[-k:][::-1]
        
        results = [self.documents[i].content for i in top_k_indices]
        return results

class KnowledgeBase:
    """
    High-level interface for Agent knowledge.
    """
    def __init__(self, output_file: str = "knowledge.json"):
        self.db = VectorDB()
        
    def load_from_text(self, text: str):
        """Chunk text and load into DB."""
        # Simple chunking by paragraphs or sentences
        chunks = [c.strip() for c in text.split('\n\n') if c.strip()]
        self.db.add_documents(chunks)
        
    def load_from_file(self, filepath: str):
        """Load text file."""
        with open(filepath, 'r') as f:
            text = f.read()
        self.load_from_text(text)
        
    def query(self, query: str) -> str:
        """Get context string for a query."""
        docs = self.db.search(query)
        if not docs:
            return ""
        return "\n\n".join(docs)
