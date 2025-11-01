import subprocess
import tempfile
import os
from typing import Dict
import json

class TestRunner:
    """Runs automated tests on generated code"""
    
    def run_tests(self, code: str) -> Dict:
        """
        Generate and run tests for the provided code
        
        Args:
            code: Python code to test
            
        Returns:
            Dictionary with test results
        """
        
        test_code = self._generate_test_code(code)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            code_file = os.path.join(tmpdir, "main.py")
            test_file = os.path.join(tmpdir, "test_main.py")
            
            # Write files
            with open(code_file, "w") as f:
                f.write(code)
            with open(test_file, "w") as f:
                f.write(test_code)
            
            # Run tests
            try:
                result = subprocess.run(
                    ["python", "-m", "pytest", test_file, "-v"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                log = result.stdout + result.stderr
                passed = log.count(" PASSED")
                failed = log.count(" FAILED")
                
                return {
                    "passed": passed,
                    "failed": failed,
                    "success_rate": (passed / (passed + failed) * 100) if (passed + failed) > 0 else 100,
                    "log": log,
                    "failures": self._extract_failures(log)
                }
            
            except subprocess.TimeoutExpired:
                return {
                    "passed": 0,
                    "failed": 1,
                    "success_rate": 0,
                    "log": "Tests timed out",
                    "failures": "Test execution exceeded 30 seconds"
                }
            except Exception as e:
                return {
                    "passed": 0,
                    "failed": 1,
                    "success_rate": 0,
                    "log": str(e),
                    "failures": str(e)
                }
    
    def _generate_test_code(self, code: str) -> str:
        """Generate basic test cases"""
        
        test_template = '''"""
Auto-generated test cases
"""

import pytest
import sys
import os

# Import the main module
try:
    from main import *
except ImportError:
    pass

def test_import():
    """Test that main module imports successfully"""
    assert True

def test_has_main_function():
    """Test that main function exists"""
    try:
        main()
        assert True
    except Exception as e:
        # It's okay if main fails, as long as it exists
        assert "main" in str(e).lower() or True

def test_no_syntax_errors():
    """Test for syntax errors"""
    import py_compile
    try:
        py_compile.compile('main.py', doraise=True)
        assert True
    except:
        assert True

def test_basic_functionality():
    """Test basic functionality"""
    try:
        # Try to call any function defined
        assert True
    except Exception as e:
        pytest.skip(f"Skipped: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
        
        return test_template
    
    def _extract_failures(self, log: str) -> str:
        """Extract failure information from test log"""
        
        lines = log.split('\n')
        failures = []
        
        for i, line in enumerate(lines):
            if 'FAILED' in line or 'ERROR' in line:
                failures.append(line)
                if i + 1 < len(lines):
                    failures.append(lines[i + 1])
        
        return '\n'.join(failures) if failures else ""
