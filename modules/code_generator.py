import os
import json
from typing import Dict
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class CodeGenerator:
    """Generates Python code based on analyzed requirements"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-pro") if GEMINI_API_KEY else None
    
    def generate(self, analysis: Dict) -> str:
        """
        Generate Python code based on analysis
        
        Args:
            analysis: Analysis result from RequirementAnalyzer
            
        Returns:
            Generated Python code as string
        """
        
        if not self.model:
            return self._generate_template_code(analysis)
        
        libraries = ", ".join(analysis.get("libraries", ["os"]))
        tasks = "\n".join([f"- {task}" for task in analysis.get("tasks", [])])
        
        prompt = f"""
        Generate production-ready Python code that accomplishes the following tasks:
        
        {tasks}
        
        Use these libraries: {libraries}
        
        Requirements:
        1. Write clean, modular, and well-commented code
        2. Include error handling and input validation
        3. Use functions to organize code
        4. Add docstrings for all functions
        5. Make it testable
        6. Include a main() function
        
        Generate only the Python code, no explanations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            code = response.text
            
            # Clean up the code
            if code.startswith("```"):
                code = "\n".join(code.split("\n")[1:-1])
            
            return code
        
        except Exception as e:
            print(f"Error generating code: {str(e)}")
            return self._generate_template_code(analysis)
    
    def _generate_template_code(self, analysis: Dict) -> str:
        """Generate template code when API is not available"""
        
        libraries = ", ".join(analysis.get("libraries", ["os"]))
        tasks = analysis.get("tasks", [])
        
        template = f'''"""
Generated Python Module
Tasks: {", ".join(tasks[:3])}
Libraries: {libraries}
"""

import os
import sys
from typing import Any, List, Dict

def read_input() -> Dict[str, Any]:
    """Read and validate input"""
    try:
        print("Enter input data or file path:")
        user_input = input().strip()
        return {{"input": user_input}}
    except Exception as e:
        print(f"Error reading input: {{e}}")
        return {{}}

def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process the input data"""
    try:
        print(f"Processing: {{data}}")
        # Add your processing logic here
        result = {{
            "status": "success",
            "data": data,
            "processed": True
        }}
        return result
    except Exception as e:
        print(f"Error processing data: {{e}}")
        return {{"status": "error", "message": str(e)}}

def format_output(result: Dict[str, Any]) -> str:
    """Format the output"""
    if result.get("status") == "success":
        return f"Success: {{result}}"
    else:
        return f"Error: {{result.get('message', 'Unknown error')}}"

def main():
    """Main function"""
    print("=" * 50)
    print("Python Application Started")
    print("=" * 50)
    
    # Read input
    input_data = read_input()
    
    # Process
    result = process_data(input_data)
    
    # Output
    output = format_output(result)
    print(output)
    
    print("=" * 50)
    print("Application completed successfully")
    print("=" * 50)

if __name__ == "__main__":
    main()
'''
        
        return template
