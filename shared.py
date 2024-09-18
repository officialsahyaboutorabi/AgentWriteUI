# shared.py

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_selected_provider():
    return st.session_state.get('last_inputs', {}).get('llm_provider', '')

def get_selected_model_name():
    return st.session_state.get('last_inputs', {}).get('llm_model', '')

def get_numberofwords():
    return st.session_state.get('num_words', {}).get('num_words', '')

def get_uploaded_file():
    return st.session_state.get('uploaded_file')

def get_image():
    return st.session_state.get('uploaded_image')
