"""Unit tests for Research Assistant Agent."""

import pytest
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from search_tools import search_web, extract_article_content, validate_url, SearchError
from document_generator import DocumentGenerator


class TestSearchTools:
    """Test search and content extraction tools."""
    
    def test_search_web(self):
        """Test web search functionality."""
        try:
            results = search_web("Python programming", num_results=3)
            assert isinstance(results, list)
            if results:  # May be empty due to rate limits
                assert len(results) <= 3
                assert "title" in results[0]
                assert "link" in results[0]
        except SearchError:
            pytest.skip("Search API unavailable")
    
    def test_validate_url(self):
        """Test URL validation."""
        assert validate_url("https://www.example.com") == True
        assert validate_url("http://example.com/path") == True
        assert validate_url("not a url") == False
        assert validate_url("") == False
    
    def test_extract_article_content(self):
        """Test content extraction from a known URL."""
        try:
            # Use a simple, stable URL
            content = extract_article_content("https://www.example.com")
            assert "title" in content
            assert "content" in content
            assert "url" in content
            assert len(content["content"]) > 0
        except SearchError as e:
            pytest.skip(f"Content extraction failed: {str(e)}")


class TestDocumentGenerator:
    """Test document generation functionality."""
    
    @pytest.fixture
    def generator(self):
        """Create a document generator instance."""
        return DocumentGenerator()
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for report generation."""
        return {
            "topic": "Test Topic",
            "summary": "This is a test summary of the research.",
            "findings": [
                "Finding number one",
                "Finding number two",
                "Finding number three"
            ],
            "sources": [
                {
                    "title": "Test Article 1",
                    "link": "https://example.com/article1",
                    "snippet": "This is article 1"
                },
                {
                    "title": "Test Article 2",
                    "link": "https://example.com/article2",
                    "snippet": "This is article 2"
                }
            ]
        }
    
    def test_generate_structured_report(self, generator, sample_data):
        """Test structured report generation."""
        report = generator.generate_report(
            topic=sample_data["topic"],
            summary=sample_data["summary"],
            findings=sample_data["findings"],
            sources=sample_data["sources"]
        )
        
        assert isinstance(report, str)
        assert sample_data["topic"] in report
        assert sample_data["summary"] in report
        assert "Key Findings" in report
        assert "Sources and References" in report
    
    def test_create_bibliography(self, generator, sample_data):
        """Test bibliography creation."""
        bibliography = generator.create_bibliography(sample_data["sources"])
        
        assert isinstance(bibliography, str)
        assert "Bibliography" in bibliography
        assert sample_data["sources"][0]["title"] in bibliography
    
    def test_save_report(self, generator, sample_data, tmp_path):
        """Test saving report to file."""
        # Override OUTPUT_DIR for testing
        import config
        original_dir = config.OUTPUT_DIR
        config.OUTPUT_DIR = str(tmp_path)
        generator = DocumentGenerator()  # Reinitialize with new config
        
        report = generator.generate_report(
            topic=sample_data["topic"],
            summary=sample_data["summary"],
            findings=sample_data["findings"],
            sources=sample_data["sources"]
        )
        
        filepath = generator.save_report(report, "test-report")
        
        assert os.path.exists(filepath)
        assert filepath.endswith(".md")
        
        # Read back and verify
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            assert sample_data["topic"] in content
        
        # Restore original config
        config.OUTPUT_DIR = original_dir


class TestResearchAgent:
    """Test Research Agent functionality."""
    
    @pytest.fixture
    def agent(self):
        """Create a research agent instance for testing."""
        from research_agent import ResearchAgent
        try:
            return ResearchAgent()
        except Exception as e:
            pytest.skip(f"Cannot initialize agent (check API keys): {str(e)}")
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly."""
        assert agent is not None
        assert agent.model is not None
        assert len(agent.tools) > 0
        assert agent.doc_generator is not None
    
    def test_agent_simple_query(self, agent):
        """Test a simple research query."""
        try:
            response = agent.query("What is Python?")
            assert isinstance(response, str)
            assert len(response) > 0
        except Exception as e:
            pytest.skip(f"Query failed: {str(e)}")
    
    def test_agent_clear_history(self, agent):
        """Test clearing research context."""
        agent.research_context["findings"].append({"finding": "test", "source": "test"})
        assert len(agent.research_context["findings"]) > 0
        
        agent.clear_history()
        assert len(agent.research_context["findings"]) == 0
        assert len(agent.research_context["sources"]) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

