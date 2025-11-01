import os
from typing import Dict
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class Reviewer:
    """Reviews and refines generated code"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-pro") if GEMINI_API_KEY else None
    
    def review(self, code: str, test_results: Dict) -> Dict:
        """
        Review code and suggest improvements
        
        Args:
            code: Generated code
            test_results: Results from test runner
            
        Returns:
            Dictionary with review report and refined code
        """
        
        if not self.model:
            return self._generate_review_template(code, test_results)
        
        test_info = f"Tests Passed: {test_results.get('passed', 0)}, Failed: {test_results.get('failed', 0)}"
        
        prompt = f"""
        Review this Python code and provide:
        1. Code quality assessment
        2. Performance improvements
        3. Bug fixes if needed
        4. Best practices recommendations
        5. Security considerations
        
        Current test status: {test_info}
        
        Code:
        {code}
        
        Provide a review report and then generate an improved version of the code.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Split review and code
            parts = response_text.split("```")
            
            summary = parts[0] if parts else response_text
            refined_code = parts[1] if len(parts) > 1 else code
            
            if refined_code.startswith("python"):
                refined_code = refined_code[6:]
            
            return {
                "summary": summary,
                "improvements": self._extract_improvements(summary),
                "refined_code": refined_code.strip(),
                "status": "reviewed"
            }
        
        except Exception as e:
            print(f"Error in review: {str(e)}")
            return self._generate_review_template(code, test_results)
    
    def _generate_review_template(self, code: str, test_results: Dict) -> Dict:
        """Generate template review when API is not available"""
        
        improvements = [
            "Add comprehensive error handling",
            "Include type hints for better code clarity",
            "Add docstrings to all functions",
            "Implement input validation",
            "Consider edge cases",
            "Add logging for debugging"
        ]
        
        if test_results.get("failed", 0) > 0:
            improvements.insert(0, "Fix failing test cases")
        
        summary = f"""
        Code Review Report
        ==================
        
        Test Results: {test_results.get('passed', 0)} passed, {test_results.get('failed', 0)} failed
        
        Recommendations:
        {chr(10).join([f"- {imp}" for imp in improvements[:3]])}
        """
        
        return {
            "summary": summary,
            "improvements": improvements[:3],
            "refined_code": code,
            "status": "reviewed"
        }
    
    def _extract_improvements(self, text: str) -> list:
        """Extract improvement points from review text"""
        
        lines = text.split('\n')
        improvements = []
        
        for line in lines:
            if any(indicator in line for indicator in ['-', '•', '*', '1.', '2.', '3.']):
                line = line.strip().lstrip('-•*123456789. ')
                if len(line) > 10:
                    improvements.append(line)
        
        return improvements[:5]
