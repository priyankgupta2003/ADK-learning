# Project 5: Customer Support Agent

An advanced project building an intelligent customer support agent using Google ADK with RAG (Retrieval Augmented Generation) and vector database integration.

## 🎯 Learning Objectives

- Implement RAG with vector databases
- Manage knowledge bases
- Handle multi-turn conversations
- Implement escalation workflows
- Use ADK for customer support automation

## 🌟 Features

- Answer FAQs from knowledge base
- Create and track support tickets
- Multi-turn conversation management
- Sentiment analysis
- Escalation to human agents
- Knowledge base management

## 📋 Prerequisites

- Completed Projects 1-4
- Python 3.10+
- Google ADK installed
- Understanding of vector databases

## 🚀 Setup

### Install Required Dependencies

```bash
# Install ChromaDB for vector database
pip install chromadb

# ChromaDB will automatically install required dependencies including:
# - sentence-transformers (for embeddings)
# - numpy, pandas, etc.
```

**Note:** First install may take a few minutes as it downloads the embedding model.

## 🎮 Usage

```bash
python support_agent.py
```

## 📚 Key Concepts

### 1. RAG (Retrieval Augmented Generation)
- Store knowledge in vector database
- Retrieve relevant context for queries
- Generate responses with retrieved context

### 2. Vector Databases
- Use ChromaDB for semantic search
- Embed documents and queries
- Find similar content

### 3. Conversation Management
- Track conversation history
- Maintain context across turns
- Handle follow-up questions

## 🔧 Project Structure

```
project5-customer-support-agent/
├── README.md
├── support_agent.py      # Main agent with ADK
├── knowledge_base.py     # RAG and vector DB
├── ticket_system.py      # Ticket management
├── config.py
└── data/
    └── knowledge/        # Knowledge base documents
```

## ⏭️ Next Steps

Move on to Project 6: Multi-Agent Task Orchestrator

