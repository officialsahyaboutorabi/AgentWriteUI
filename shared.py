# shared.py

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_selected_provider():
    return st.session_state.get('last_inputs', {}).get('llm_provider', '')

def get_selected_model_name():
    return st.session_state.get('last_inputs', {}).get('llm_model', '')
