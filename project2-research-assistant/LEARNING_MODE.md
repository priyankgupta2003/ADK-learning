# Learning Mode - Research Assistant

## 📚 How This Project Works

This Research Assistant demonstrates Google ADK's multi-step reasoning and tool chaining capabilities.

## 🎓 Learning Mode (Default)

By default, this project uses **simulated search results** for learning purposes. This allows you to:

✅ Focus on learning Google ADK concepts  
✅ Understand how agents use tools  
✅ See multi-step reasoning in action  
✅ Practice without web scraping complexity  

### What You'll See

When you ask a research question, the agent will:
1. Search for information (using simulated results)
2. Extract article content (simulated)
3. Save findings
4. Synthesize a response

### Example

```
You: "What are the top skills for software developers?"

Agent: 
- Searches for "top skills software developers"
- Finds 5 simulated articles
- Extracts content from each
- Saves key findings
- Provides a comprehensive answer
```

## 🌐 Production Mode (Optional)

To use **real web search**, install BeautifulSoup4:

```bash
pip install beautifulsoup4
```

The agent will automatically:
- Use real DuckDuckGo search
- Extract actual web page content
- Provide real-time information

## 💡 Why Use Learning Mode?

1. **Focus on ADK Concepts** - Learn agent architecture without distractions
2. **No Dependencies** - Works immediately without extra packages
3. **Reliable** - No network issues or blocked requests
4. **Fast** - Instant responses for rapid experimentation

## 🎯 What You're Learning

The important ADK concepts demonstrated:

- ✅ **Tool Chaining** - Agent calls multiple tools in sequence
- ✅ **State Management** - Tracks findings across tool calls
- ✅ **Multi-Step Reasoning** - Breaks down research into steps
- ✅ **Context Handling** - Maintains research context
- ✅ **Document Generation** - Creates structured reports

These concepts work identically with real or simulated data!

## 🚀 Upgrade Path

1. **Start:** Use learning mode to understand ADK
2. **Practice:** Build confidence with simulated results
3. **Upgrade:** Install BeautifulSoup4 for real search
4. **Extend:** Add Google Custom Search API for production

## 📝 Summary

- Default: Simulated results (perfect for learning)
- Optional: Real web search (install beautifulsoup4)
- Learn: Google ADK tool patterns and agent architecture

**The Google ADK concepts are the same either way!**

