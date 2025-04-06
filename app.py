
import streamlit as st
import random
import time
import os

# إعداد الصفحة
st.set_page_config(page_title="Note Reading Trainer (G Clef)", layout="centered")

# اختيار اللغة
if "language" not in st.session_state:
    st.session_state.language = None

if st.session_state.language is None:
    st.image("Logo.PNG", width=150)
    st.markdown("## Welcome | مرحباً بك")
    lang = st.radio("Choose Language | اختر اللغة", ["English", "العربية"])
    if st.button("Start | ابدأ"):
        st.session_state.language = lang
        st.rerun()
else:
    lang = st.session_state.language
    is_ar = lang == "العربية"

    st.image("Logo.PNG", width=150)
    st.title("مدرب قراءة النوتات (مفتاح صول)" if is_ar else "Note Reading Trainer (G Clef)")

    notes = [
        ('E', 'Mi'), ('F', 'Fa'), ('G', 'Sol'), ('A', 'La'),
        ('B', 'Si'), ('C', 'Do'), ('D', 'Re'), ('E2', 'Mi'),
        ('F2', 'Fa')
    ]

    note_positions = {
        'E': 0, 'F': 0.5, 'G': 1, 'A': 1.5,
        'B': 2, 'C': 2.5, 'D': 3, 'E2': 3.5,
        'F2': 4
    }
