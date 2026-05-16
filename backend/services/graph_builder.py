import ast
from typing import List, Dict

class DependencyGraphBuilder:
    def __init__(self):
        """
        Initializes the Dependency Graph Builder.
        This module parses Python Abstract Syntax Trees (AST) to map relationships 
        and imports between different source code files.
        """
        self.dependency_map: Dict[str, List[str]] = {}

    def analyze_imports(self, file_path: str, code_content: str) -> List[str]:
        """
        Parses the code content to extract all imported modules, building a dependency tree.
        """
        extracted_imports = []
        try:
            # Parse the raw code string into an Abstract Syntax Tree
            tree = ast.parse(code_content)
            
            # Traverse all nodes in the AST
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        extracted_imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        extracted_imports.append(node.module)
                        
            # Store the mapped dependencies
            self.dependency_map[file_path] = extracted_imports
            return extracted_imports
            
        except SyntaxError as e:
            print(f"[WARNING] Syntax error detected in {file_path}. Cannot parse AST: {e}")
            return []
        except Exception as e:
            print(f"[ERROR] Failed to analyze dependencies for {file_path}. Reason: {e}")
            return []

# --- Testing the Module ---
if __name__ == "__main__":
    print("[INFO] Initializing Dependency Graph Builder...")
    
    builder = DependencyGraphBuilder()
    
    # A sample Python code snippet to test the AST parser
    sample_code = """
import os
import sys
from datetime import datetime
from backend.core.config import settings
    """
    
    print("[INFO] Analyzing sample code AST...")
    result = builder.analyze_imports("test_script.py", sample_code)
    
    print(f"[SUCCESS] Extracted Dependencies: {result}")