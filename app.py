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

# Initialize session state - MUST be done before any widget
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
if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New Chat"

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
    """Render chat history sidebar (ChatGPT-like interface) - FIXED: No st.rerun() in sidebar"""
    with st.sidebar:
        st.markdown("## 💬 Chat History")
        
        # New chat button - uses key to prevent duplicate rendering
        if st.button("➕ New Chat", use_container_width=True, key="new_chat_btn"):
            session_id = chat_manager.create_session("New Chat")
            st.session_state.current_session_id = session_id
            st.session_state.chat_title = "New Chat"
            st.session_state.analysis_result = None
            st.session_state.generated_code = None
        
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
                            st.session_state.chat_title = session['title']
                    
                    with col2:
                        if st.button("🗑️", key=f"del_session_{session['id']}"):
                            chat_manager.delete_session(session['id'])
                            if st.session_state.current_session_id == session['id']:
                                st.session_state.current_session_id = None
                                st.session_state.chat_title = "New Chat"
            else:
                st.info("No chat history yet")
        except Exception as e:
            st.error(f"Error loading chat history: {str(e)}")
            st.info("Try refreshing the page")

def render_chat_interface():
    """Render ChatGPT-like chat interface"""
    
    # Initialize session if needed
    if not st.session_state.current_session_id:
        st.session_state.current_session_id = chat_manager.create_session("New Chat")
        st.session_state.chat_title = "New Chat"
    
    # Display chat title
    st.markdown(f"## 💬 {st.session_state.chat_title}")
    
    # Display chat messages
    try:
        messages = chat_manager.get_session_messages(st.session_state.current_session_id)
        
        for msg in messages:
            with st.chat_message(msg['role']):
                st.write(msg['content'])
    except Exception as e:
        st.warning(f"Could not load messages: {str(e)}")
        messages = []
    
    # Chat input
    if prompt := st.chat_input("Enter your requirement or ask a question..."):
        try:
            # Add user message to chat
            chat_manager.add_message(st.session_state.current_session_id, "user", prompt)
            
            # Get AI response
            with st.spinner("Analyzing..."):
                try:
                    analysis = langchain.analyze_requirement_with_langchain(prompt)
                    st.session_state.analysis_result = analysis
                    
                    # Create response
                    tasks_text = "\n".join([f"- {task}" for task in analysis.get("tasks", [])])
                    response_text = f"""**Analysis Complete!**

**Tasks:**
{tasks_text}

**Libraries:** {', '.join(analysis.get("libraries", [])) or "None"}

**Constraints:** {analysis.get("constraints", "None")}"""
                    
                    # Add assistant message
                    chat_manager.add_message(st.session_state.current_session_id, "assistant", response_text)
                    
                except Exception as analysis_error:
                    error_msg = f"Error during analysis: {str(analysis_error)}"
                    st.error(error_msg)
                    chat_manager.add_message(st.session_state.current_session_id, "assistant", error_msg)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

def render_requirement_input():
    """Render requirement input section with title input"""
    st.subheader("📦 New Project")
    
    col_title_1, col_title_2 = st.columns([1, 1])
    with col_title_1:
        st.markdown("#### Project Title:")
        project_title = st.text_input(
            "Give your project a name",
            placeholder="e.g., Student Grade Analyzer",
            label_visibility="collapsed",
            key="project_title_input"
        )
    
    with col_title_2:
        pass
    
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
                return
        
        with st.spinner("Analyzing requirement..."):
            try:
                st.session_state.analysis_result = langchain.analyze_requirement_with_langchain(input_text)
                
                final_title = project_title or "New Project"
                
                st.session_state.current_project = {
                    "title": final_title,
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
                    
                    response_msg = f"**Analysis Complete!**\n\nProject: **{final_title}**\n\nIdentified tasks: {', '.join(st.session_state.analysis_result.get('tasks', [])[:3])}"
                    chat_manager.add_message(
                        st.session_state.current_session_id,
                        "assistant",
                        response_msg
                    )
                    
                    # Update session title with project title
                    chat_manager.update_session_title(st.session_state.current_session_id, final_title)
                    st.session_state.chat_title = final_title
                
                st.success(f"✅ Analysis complete for: {final_title}")
            except Exception as e:
                st.error(f"Error analyzing requirement: {str(e)}")
    
    return requirement_text, uploaded_file, project_title

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
            if st.button("⚙️ Generate Code", use_container_width=True, key="gen_code_btn"):
                with st.spinner("Generating code..."):
                    try:
                        st.session_state.generated_code = generator.generate(
                            st.session_state.analysis_result
                        )
                        st.success("✅ Code generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating code: {str(e)}")
        
        with col2:
            if st.session_state.generated_code and st.button("🧪 Run Tests", use_container_width=True, key="run_tests_btn"):
                with st.spinner("Generating and running tests..."):
                    try:
                        st.session_state.test_results = tester.run_tests(
                            st.session_state.generated_code
                        )
                        
                        # Display results immediately
                        test_res = st.session_state.test_results
                        if test_res:
                            st.success(f"✅ Tests Complete! Passed: {test_res.get('passed', 0)}, Failed: {test_res.get('failed', 0)}")
                        
                    except Exception as e:
                        st.error(f"Error running tests: {str(e)}")
                        st.session_state.test_results = {
                            "passed": 0,
                            "failed": 1,
                            "success_rate": 0,
                            "log": f"Error: {str(e)}",
                            "failures": str(e)
                        }
        
        with col3:
            if st.session_state.generated_code and st.button("🔁 Review & Refine", use_container_width=True, key="review_btn"):
                with st.spinner("Reviewing and refining code..."):
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
                        st.success("✅ Review complete!")
                    except Exception as e:
                        st.error(f"Error in review process: {str(e)}")

def render_output_console():
    """Render the output console with all tabs"""
    st.subheader("💻 Output Console")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Generated Code", "Test Results", "Review Report", "Code Output", "Download Package"])
    
    with tab1:
        if st.session_state.generated_code:
            st.code(st.session_state.generated_code, language="python")
            st.download_button(
                label="Download Code",
                data=st.session_state.generated_code,
                file_name="main.py",
                mime="text/plain",
                key="dl_main_code"
            )
        else:
            st.info("Generated code will appear here after clicking 'Generate Code'")
    
    with tab2:
        if st.session_state.test_results is not None and isinstance(st.session_state.test_results, dict):
            results = st.session_state.test_results
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tests Passed", results.get("passed", 0))
            with col2:
                st.metric("Tests Failed", results.get("failed", 0))
            with col3:
                success_rate = results.get("success_rate", 0)
                st.metric("Success Rate", f"{success_rate:.1f}%")
            
            st.markdown("---")
            
            if results.get("failed", 0) > 0:
                st.markdown("<div class='error-box'>", unsafe_allow_html=True)
                st.write("**Failed Tests:**")
                failures = results.get("failures", "")
                if failures:
                    st.write(failures)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='success-box'>", unsafe_allow_html=True)
                st.write("✅ All tests passed!")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("#### Test Log:")
            test_log = results.get("log", "")
            if test_log:
                st.code(test_log, language="text")
            else:
                st.info("No test log available")
        else:
            st.info("Test results will appear here after clicking 'Run Tests'")
    
    with tab3:
        if st.session_state.review_report:
            report = st.session_state.review_report
            
            if isinstance(report, dict):
                summary = report.get("summary", "")
                if summary:
                    st.write(summary)
                
                if report.get("improvements"):
                    st.markdown("#### Improvements Made:")
                    for improvement in report["improvements"]:
                        st.write(f"• {improvement}")
                
                if report.get("refined_code"):
                    st.markdown("#### Refined Code:")
                    st.code(report["refined_code"], language="python")
                    st.download_button(
                        label="Download Refined Code",
                        data=report["refined_code"],
                        file_name="main_refined.py",
                        mime="text/plain",
                        key="dl_refined_code"
                    )
            else:
                st.write(report)
        else:
            st.info("Review report will appear here after clicking 'Review & Refine'")
    
    with tab4:
        st.markdown("#### Program Output")
        
        if st.session_state.generated_code:
            if st.button("▶️ Run Code & Show Output", use_container_width=True, key="run_code_output"):
                with st.spinner("Executing code..."):
                    try:
                        import tempfile
                        import subprocess
                        
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                            f.write(st.session_state.generated_code)
                            f.flush()
                            temp_file = f.name
                        
                        result = subprocess.run(
                            ["python", temp_file],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        
                        os.unlink(temp_file)
                        
                        st.markdown("##### Output:")
                        if result.stdout:
                            st.code(result.stdout, language="text")
                        else:
                            st.info("No output generated")
                        
                        if result.stderr:
                            st.markdown("##### Errors/Warnings:")
                            st.code(result.stderr, language="text")
                    
                    except subprocess.TimeoutExpired:
                        st.error("❌ Code execution timed out (>10 seconds)")
                    except Exception as e:
                        st.error(f"❌ Error executing code: {str(e)}")
        else:
            st.info("Generate code first to see output")
    
    with tab5:
        st.markdown("### Download Complete Project Package")
        st.markdown("Download all generated files, requirements, and configuration as a ZIP package.")
        
        if st.button("📦 Download Package", use_container_width=True, key="download_pkg"):
            try:
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # Add main files
                    if st.session_state.generated_code:
                        zip_file.writestr("main.py", st.session_state.generated_code)
                    
                    if st.session_state.test_results and isinstance(st.session_state.test_results, dict):
                        test_log = st.session_state.test_results.get("log", "No tests run")
                        zip_file.writestr("test_results.txt", test_log)
                    
                    if st.session_state.review_report:
                        if isinstance(st.session_state.review_report, dict):
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
                    project_title = st.session_state.current_project.get("title", "Generated Project") if st.session_state.current_project else "Generated Project"
                    readme = f"""# {project_title}

## Overview
This is an auto-generated Python project using SASDS (Single Agent Software Development System).

## Files
- main.py - Main generated code
- main_refined.py - Refined version after review (if available)
- test_results.txt - Test execution results
- review_report.txt - Code review report
- requirements.txt - Python dependencies

## How to Run
1. Install dependencies: pip install -r requirements.txt
2. Run the project: python main.py
3. Run tests: pytest test_main.py

## Generated At
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
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
                        "project_title": project_title,
                        "generated_at": datetime.now().isoformat(),
                        "analysis": st.session_state.analysis_result or {},
                        "test_summary": {
                            "passed": st.session_state.test_results.get("passed", 0) if st.session_state.test_results and isinstance(st.session_state.test_results, dict) else 0,
                            "failed": st.session_state.test_results.get("failed", 0) if st.session_state.test_results and isinstance(st.session_state.test_results, dict) else 0,
                        }
                    }
                    zip_file.writestr("project_metadata.json", json.dumps(metadata, indent=2))
                
                zip_buffer.seek(0)
                st.download_button(
                    label="📥 Download ZIP Package",
                    data=zip_buffer.getvalue(),
                    file_name=f"sasds_{project_title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    key="download_zip"
                )
                st.success("✅ Package ready for download!")
            
            except Exception as e:
                st.error(f"Error creating package: {str(e)}")

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
        if st.button("🏠 Home", use_container_width=True, key="home_btn"):
            st.session_state.current_project = None
    
    st.markdown("---")
    
    view_mode = st.radio("View Mode:", ["Chat Interface", "Project Builder"], horizontal=True, key="view_mode_radio")
    
    if view_mode == "Chat Interface":
        render_chat_interface()
    else:
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
