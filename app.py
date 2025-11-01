import streamlit as st
import os
import json
import sqlite3
import zipfile
import io
from datetime import datetime
from pathlib import Path
from modules.requirement_analyzer import RequirementAnalyzer
from modules.code_generator import CodeGenerator
from modules.test_runner import TestRunner
from modules.reviewer import Reviewer
from modules.storage import ProjectStorage
from modules.chat_manager import ChatManager
from modules.file_manager import FileManager
from modules.langchain_integration import LangChainIntegration

# Configure Streamlit
st.set_page_config(
    page_title="SASDS - AI Software Development",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

chat_manager = ChatManager()
file_manager = FileManager()
langchain = LangChainIntegration()

# Initialize session state
if "current_project" not in st.session_state:
    st.session_state.current_project = None
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "generated_code" not in st.session_state:
    st.session_state.generated_code = None
if "test_results" not in st.session_state:
    st.session_state.test_results = None
if "review_report" not in st.session_state:
    st.session_state.review_report = None

# Initialize modules
storage = ProjectStorage()
analyzer = RequirementAnalyzer()
generator = CodeGenerator()
tester = TestRunner()
reviewer = Reviewer()

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        background-color: #0a0e27;
        color: #e0e0e0;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    .task-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
        margin: 10px 0;
    }
    .success-box {
        background-color: #1a3a2a;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00ff88;
    }
    .error-box {
        background-color: #3a1a1a;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff3333;
    }
</style>
""", unsafe_allow_html=True)

def render_header():
    """Render the main header"""
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("## 🚀 SASDS")
    with col2:
        st.markdown("### Single Agent Software Development System")
    st.markdown("---")
    st.markdown("**Build, test, and refine software automatically using AI powered by Google Gemini**")

def render_sidebar_chat_history():
    """Render chat history sidebar (ChatGPT-like interface)"""
    with st.sidebar:
        st.markdown("## 💬 Chat History")
        
        # New chat button
        if st.button("➕ New Chat", use_container_width=True):
            session_id = chat_manager.create_session("New Chat")
            st.session_state.current_session_id = session_id
            st.session_state.analysis_result = None
            st.session_state.generated_code = None
            st.rerun()
        
        st.markdown("---")
        
        try:
            sessions = chat_manager.get_all_sessions()
            
            if sessions:
                for session in sessions:
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        if st.button(
                            f"💭 {session['title'][:30]}",
                            use_container_width=True,
                            key=f"session_{session['id']}"
                        ):
                            st.session_state.current_session_id = session['id']
                            st.rerun()
                    
                    with col2:
                        if st.button("🗑️", key=f"del_session_{session['id']}"):
                            chat_manager.delete_session(session['id'])
                            if st.session_state.current_session_id == session['id']:
                                st.session_state.current_session_id = None
                            st.rerun()
            else:
                st.info("No chat history yet")
        except Exception as e:
            st.error(f"Error loading chat history: {str(e)}")
            st.info("Try refreshing the page or clearing browser cache")

def render_chat_interface():
    """Render ChatGPT-like chat interface"""
    
    if not st.session_state.current_session_id:
        st.session_state.current_session_id = chat_manager.create_session("New Chat")
    
    # Display chat messages
    try:
        messages = chat_manager.get_session_messages(st.session_state.current_session_id)
        
        for msg in messages:
            with st.chat_message(msg['role']):
                st.write(msg['content'])
    except Exception as e:
        st.error(f"Error loading messages: {str(e)}")
        messages = []
    
    # Chat input
    if prompt := st.chat_input("Enter your requirement or ask a question..."):
        try:
            # Add user message
            chat_manager.add_message(st.session_state.current_session_id, "user", prompt)
            
            # Get AI response
            with st.spinner("Analyzing..."):
                analysis = langchain.analyze_requirement_with_langchain(prompt)
                st.session_state.analysis_result = analysis
                
                # Create response
                response_text = f"""
**Analysis Complete!**

**Tasks:**
{chr(10).join([f"- {task}" for task in analysis.get("tasks", [])])}

**Libraries:** {', '.join(analysis.get("libraries", []))}

**Constraints:** {analysis.get("constraints", "None")}
                """
                
                # Add assistant message
                chat_manager.add_message(st.session_state.current_session_id, "assistant", response_text)
                
                st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

def render_requirement_input():
    """Render requirement input section"""
    st.subheader("📦 New Project")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Enter Your Requirement:")
        requirement_text = st.text_area(
            "Type your software requirement here",
            placeholder="e.g., Build a program to analyze student marks from a CSV file",
            height=120,
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("#### Or Upload Requirement File:")
        uploaded_file = st.file_uploader(
            "Choose a file (TXT, PDF, DOCX, CSV, JSON, PY)",
            type=["txt", "pdf", "docx", "csv", "json", "py"],
            label_visibility="collapsed"
        )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        analyze_btn = st.button("🔍 Analyze Requirement", use_container_width=True, key="analyze_btn")
    with col2:
        clear_btn = st.button("❌ Clear", use_container_width=True, key="clear_btn")
    with col3:
        pass
    
    if clear_btn:
        st.session_state.analysis_result = None
        st.session_state.generated_code = None
        st.session_state.test_results = None
        st.session_state.review_report = None
        st.rerun()
    
    if analyze_btn:
        if not requirement_text and not uploaded_file:
            st.error("Please enter a requirement or upload a file")
            return
        
        input_text = requirement_text
        if uploaded_file:
            try:
                file_content = uploaded_file.getvalue()
                file_path = file_manager.save_uploaded_file(
                    st.session_state.current_project.get("id", 1) if st.session_state.current_project else 1,
                    file_content,
                    uploaded_file.name
                )
                input_text += f"\n\n[Uploaded file: {uploaded_file.name}]\n{file_content.decode('utf-8', errors='ignore')[:1000]}"
            except Exception as e:
                st.error(f"Error uploading file: {str(e)}")
        
        with st.spinner("Analyzing requirement..."):
            try:
                st.session_state.analysis_result = langchain.analyze_requirement_with_langchain(input_text)
                st.session_state.current_project = {
                    "title": "New Project",
                    "requirement": input_text[:200],
                    "created_at": datetime.now().isoformat(),
                    "version": 1
                }
                
                if st.session_state.current_session_id:
                    chat_manager.add_message(
                        st.session_state.current_session_id,
                        "user",
                        requirement_text[:500]
                    )
                    
                    response_msg = f"**Analysis Complete!**\n\nIdentified tasks: {', '.join(st.session_state.analysis_result.get('tasks', [])[:3])}"
                    chat_manager.add_message(
                        st.session_state.current_session_id,
                        "assistant",
                        response_msg
                    )
            except Exception as e:
                st.error(f"Error analyzing requirement: {str(e)}")
    
    return requirement_text, uploaded_file

def render_analysis_result():
    """Render analysis results"""
    if st.session_state.analysis_result:
        st.subheader("📊 Analysis Result")
        
        analysis = st.session_state.analysis_result
        
        st.markdown("#### Functional Tasks:")
        for i, task in enumerate(analysis.get("tasks", []), 1):
            st.markdown(f"<div class='task-box'><b>{i}. {task}</b></div>", unsafe_allow_html=True)
        
        if analysis.get("libraries"):
            st.markdown("#### Suggested Libraries:")
            st.write(", ".join(analysis["libraries"]))
        
        if analysis.get("constraints"):
            st.markdown("#### Constraints:")
            st.write(analysis["constraints"])
        
        st.markdown("---")

def render_code_generation():
    """Render code generation section"""
    if st.session_state.analysis_result:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⚙ Generate Code", use_container_width=True):
                with st.spinner("Generating code..."):
                    try:
                        st.session_state.generated_code = generator.generate(
                            st.session_state.analysis_result
                        )
                    except Exception as e:
                        st.error(f"Error generating code: {str(e)}")
        
        with col2:
            if st.session_state.generated_code and st.button("🧪 Run Tests", use_container_width=True):
                with st.spinner("Running tests..."):
                    try:
                        st.session_state.test_results = tester.run_tests(
                            st.session_state.generated_code
                        )
                    except Exception as e:
                        st.error(f"Error running tests: {str(e)}")
        
        with col3:
            if st.session_state.generated_code and st.button("🔁 Review & Refine", use_container_width=True):
                with st.spinner("Reviewing and refining..."):
                    try:
                        test_results = st.session_state.test_results or {
                            "passed": 0,
                            "failed": 0,
                            "success_rate": 0,
                            "log": "No tests run yet"
                        }
                        st.session_state.review_report = reviewer.review(
                            st.session_state.generated_code,
                            test_results
                        )
                    except Exception as e:
                        st.error(f"Error in review process: {str(e)}")

def render_output_console():
    """Render the output console"""
    st.subheader("💻 Output Console")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Generated Code", "Test Results", "Review Report", "All Files", "Download Package"])
    
    with tab1:
        if st.session_state.generated_code:
            st.code(st.session_state.generated_code, language="python")
            st.download_button(
                label="Download Code",
                data=st.session_state.generated_code,
                file_name="main.py",
                mime="text/plain"
            )
        else:
            st.info("Generated code will appear here")
    
    with tab2:
        if st.session_state.test_results is not None:
            results = st.session_state.test_results
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tests Passed", results.get("passed", 0))
            with col2:
                st.metric("Tests Failed", results.get("failed", 0))
            with col3:
                st.metric("Success Rate", f"{results.get('success_rate', 0):.1f}%")
            
            if results.get("failed", 0) > 0:
                st.markdown("<div class='error-box'>", unsafe_allow_html=True)
                st.write("**Failed Tests:**")
                st.write(results.get("failures", ""))
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='success-box'>", unsafe_allow_html=True)
                st.write("✅ All tests passed!")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.code(results.get("log", ""), language="text")
        else:
            st.info("Test results will appear here")
    
    with tab3:
        if st.session_state.review_report:
            report = st.session_state.review_report
            st.write(report.get("summary", ""))
            
            if report.get("improvements"):
                st.markdown("#### Improvements Made:")
                for improvement in report["improvements"]:
                    st.write(f"• {improvement}")
            
            if report.get("refined_code"):
                st.code(report["refined_code"], language="python")
                st.download_button(
                    label="Download Refined Code",
                    data=report["refined_code"],
                    file_name="main_refined.py",
                    mime="text/plain"
                )
        else:
            st.info("Review report will appear here")
    
    with tab4:
        if st.session_state.generated_code:
            files = {
                "main.py": st.session_state.generated_code,
                "test_main.py": f"# Generated test file\n# {st.session_state.test_results.get('log', 'Tests pending') if st.session_state.test_results else 'Tests pending'}",
            }
            
            if st.session_state.review_report:
                files["review_report.txt"] = st.session_state.review_report.get("summary", "")
            
            st.json(files)
        else:
            st.info("No files generated yet")
    
    with tab5:
        st.markdown("### Download Complete Project Package")
        st.markdown("Download all generated files, requirements, and configuration as a ZIP package.")
        
        if st.button("📦 Download Package", use_container_width=True):
            try:
                # Create ZIP file
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # Add main files
                    if st.session_state.generated_code:
                        zip_file.writestr("main.py", st.session_state.generated_code)
                    
                    if st.session_state.test_results:
                        test_log = st.session_state.test_results.get("log", "No tests run")
                        zip_file.writestr("test_results.txt", test_log)
                    
                    if st.session_state.review_report:
                        review_summary = st.session_state.review_report.get("summary", "")
                        zip_file.writestr("review_report.txt", review_summary)
                        
                        if st.session_state.review_report.get("refined_code"):
                            zip_file.writestr("main_refined.py", st.session_state.review_report["refined_code"])
                    
                    # Add requirements.txt
                    if st.session_state.analysis_result:
                        libraries = st.session_state.analysis_result.get("libraries", [])
                        requirements_content = "\n".join(libraries) + "\n"
                        zip_file.writestr("requirements.txt", requirements_content)
                    
                    # Add README.md
                    readme = """# Generated Project

## Overview
This is an auto-generated Python project using SASDS (Single Agent Software Development System).

## Files
- main.py - Main generated code
- main_refined.py - Refined version after review
- test_results.txt - Test execution results
- review_report.txt - Code review report
- requirements.txt - Python dependencies

## How to Run
1. Install dependencies: pip install -r requirements.txt
2. Run the project: python main.py
3. Run tests: pytest test_main.py

## Generated At
"""
                    readme += f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    zip_file.writestr("README.md", readme)
                    
                    # Add .gitignore
                    gitignore = """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
venv/
"""
                    zip_file.writestr(".gitignore", gitignore)
                    
                    # Add project metadata
                    metadata = {
                        "generated_at": datetime.now().isoformat(),
                        "analysis": st.session_state.analysis_result or {},
                        "test_summary": {
                            "passed": st.session_state.test_results.get("passed", 0) if st.session_state.test_results else 0,
                            "failed": st.session_state.test_results.get("failed", 0) if st.session_state.test_results else 0,
                        }
                    }
                    zip_file.writestr("project_metadata.json", json.dumps(metadata, indent=2))
                
                # Download button
                zip_buffer.seek(0)
                st.download_button(
                    label="Download ZIP Package",
                    data=zip_buffer.getvalue(),
                    file_name=f"sasds_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip"
                )
                st.success("Package ready for download!")
            
            except Exception as e:
                st.error(f"Error creating package: {str(e)}")
        else:
            st.info("Click 'Download Package' to create a ZIP file with all generated files.")

def render_recent_projects():
    """Render recent projects section"""
    st.subheader("📂 Recent Projects")
    
    try:
        projects = storage.get_recent_projects()
        
        if projects:
            for project in projects:
                with st.expander(f"{project['title']} (v{project['version']})"):
                    st.write(f"**Created:** {project['created_at']}")
                    st.write(f"**Requirement:** {project['requirement']}")
                    
                    if st.button(f"Open Project", key=f"project_{project['id']}"):
                        st.session_state.current_project = project
                        st.rerun()
        else:
            st.info("No projects yet. Create your first project!")
    except Exception as e:
        st.warning(f"Could not load recent projects: {str(e)}")

def main():
    """Main application"""
    render_sidebar_chat_history()
    
    render_header()
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_project = None
            st.rerun()
    
    st.markdown("---")
    
    view_mode = st.radio("View Mode:", ["Chat Interface", "Project Builder"], horizontal=True)
    
    if view_mode == "Chat Interface":
        render_chat_interface()
    else:
        # Main content
        render_requirement_input()
        render_analysis_result()
        
        if st.session_state.analysis_result:
            render_code_generation()
            st.markdown("---")
            render_output_console()
        
        st.markdown("---")
        render_recent_projects()

if __name__ == "__main__":
    main()
