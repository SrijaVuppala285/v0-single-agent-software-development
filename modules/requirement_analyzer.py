import os
import json
from typing import Dict, List
import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class RequirementAnalyzer:
    """Analyzes user requirements and breaks them into actionable tasks"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-pro") if GEMINI_API_KEY else None
    
    def analyze(self, requirement: str) -> Dict:
        """
        Analyze requirement and extract tasks, libraries, and constraints
        
        Args:
            requirement: User requirement text
            
        Returns:
            Dictionary with tasks, libraries, and constraints
        """
        
        if not self.model:
            # Fallback analysis for development
            return self._fallback_analysis(requirement)
        
        prompt = f"""
        Analyze the following software requirement and break it down into:
        1. Functional Tasks (what needs to be done)
        2. Required Python Libraries
        3. Input/Output specifications
        4. Any constraints or considerations
        
        Requirement: {requirement}
        
        Respond in JSON format:
        {{
            "tasks": ["task1", "task2", ...],
            "libraries": ["library1", "library2", ...],
            "input_output": "description",
            "constraints": "any constraints"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            
            # Try to parse JSON
            try:
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
            except:
                result = self._parse_response(response_text)
            
            return result
        
        except Exception as e:
            print(f"Error in analysis: {str(e)}")
            return self._fallback_analysis(requirement)
    
    def _fallback_analysis(self, requirement: str) -> Dict:
        """Fallback analysis when API is not available"""
        
        keywords = requirement.lower()
        
        tasks = []
        libraries = []
        
        if "csv" in keywords:
            tasks.extend(["Read CSV file", "Parse data", "Process data"])
            libraries.append("pandas")
        
        if "json" in keywords:
            tasks.extend(["Read JSON file", "Parse JSON"])
            libraries.append("json")
        
        if "database" in keywords or "sql" in keywords:
            tasks.extend(["Connect to database", "Query data", "Store results"])
            libraries.append("sqlite3")
        
        if "plot" in keywords or "graph" in keywords or "visualiz" in keywords:
            tasks.extend(["Visualize data", "Create chart"])
            libraries.append("matplotlib")
        
        if "file" in keywords:
            tasks.extend(["Read file", "Write file", "Handle errors"])
            libraries.append("os")
        
        if not tasks:
            tasks = ["Understand requirement", "Design solution", "Implement code", "Test implementation"]
        
        libraries = list(set(["os", "sys"] + libraries))
        
        return {
            "tasks": tasks,
            "libraries": libraries,
            "input_output": "Input: User provided data or files. Output: Processed results",
            "constraints": "Must be efficient and handle edge cases"
        }
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse response when JSON extraction fails"""
        
        lines = response_text.split('\n')
        tasks = []
        libraries = []
        
        for line in lines:
            if any(indicator in line for indicator in ['task', 'step', '1.', '2.', '3.']):
                line = line.strip().lstrip('0123456789.-) ')
                if line and len(line) > 5:
                    tasks.append(line)
            
            if any(lib in line.lower() for lib in ['import', 'library', 'require', 'pandas', 'numpy', 'matplotlib']):
                words = line.split()
                for word in words:
                    if any(lib in word.lower() for lib in ['pandas', 'numpy', 'matplotlib', 'sqlite', 'json', 'csv']):
                        libraries.append(word.lower())
        
        if not tasks:
            tasks = ["Understand requirement", "Implement solution"]
        
        libraries = list(set(libraries)) if libraries else ["os"]
        
        return {
            "tasks": tasks[:5],
            "libraries": libraries[:5],
            "input_output": "Input: User data. Output: Processed results",
            "constraints": "Standard constraints apply"
        }
