"""Knowledge base and RAG implementation for Customer Support Agent."""

from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
import os
from config import VECTOR_DB_DIR, KNOWLEDGE_BASE_DIR, TOP_K_RESULTS


class KnowledgeBase:
    """Manage knowledge base with vector search."""
    
    def __init__(self):
        """Initialize the knowledge base."""
        self.client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
        self.collection = self.client.get_or_create_collection(
            name="support_kb",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_document(self, doc_id: str, text: str, metadata: Dict = None):
        """Add a document to the knowledge base."""
        self.collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[metadata or {}]
        )
    
    def search(self, query: str, top_k: int = TOP_K_RESULTS) -> List[Dict]:
        """Search the knowledge base."""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        documents = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                documents.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
        
        return documents
    
    def load_knowledge_files(self):
        """Load knowledge base files from directory."""
        if not os.path.exists(KNOWLEDGE_BASE_DIR):
            return
        
        for filename in os.listdir(KNOWLEDGE_BASE_DIR):
            if filename.endswith(('.txt', '.md')):
                filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.add_document(
                        doc_id=filename,
                        text=content,
                        metadata={"source": filename}
                    )


def search_knowledge_base(query: str, top_k: int = TOP_K_RESULTS) -> str:
    """Search the knowledge base for product information, FAQs, and troubleshooting guides.
    
    Args:
        query: Search query
        top_k: Number of results to return
    """
    try:
        kb = KnowledgeBase()
        
        # Load knowledge files if collection is empty
        if kb.collection.count() == 0:
            kb.load_knowledge_files()
        
        results = kb.search(query, top_k)
        
        if results:
            formatted = f"Found {len(results)} relevant articles:\n\n"
            for i, doc in enumerate(results, 1):
                formatted += f"{i}. {doc['content'][:300]}...\n"
                if doc.get('metadata'):
                    formatted += f"   Source: {doc['metadata'].get('source', 'Unknown')}\n"
                formatted += "\n"
            return formatted
        else:
            return "No relevant information found in knowledge base for your query."
    
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"

