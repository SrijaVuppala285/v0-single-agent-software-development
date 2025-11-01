import os
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

class LangChainIntegration:
    """Handles LLM interactions using LangChain"""
    
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY", "")
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=0.7
        ) if api_key else None
        
        self.memory = ConversationBufferMemory()
    
    def analyze_requirement_with_langchain(self, requirement: str) -> Dict:
        """Use LangChain to analyze requirements"""
        
        if not self.llm:
            return self._fallback_analysis(requirement)
        
        template = """
        You are an expert software architect. Analyze the following requirement and provide:
        1. Functional Tasks (list each task)
        2. Required Python Libraries
        3. Input/Output specifications
        4. Potential risks and constraints
        
        Requirement: {requirement}
        
        Provide a structured analysis in JSON format.
        """
        
        prompt = PromptTemplate(
            input_variables=["requirement"],
            template=template
        )
        
        try:
            chain = LLMChain(llm=self.llm, prompt=prompt, memory=self.memory)
            response = chain.run(requirement=requirement)
            
            # Parse response
            import json
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except Exception as e:
            print(f"LangChain error: {str(e)}")
        
        return self._fallback_analysis(requirement)
    
    def generate_code_with_langchain(self, analysis: Dict) -> str:
        """Use LangChain to generate code"""
        
        if not self.llm:
            return "# Generated code placeholder"
        
        tasks = ", ".join(analysis.get("tasks", []))
        libraries = ", ".join(analysis.get("libraries", []))
        
        template = """
        Generate production-ready Python code for the following tasks:
        
        Tasks: {tasks}
        Required Libraries: {libraries}
        
        Requirements:
        - Include proper error handling
        - Add docstrings and comments
        - Follow PEP 8 style guide
        - Include main function
        
        Code:
        """
        
        prompt = PromptTemplate(
            input_variables=["tasks", "libraries"],
            template=template
        )
        
        try:
            chain = LLMChain(llm=self.llm, prompt=prompt)
            code = chain.run(tasks=tasks, libraries=libraries)
            return code
        except Exception as e:
            print(f"Code generation error: {str(e)}")
            return "# Code generation failed"
    
    def review_code_with_langchain(self, code: str, test_results: Dict) -> Dict:
        """Use LangChain for code review"""
        
        if not self.llm:
            return {"summary": "Review pending", "improvements": []}
        
        template = """
        Review the following Python code and provide improvements:
        
        Code:
        {code}
        
        Test Results: {test_results}
        
        Provide:
        1. Code quality assessment
        2. Specific improvements
        3. Performance optimization suggestions
        4. Security considerations
        """
        
        prompt = PromptTemplate(
            input_variables=["code", "test_results"],
            template=template
        )
        
        try:
            chain = LLMChain(llm=self.llm, prompt=prompt)
            review = chain.run(code=code, test_results=str(test_results))
            
            return {
                "summary": review,
                "improvements": self._extract_improvements(review)
            }
        except Exception as e:
            print(f"Review error: {str(e)}")
            return {"summary": "Review failed", "improvements": []}
    
    def _extract_improvements(self, review_text: str) -> List[str]:
        """Extract improvements from review text"""
        improvements = []
        lines = review_text.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['improve', 'optimize', 'add', 'fix', 'remove']):
                line = line.strip()
                if len(line) > 10:
                    improvements.append(line)
        return improvements[:5]
    
    def _fallback_analysis(self, requirement: str) -> Dict:
        """Fallback analysis"""
        return {
            "tasks": ["Analyze requirement", "Plan solution", "Implement code"],
            "libraries": ["os", "sys"],
            "input_output": "Standard I/O",
            "constraints": "None"
        }
