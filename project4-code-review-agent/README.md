# Project 4: Code Review Agent

An advanced project that builds an AI-powered code review agent using Google ADK with code parsing and analysis capabilities.

## 🎯 Learning Objectives

- Parse and analyze code using AST
- Handle multi-file context
- Provide technical feedback
- Generate documentation
- Use ADK for complex technical reasoning

## 🌟 Features

- Analyze code quality and style
- Detect bugs and security vulnerabilities
- Suggest optimizations and best practices
- Generate code documentation
- Check for code smells and anti-patterns
- Multi-language support (Python, JavaScript, Java, etc.)

## 📋 Prerequisites

- Completed Projects 1-3
- Python 3.10+
- Google ADK installed
- Understanding of code analysis concepts

## 🚀 Setup

```bash
pip install google-adk pylint radon ast-tools
```

## 🎮 Usage

```bash
python code_review_agent.py path/to/code.py
```

## 📚 Key Concepts

### 1. Code Parsing with AST
- Parse Python code into Abstract Syntax Trees
- Analyze code structure and complexity

### 2. Static Analysis
- Use pylint, radon for code metrics
- Detect common issues automatically

### 3. AI-Powered Review
- Use ADK agent to provide contextual feedback
- Explain issues and suggest improvements

## 🔧 Project Structure

```
project4-code-review-agent/
├── README.md
├── code_review_agent.py    # Main agent with ADK
├── code_analyzer.py         # Code analysis tools
├── config.py
└── tests/
```

## ⏭️ Next Steps

Move on to Project 5: Customer Support Agent (RAG and knowledge base)

