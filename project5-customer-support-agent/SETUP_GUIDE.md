# Project 5 Setup Guide - Customer Support Agent with RAG

## 📦 Installation Steps

### Step 1: Install ChromaDB

Project 5 requires ChromaDB for the vector database (RAG):

```bash
pip install chromadb
```

This will install:
- ✅ ChromaDB (vector database)
- ✅ Sentence-transformers (embedding model)
- ✅ Required dependencies

**First install may take 2-3 minutes** as it downloads the embedding model (~80 MB).

### Step 2: Verify Installation

```bash
python -c "import chromadb; print('ChromaDB installed successfully!')"
```

### Step 3: Run the Agent

```bash
cd project5-customer-support-agent
python support_agent.py
```

---

## 🗄️ How the VectorDB Works

### Automatic Setup

When you first run the agent:

1. **ChromaDB creates database** automatically in `data/vectordb/`
2. **Knowledge files are loaded** from `data/knowledge/` 
3. **Embeddings are generated** using sentence-transformers
4. **Ready for semantic search!**

### Directory Structure

```
project5-customer-support-agent/
├── data/
│   ├── vectordb/              ← ChromaDB storage (auto-created)
│   │   └── chroma.sqlite3     ← Vector database file
│   ├── knowledge/             ← Put your FAQ/docs here
│   │   └── faq.md            ← Sample knowledge base
│   └── tickets/               ← Support tickets
```

---

## 📝 Adding Your Own Knowledge

### Method 1: Add Files to data/knowledge/

1. Create `.txt` or `.md` files in `data/knowledge/`
2. Add your content (FAQs, documentation, policies)
3. Run the agent - it auto-loads all files!

Example:
```bash
# Create a new knowledge file
echo "Q: What payment methods do you accept?
A: We accept credit cards, PayPal, and bank transfers." > data/knowledge/payment.md

# Run agent
python support_agent.py
# Agent can now answer payment questions!
```

### Method 2: Programmatic (Advanced)

```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()
kb.add_document(
    doc_id="custom_doc_1",
    text="Your content here...",
    metadata={"source": "Custom", "category": "Billing"}
)
```

---

## 🔍 Testing the Knowledge Base

### Test if Knowledge is Loaded:

```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()
print(f"Documents in collection: {kb.collection.count()}")

# Load knowledge files
kb.load_knowledge_files()
print(f"After loading: {kb.collection.count()}")

# Search
results = kb.search("How do I reset my password?")
for result in results:
    print(result['content'][:200])
```

### Test with the Agent:

```bash
python support_agent.py
```

Ask:
- "How do I reset my password?"
- "How do I invite team members?"
- "What payment methods do you accept?"

All these are in the sample `faq.md` file!

---

## 🐛 Troubleshooting

### "Module 'chromadb' not found"
```bash
pip install chromadb
```

### "No results found in knowledge base"
**Cause:** Knowledge files not loaded into ChromaDB

**Fix:** The fix I just applied will auto-load files on first search!

**Manual fix:**
```python
from knowledge_base import KnowledgeBase
kb = KnowledgeBase()
kb.load_knowledge_files()  # Manually load files
```

### "Collection is empty"
**Cause:** No `.txt` or `.md` files in `data/knowledge/`

**Fix:** Add knowledge files or use the sample `faq.md` provided

---

## 💡 How RAG Works in This Project

### The Flow:

1. **User asks question** → "How do I invite team members?"

2. **search_knowledge_base tool called** → Checks if documents loaded

3. **Auto-loads if empty** → Loads all .txt/.md files from data/knowledge/

4. **Semantic search** → Finds relevant content by meaning

5. **Returns context** → Agent gets relevant FAQ section

6. **Agent responds** → Uses context to answer question

---

## 🎓 What You're Learning

**RAG (Retrieval Augmented Generation):**
- Store knowledge in vector database
- Retrieve relevant context for queries
- Generate responses using retrieved information

**Vector Databases:**
- ChromaDB for local vector storage
- Semantic search by meaning (not keywords)
- Persistent storage across sessions

**This is the same pattern used by ChatGPT, Claude, and all modern AI assistants!**

---

## 🚀 Quick Fix Applied

I just updated `knowledge_base.py` to **automatically load knowledge files** on first search if the collection is empty.

### Try Again Now:

```bash
python support_agent.py
```

Ask: **"How do I invite team members?"**

It should now find the answer in the FAQ! ✅

---

## 📊 What's in the Sample FAQ

The provided `data/knowledge/faq.md` includes:

- Account Management (reset password, update email)
- Billing (payment methods, cancel subscription)
- Technical Support (slow app, error messages)
- **Features (invite team members!)** ← Your question
- Data Export

Try asking about any of these topics!

---

Let me know if it works now! 🎯

