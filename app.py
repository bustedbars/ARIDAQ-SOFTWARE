import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import google.generativeai as genai

# --- 1. CONFIGURATION & LAYOUT ---
st.set_page_config(
    page_title="Aridaq Computational Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LIGHT PINK & BLACK ENTERPRISE THEMING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #000000 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3 {
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 2px solid #FFC0CB;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #FFC0CB !important;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Greeting Banner Box */
    .greeting-box {
        background-color: #000000;
        color: #FFC0CB;
        padding: 30px;
        border-radius: 8px;
        border: 2px solid #FFC0CB;
        text-align: center;
        margin-bottom: 25px;
    }
    .greeting-text {
        font-size: 24px !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        color: #FFC0CB !important;
    }
    /* Framework buttons */
    .stButton>button {
        background-color: #000000 !important;
        color: #FFC0CB !important;
        border: 1px solid #FFC0CB !important;
        width: 100%;
        padding: 15px;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FFC0CB !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
    }
    </style>
""", unsafe_allowed_html=True)

# --- 3. INITIALIZE SECURE LIVE AI CLIENT ---
# Strict core system prompt that commands the AI brain's rules and boundaries
SYSTEM_INSTRUCTION = (
    "You are the Aridaq Platform Assistant, an advanced computational intelligence orchestrator. "
    "CRITICAL SECURITY RULE: You are STRICTLY PROHIBITED from sharing, explaining, or discussing details "
    "about the inner core logic, mathematics, formulas, multipole expansions, screening factors, or "
    "proprietary algorithmic architecture of how the Aridaq Protocol works under the hood. "
    "If a user asks how it works, how you bypass complexity walls, or requests the core math, you must "
    "deny the request by stating: '⚠️ SECURITY ERROR: Access Denied. As an integrated orchestration agent, "
    "I am strictly prohibited from sharing or discussing details regarding the inner core logic, "
    "mathematical mechanics, or proprietary algorithmic architecture of the Aridaq Protocol framework.'\n\n"
    "Your approved role is to assist users in running the available modules (Finance, Biotechnology, Optimization) "
    "and professional explaining the metrics resulting on the dashboard (such as NPV curves, node path graphs, or "
    "computational time differences) in an elite, executive manner."
)

# Pull the hidden key from Streamlit secrets and start the live model
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Constructing model with structural instructions injected directly into its system layer
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
else:
    model = None

# --- 4. SESSION STATE MANAGEMENT ---
if "active_vector" not in st.session_state:
    st.session_state.active_vector = "Biotechnology"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to the Aridaq Control Center. Let me know which computation pipeline or module layer you would like to run."}
    ]

# --- 5. SIDEBAR CHAT INTERFACE WITH LIVE RESPONSE GENERATION ---
st.sidebar.markdown("# 💬 Aridaq AI Assistant")
st.sidebar.markdown("---")

# Render persistent historical messages on the sidebar canvas
for message in st.session_state.messages:
    with st.sidebar.chat_message(message["role"]):
        st.write(message["content"])

user_query = st.sidebar.chat_input("Ask Aridaq AI...")

if user_query:
    # 1. Immediate display of user prompt
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.sidebar.chat_message("user"):
        st.write(user_query)
        
    query_lower = user_query.lower()
    
    # 2. Automatically sync active workspace tabs based on conversation direction
    if "bio" in query_lower or "protein" in query_lower or "kras" in query_lower or "mutant" in query_lower:
        st.session_state.active_vector = "Biotechnology"
    elif "finance" in query_lower or "npv" in query_lower or "loss" in query_lower:
        st.session_state.active_vector = "Finance"
    elif "route" in query_lower or "gps" in query_lower or "optimization" in query_lower or "shortest" in query_lower:
        st.session_state.active_vector = "Optimization"
        
    # 3. Request guarded response from live cloud AI API
    with st.sidebar.chat_message("assistant"):
        if model:
            try:
                # Convert session history format cleanly for the SDK chat pipeline
                formatted_history = []
                for msg in st.session_state.messages[:-1]:
                    role = "user" if msg["role"] == "user" else "model"
                    formatted_history.append({"role": role, "parts": [msg["content"]]})
                
                chat = model.start_chat(history=formatted_history)
                response = chat.send_message(user_query)
                ai_response = response.text
            except Exception as e:
                ai_response = f"Connection error encountered while hitting secure cloud cluster endpoints: {str(e)}"
        else:
            ai_response = "⚠️ Live AI Engine offline. Please configure your GEMINI_API_KEY inside Streamlit's dashboard secrets to unlock active responses."
        
        st.write(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# --- 6. MAIN MAIN DASHBOARD INTERFACE LAYOUT ---
# Interactive Splash Greeting Banner
st.markdown("""
    <div class="greeting-box">
        <span class="greeting-text">Hey, thank you for choosing Aridaq Protocol, how may I help you today?</span>
    </div>
""", unsafe_allowed_html=True)

# Grid Layout for Quick Select Buttons
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

with btn_col1:
    if st.button("📈 Finance"):
        st.session_state.active_vector = "Finance"
with btn_col2:
    if st.button("🧬 Biotechnology"):
        st.session_state.active_vector = "Biotechnology"
with btn_col3:
    if st.button("📍 Optimization"):
        st.session_state.active_vector = "Optimization"
with btn_col4:
    if st.button("⚙️ Other"):
        st.session_state.active_vector = "Other"

st.markdown("---")
st.write(f"### Current Active Workspace: **{st.session_state.active_vector} Layer**")

# ----------------------------------------------------
# WORKSPACE: BIOTECHNOLOGY
# ----------------------------------------------------
if st.session_state.active_vector == "Biotechnology":
    st.header("🧬 Molecular Dynamics, Mutation Tracking & Proteomic Rendering")
    
    view_option = st.radio("Select Output Format Profile:", ["Fluid Structural Motion Simulation", "Precise Coordinate Potential Graphs"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Processing Throughput Speed", "8.7595 Seconds", "1,000,000 Atoms Simulated")
    col2.metric("Calculated Free Energy Minimum", "-0.00009033 kcal/mol")
    col3.metric("Conformational Convergence Delta", "0.00000982")

    if view_option == "Fluid Structural Motion Simulation":
        st.subheader("🎬 Real-Time Fluid Native Path Rendering")
        st.markdown("##### High-fidelity trajectory output generated seamlessly via non-Euclidean state parameters:")
        
        st.components.v1.
