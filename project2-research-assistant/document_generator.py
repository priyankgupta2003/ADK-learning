"""Document generation utilities for Research Assistant Agent."""

from typing import List, Dict, Optional
from datetime import datetime
import re
from config import REPORT_TEMPLATE, INCLUDE_CITATIONS, CITATION_FORMAT, OUTPUT_DIR
import os


class DocumentGenerator:
    """Generate formatted research documents."""
    
    def __init__(self):
        """Initialize the document generator."""
        self.template = REPORT_TEMPLATE
        self.include_citations = INCLUDE_CITATIONS
        self.citation_format = CITATION_FORMAT
    
    def generate_report(
        self,
        topic: str,
        summary: str,
        findings: List[str],
        sources: List[Dict],
        additional_sections: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Generate a structured research report.
        
        Args:
            topic: Research topic
            summary: Executive summary
            findings: List of key findings
            sources: List of source dictionaries with title, url, snippet
            additional_sections: Optional dict of section_name: content
        
        Returns:
            Formatted report as a string
        """
        if self.template == "structured":
            return self._generate_structured_report(
                topic, summary, findings, sources, additional_sections
            )
        elif self.template == "summary":
            return self._generate_summary_report(topic, summary, findings, sources)
        else:
            return self._generate_detailed_report(
                topic, summary, findings, sources, additional_sections
            )
    
    def _generate_structured_report(
        self,
        topic: str,
        summary: str,
        findings: List[str],
        sources: List[Dict],
        additional_sections: Optional[Dict[str, str]] = None
    ) -> str:
        """Generate a structured research report."""
        lines = []
        
        # Header
        lines.append(f"# Research Report: {topic}")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Sources:** {len(sources)}\n")
        lines.append("---\n")
        
        # Executive Summary
        lines.append("## Executive Summary\n")
        lines.append(summary)
        lines.append("\n")
        
        # Key Findings
        if findings:
            lines.append("## Key Findings\n")
            for i, finding in enumerate(findings, 1):
                lines.append(f"{i}. {finding}")
            lines.append("\n")
        
        # Additional Sections
        if additional_sections:
            for section_name, content in additional_sections.items():
                lines.append(f"## {section_name}\n")
                lines.append(content)
                lines.append("\n")
        
        # Sources and References
        if self.include_citations and sources:
            lines.append("## Sources and References\n")
            lines.extend(self._format_citations(sources))
        
        return "\n".join(lines)
    
    def _generate_summary_report(
        self,
        topic: str,
        summary: str,
        findings: List[str],
        sources: List[Dict]
    ) -> str:
        """Generate a concise summary report."""
        lines = [
            f"# {topic}\n",
            summary,
            "\n**Key Points:**\n"
        ]
        
        for finding in findings:
            lines.append(f"- {finding}")
        
        if self.include_citations and sources:
            lines.append("\n**Sources:**")
            for source in sources:
                lines.append(f"- {source.get('title', 'Unknown')}: {source.get('link', '')}")
        
        return "\n".join(lines)
    
    def _generate_detailed_report(
        self,
        topic: str,
        summary: str,
        findings: List[str],
        sources: List[Dict],
        additional_sections: Optional[Dict[str, str]] = None
    ) -> str:
        """Generate a detailed research report."""
        lines = []
        
        # Title Page
        lines.append("=" * 80)
        lines.append(f"{topic.upper()}")
        lines.append("Research Report")
        lines.append(f"Generated: {datetime.now().strftime('%B %d, %Y')}")
        lines.append("=" * 80)
        lines.append("\n")
        
        # Table of Contents
        lines.append("TABLE OF CONTENTS")
        lines.append("-" * 80)
        lines.append("1. Executive Summary")
        lines.append("2. Key Findings")
        if additional_sections:
            for i, section in enumerate(additional_sections.keys(), 3):
                lines.append(f"{i}. {section}")
        lines.append(f"{len(additional_sections) + 3 if additional_sections else 3}. References")
        lines.append("\n" + "=" * 80 + "\n")
        
        # Executive Summary
        lines.append("1. EXECUTIVE SUMMARY")
        lines.append("-" * 80)
        lines.append(summary)
        lines.append("\n" + "=" * 80 + "\n")
        
        # Key Findings
        lines.append("2. KEY FINDINGS")
        lines.append("-" * 80)
        for i, finding in enumerate(findings, 1):
            lines.append(f"\n{i}. {finding}")
        lines.append("\n" + "=" * 80 + "\n")
        
        # Additional Sections
        if additional_sections:
            for i, (section_name, content) in enumerate(additional_sections.items(), 3):
                lines.append(f"{i}. {section_name.upper()}")
                lines.append("-" * 80)
                lines.append(content)
                lines.append("\n" + "=" * 80 + "\n")
        
        # References
        section_num = len(additional_sections) + 3 if additional_sections else 3
        lines.append(f"{section_num}. REFERENCES")
        lines.append("-" * 80)
        lines.extend(self._format_citations(sources))
        
        return "\n".join(lines)
    
    def _format_citations(self, sources: List[Dict]) -> List[str]:
        """Format citations based on the specified format."""
        citations = []
        
        for i, source in enumerate(sources, 1):
            title = source.get('title', 'Unknown Title')
            url = source.get('link', source.get('url', ''))
            source_name = source.get('source', '')
            
            if self.citation_format == "markdown":
                citations.append(f"{i}. [{title}]({url})")
                if source_name:
                    citations.append(f"   Source: {source_name}")
            elif self.citation_format == "apa":
                # Simplified APA format
                date = datetime.now().strftime('%Y, %B %d')
                citations.append(f"{i}. {title}. ({date}). Retrieved from {url}")
            elif self.citation_format == "mla":
                # Simplified MLA format
                date = datetime.now().strftime('%d %B %Y')
                citations.append(f'{i}. "{title}." Web. {date}. <{url}>')
            else:
                citations.append(f"{i}. {title} - {url}")
        
        return citations
    
    def save_report(self, content: str, filename: str) -> str:
        """
        Save report to a file.
        
        Args:
            content: Report content
            filename: Output filename (will be saved in OUTPUT_DIR)
        
        Returns:
            Full path to saved file
        """
        # Ensure filename is safe
        safe_filename = re.sub(r'[^\w\s-]', '', filename)
        safe_filename = re.sub(r'[-\s]+', '-', safe_filename)
        
        # Add .md extension if not present
        if not safe_filename.endswith('.md'):
            safe_filename += '.md'
        
        filepath = os.path.join(OUTPUT_DIR, safe_filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def create_bibliography(self, sources: List[Dict]) -> str:
        """
        Create a formatted bibliography.
        
        Args:
            sources: List of source dictionaries
        
        Returns:
            Formatted bibliography string
        """
        lines = ["# Bibliography\n"]
        lines.extend(self._format_citations(sources))
        return "\n".join(lines)

