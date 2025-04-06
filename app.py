
import streamlit as st
import random
import time
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="Note Reading Trainer", layout="centered")

# تحديد حالة الجلسة
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "language" not in st.session_state:
    st.session_state.language = "en"

# القاموس اللغوي
texts = {
    "en": {
        "welcome": "Welcome",
        "choose_language": "Choose Language",
        "start": "Start",
        "round": "Round",
        "choose_note": "Choose the correct note name:",
        "correct": "Correct!",
        "incorrect": "Incorrect! The correct answer was",
    },
    "ar": {
        "welcome": "مرحباً بك",
        "choose_language": "اختر اللغة",
        "start": "ابدأ",
        "round": "الجولة",
        "choose_note": "اختر اسم النغمة الصحيحة:",
        "correct": "إجابة صحيحة!",
        "incorrect": "إجابة خاطئة! الجواب الصحيح هو",
    }
}

# واجهة البداية
if st.session_state.page == "welcome":
    st.image("Logo.PNG", width=150)
    st.markdown(f"## {texts['en']['welcome']} | {texts['ar']['welcome']}")
    language = st.radio(f"{texts['en']['choose_language']} | {texts['ar']['choose_language']}",
                        ["en", "ar"], index=0)
    if st.button(f"{texts['en']['start']} | {texts['ar']['start']}"):
        st.session_state.language = language
        st.session_state.page = "main"
        st.rerun()

# التطبيق الأساسي
elif st.session_state.page == "main":
    lang = st.session_state.language
    t = texts[lang]

    notes = [
        ('E', 'Mi'), ('F', 'Fa'), ('G', 'Sol'),
        ('A', 'La'), ('B', 'Si'), ('C', 'Do'),
        ('D', 'Re'), ('E2', 'Mi'), ('F2', 'Fa')
    ]

    note_positions = {
        'E': 0, 'F': 0.5, 'G': 1, 'A': 1.5,
        'B': 2, 'C': 2.5, 'D': 3, 'E2': 3.5, 'F2': 4
    }

    if "round" not in st.session_state:
        st.session_state.round = 1
        st.session_state.score = 0
        st.session_state.total = 0

    st.image("Logo.PNG", width=150)
    st.radio(t['choose_note'], [f"{n[1]} ({n[0]})" for n in options], index=None)

    correct_note = random.choice(notes)
    options = random.sample(notes, 2)
    if correct_note not in options:
        options.append(correct_note)
    random.shuffle(options)

    fig, ax = plt.subplots(figsize=(5, 1))
    ax.plot([0.5], [note_positions[correct_note[0]]], 'ro', markersize=12)
    ax.set_xlim(0, 1)
    ax.set_ylim(-1, 5)
    ax.set_xticks([])
    ax.set_yticks(range(5))
    ax.set_yticklabels([])
    ax.grid(False)
    for i in range(5):
        ax.hlines(i, 0, 1, color='black')
    st.pyplot(fig)

    answer = st.radio(t['choose_note'], [f"{n[1]} ({n[0]})" for n in options])
    if st.button(t['start']):
        selected_note = answer.split("(")[-1].replace(")", "")
        st.session_state.total += 1
        if selected_note == correct_note[0]:
            st.success(t["correct"])
            st.session_state.score += 1
        else:
            st.error(f"{t['incorrect']} {correct_note[1]} ({correct_note[0]})")
        time.sleep(1)
        st.session_state.round += 1
        st.rerun()
