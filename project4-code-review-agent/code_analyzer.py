"""Code analysis tools for Code Review Agent."""

import ast
import re
from typing import Dict, Any, List
import os


def analyze_code(file_path: str) -> str:
    """Analyze code structure, get line counts, and identify functions and classes.
    
    Args:
        file_path: Path to the code file
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found - {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Basic metrics
        lines = code.split('\n')
        total_lines = len(lines)
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        comment_lines = len([l for l in lines if l.strip().startswith('#')])
        blank_lines = total_lines - code_lines - comment_lines
        
        result = f"Code Analysis for {file_path}:\n\n"
        result += f"Lines of Code:\n"
        result += f"  Total: {total_lines}\n"
        result += f"  Code: {code_lines}\n"
        result += f"  Comments: {comment_lines}\n"
        result += f"  Blank: {blank_lines}\n\n"
        
        # For Python files, parse AST
        if file_path.endswith('.py'):
            try:
                tree = ast.parse(code)
                functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                
                result += f"Python Structure:\n"
                result += f"  Functions: {len(functions)}\n"
                if functions:
                    result += f"    {', '.join(functions[:10])}\n"
                result += f"  Classes: {len(classes)}\n"
                if classes:
                    result += f"    {', '.join(classes[:10])}\n"
            except SyntaxError as e:
                result += f"\nSyntax Error: {str(e)}\n"
        
        return result
    
    except Exception as e:
        return f"Error analyzing code: {str(e)}"


def check_code_metrics(file_path: str) -> str:
    """Check code complexity and quality metrics including cyclomatic complexity and function lengths.
    
    Args:
        file_path: Path to the code file
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found - {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        result = f"Code Metrics for {file_path}:\n\n"
        
        # Calculate basic complexity (simplified)
        if file_path.endswith('.py'):
            try:
                tree = ast.parse(code)
                
                # Count control flow statements
                control_flow = 0
                for node in ast.walk(tree):
                    if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                        control_flow += 1
                
                result += f"Complexity:\n"
                result += f"  Control Flow Statements: {control_flow}\n"
                result += f"  Estimated Cyclomatic Complexity: {control_flow + 1}\n\n"
                
                # Function lengths
                function_lengths = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                        function_lengths.append((node.name, func_lines))
                
                if function_lengths:
                    max_length = max([f[1] for f in function_lengths])
                    result += f"Function Lengths:\n"
                    result += f"  Total Functions: {len(function_lengths)}\n"
                    result += f"  Longest Function: {max_length} lines\n"
                    result += f"\n  Top 5 Longest Functions:\n"
                    for name, lines in sorted(function_lengths, key=lambda x: x[1], reverse=True)[:5]:
                        result += f"    - {name}: {lines} lines\n"
                
            except SyntaxError as e:
                result += f"Syntax error: {str(e)}\n"
        
        return result
    
    except Exception as e:
        return f"Error checking code metrics: {str(e)}"


def detect_issues(file_path: str) -> str:
    """Detect common code issues, anti-patterns, and style violations.
    
    Args:
        file_path: Path to the code file
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found - {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
            lines = code.split('\n')
        
        issues = []
        
        # Check for common issues
        for i, line in enumerate(lines, 1):
            # Long lines
            if len(line) > 120:
                issues.append({
                    "line": i,
                    "severity": "minor",
                    "issue": "Line too long",
                    "description": f"Line has {len(line)} characters (recommended max: 120)"
                })
            
            # Bare except clauses
            if re.search(r'except\s*:', line):
                issues.append({
                    "line": i,
                    "severity": "major",
                    "issue": "Bare except clause",
                    "description": "Use specific exception types instead of bare 'except:'"
                })
            
            # TODO comments
            if 'TODO' in line or 'FIXME' in line:
                issues.append({
                    "line": i,
                    "severity": "minor",
                    "issue": "TODO/FIXME comment",
                    "description": "Unresolved TODO or FIXME comment"
                })
        
        # Python-specific checks
        if file_path.endswith('.py'):
            try:
                tree = ast.parse(code)
                
                # Check for functions without docstrings
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if not ast.get_docstring(node):
                            issues.append({
                                "line": node.lineno,
                                "severity": "minor",
                                "issue": "Missing docstring",
                                "description": f"Function '{node.name}' has no docstring"
                            })
            
            except SyntaxError:
                pass
        
        # Format issues as string
        if not issues:
            return f"No issues detected in {file_path}. Code looks good!"
        
        result = f"Found {len(issues)} issues in {file_path}:\n\n"
        
        # Group by severity
        critical = [i for i in issues if i['severity'] == 'critical']
        major = [i for i in issues if i['severity'] == 'major']
        minor = [i for i in issues if i['severity'] == 'minor']
        
        if critical:
            result += f"CRITICAL ({len(critical)}):\n"
            for issue in critical:
                result += f"  Line {issue['line']}: {issue['issue']} - {issue['description']}\n"
            result += "\n"
        
        if major:
            result += f"MAJOR ({len(major)}):\n"
            for issue in major[:5]:  # Limit output
                result += f"  Line {issue['line']}: {issue['issue']} - {issue['description']}\n"
            if len(major) > 5:
                result += f"  ... and {len(major) - 5} more\n"
            result += "\n"
        
        if minor:
            result += f"MINOR ({len(minor)}): {len(minor)} minor issues found\n"
        
        return result
    
    except Exception as e:
        return f"Error detecting issues: {str(e)}"

