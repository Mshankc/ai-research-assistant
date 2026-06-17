"""
Streamlit UI for the AI Research Assistant.
This creates a beautiful, professional web interface.
Run with: streamlit run app.py
"""
import streamlit as st
import os
import time
from dotenv import load_dotenv

load_dotenv()

from src.graph import build_research_graph

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS for State-of-the-Art Premium Look ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@400;500;600&display=swap');
    
    /* Global Styles */
    .stApp {
        background: #0B0E14; /* Deep, rich dark background */
        background-image: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,0.1) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,0.1) 0, transparent 50%);
        font-family: 'Inter', sans-serif;
        color: #E2E8F0;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #60A5FA, #A78BFA, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }

    /* Glassmorphic Agent Cards */
    .agent-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .agent-card:hover {
        transform: translateY(-4px);
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(167, 139, 250, 0.3);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.04), 0 0 15px rgba(167, 139, 250, 0.15);
    }
    
    .agent-icon {
        font-size: 2rem;
        margin-bottom: 12px;
        display: inline-block;
        padding: 12px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .agent-card h4 {
        color: #F8FAFC;
        margin-bottom: 8px;
        font-size: 1.25rem;
    }
    
    .agent-card p {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Streamlit Overrides */
    
    /* Search Bar Input */
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #F8FAFC !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2), 0 4px 20px rgba(0,0,0,0.2) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
        background: linear-gradient(135deg, #9333EA 0%, #2563EB 100%) !important;
    }
    
    /* Status Dashboard */
    .status-container {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        margin-top: 20px;
    }
    
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        padding: 12px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .step-item:last-child {
        border-bottom: none;
    }
    
    .step-icon {
        font-size: 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .step-content {
        flex-grow: 1;
    }
    
    .step-title {
        font-weight: 600;
        color: #F8FAFC;
        margin-bottom: 4px;
        font-family: 'Outfit', sans-serif;
    }
    
    .step-desc {
        color: #94A3B8;
        font-size: 0.9rem;
    }
    
    /* Markdown Report Container */
    .report-container {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 40px;
        margin-top: 30px;
        font-size: 1.05rem;
        line-height: 1.7;
    }
    
    .report-container h1, .report-container h2, .report-container h3 {
        color: #F8FAFC !important;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    
    .report-container a {
        color: #60A5FA;
        text-decoration: none;
    }
    
    .report-container a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("<div style='text-align: center; padding: 40px 0;'>", unsafe_allow_html=True)
st.markdown("<h1 style='font-size: 3.5rem; margin-bottom: 0;'><span class='gradient-text'>AI Research Assistant</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.2rem; color: #94A3B8; margin-top: 10px;'>Autonomous multi-agent research powered by LangGraph & Gemini</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Agent Capabilities ---
st.markdown("<h3 style='margin-bottom: 20px;'>The Research Team</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="agent-card">
        <div class="agent-icon">🔍</div>
        <h4>Research Agent</h4>
        <p>Scours the web autonomously using the Tavily API to gather up-to-date, highly relevant data and sources.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <div class="agent-icon">✍️</div>
        <h4>Writer Agent</h4>
        <p>Synthesizes raw data into a structured, highly polished markdown report highlighting key insights.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card">
        <div class="agent-icon">🧐</div>
        <h4>Critic Agent</h4>
        <p>Critiques the draft for accuracy and completeness, demanding revisions until the report is flawless.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# --- Main Interaction Area ---
st.markdown("### Start a Mission")
input_col, btn_col = st.columns([4, 1], vertical_alignment="bottom")

with input_col:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g., The implications of quantum computing on cryptography by 2030...",
        label_visibility="collapsed"
    )

with btn_col:
    start_btn = st.button("🚀 Initialize Agents")

# --- Execution Logic ---
if start_btn:
    if not topic:
        st.error("⚠️ Please enter a research topic to begin.")
    else:
        # Build the graph
        graph = build_research_graph()
        
        # Initial state
        initial_state = {
            "topic": topic,
            "messages": [],
            "research_data": "",
            "draft_report": "",
            "critic_feedback": "",
            "final_report": "",
            "revision_count": 0,
            "is_approved": False,
        }
        
        st.markdown("<h3 style='margin-top: 40px;'>Live Telemetry</h3>", unsafe_allow_html=True)
        
        # Placeholder for dynamic UI
        dashboard_placeholder = st.empty()
        
        # This list will accumulate HTML strings for each step
        dashboard_html_items = []
        
        def render_dashboard(items, is_loading=True):
            html = '<div class="status-container">\n'
            for item in items:
                html += item + "\n"
            if is_loading:
                html += '''<div class="step-item">
    <div class="step-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>
                .spinner { transform-origin: center; animation: spin 1s linear infinite; }
                @keyframes spin { 100% { transform: rotate(360deg); } }
            </style>
            <circle class="spinner" cx="12" cy="12" r="10" stroke="#8B5CF6" stroke-width="3" stroke-dasharray="31.4 31.4" stroke-linecap="round"/>
        </svg>
    </div>
    <div class="step-content">
        <div class="step-title" style="color: #8B5CF6;">Agents Computing...</div>
        <div class="step-desc">Processing current task in the background.</div>
    </div>
</div>'''
            html += '\n</div>'
            dashboard_placeholder.markdown(html, unsafe_allow_html=True)

        # Initial render
        render_dashboard(dashboard_html_items, is_loading=True)
        
        # Stream the graph execution
        current_state = initial_state.copy()
        for step in graph.stream(initial_state):
            for node_name, node_output in step.items():
                # Update our running state
                current_state.update(node_output)
                
                if node_name == "research":
                    dashboard_html_items.append('''<div class="step-item">
    <div class="step-icon">🔍</div>
    <div class="step-content">
        <div class="step-title">Research Agent Complete</div>
        <div class="step-desc">Successfully gathered source materials and structured data from the web.</div>
    </div>
</div>''')
                
                elif node_name == "write":
                    rev = node_output.get("revision_count", 1)
                    dashboard_html_items.append(f'''<div class="step-item">
    <div class="step-icon">✍️</div>
    <div class="step-content">
        <div class="step-title">Writer Agent Complete (Draft v{rev})</div>
        <div class="step-desc">Synthesized data into a comprehensive markdown report draft.</div>
    </div>
</div>''')
                
                elif node_name == "critique":
                    is_approved = node_output.get("is_approved", False)
                    if is_approved:
                        dashboard_html_items.append('''<div class="step-item">
    <div class="step-icon">✅</div>
    <div class="step-content">
        <div class="step-title" style="color: #4ADE80;">Critic Agent Approved</div>
        <div class="step-desc">The draft meets all quality standards and has been approved for release.</div>
    </div>
</div>''')
                    else:
                        dashboard_html_items.append('''<div class="step-item">
    <div class="step-icon">🔄</div>
    <div class="step-content">
        <div class="step-title" style="color: #FBBF24;">Critic Agent Rejected</div>
        <div class="step-desc">Deficiencies found. Sending back to Writer Agent for revision.</div>
    </div>
</div>''')
                        
                # Update UI immediately after each step
                render_dashboard(dashboard_html_items, is_loading=True)
                
        # Final render (remove loader)
        render_dashboard(dashboard_html_items, is_loading=False)
        st.success("✨ Mission Accomplished!")
        
        # Display the final report
        report_content = current_state.get("draft_report", "No report generated.")
        
        st.markdown("<h3 style='margin-top: 40px;'>Final Intelligence Report</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='report-container'>\n\n{report_content}\n\n</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        dl_col1, dl_col2, dl_col3 = st.columns([1, 2, 1])
        with dl_col2:
            st.download_button(
                label="📥 Download Mission Brief (.md)",
                data=str(report_content),
                file_name=f"intel_report_{topic.replace(' ', '_')[:20]}.md",
                mime="text/markdown",
                use_container_width=True
            )

# --- Footer ---
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #475569; font-size: 0.9rem;'>Developed with LangGraph, Ollama, and Streamlit</p>",
    unsafe_allow_html=True,
)