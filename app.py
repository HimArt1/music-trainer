
import streamlit as st
import random
import time
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="Note Reading Trainer", layout="centered")

# الشعار
st.image("Logo.PNG", width=150)

# دعم اللغتين
languages = {
    "en": {
        "welcome": "Welcome",
        "choose_lang": "Choose Language",
        "start": "Start",
        "round": "Round",
        "choose_answer": "Choose the correct note name:",
        "correct": "Correct!",
        "incorrect": "Incorrect! The correct answer was",
        "score": "Your score is",
        "restart": "Restart",
    },
    "ar": {
        "welcome": "مرحباً بك",
        "choose_lang": "اختر اللغة",
        "start": "ابدأ",
        "round": "الجولة",
        "choose_answer": "اختر اسم النغمة الصحيحة:",
        "correct": "إجابة صحيحة!",
        "incorrect": "إجابة خاطئة! النغمة الصحيحة كانت",
        "score": "درجتك هي",
        "restart": "أعد المحاولة",
    }
}

if "language" not in st.session_state:
    st.session_state.language = None
if "started" not in st.session_state:
    st.session_state.started = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "round" not in st.session_state:
    st.session_state.round = 1

# واجهة البداية
if not st.session_state.started:
    st.markdown(f"## {languages['en']['welcome']} | {languages['ar']['welcome']}")
    lang_choice = st.radio(f"{languages['en']['choose_lang']} | {languages['ar']['choose_lang']}", ["English", "العربية"])
    st.session_state.language = "en" if lang_choice == "English" else "ar"
    if st.button(f"{languages['en']['start']} | {languages['ar']['start']}"):
        st.session_state.started = True
        st.experimental_rerun()

# المتغيرات بعد البدء
if st.session_state.started:
    lang = st.session_state.language
    text = languages[lang]

    notes = [
        ('E', 'Mi'), ('F', 'Fa'), ('G', 'Sol'),
        ('A', 'La'), ('B', 'Si'), ('C', 'Do'),
        ('D', 'Re'), ('E2', 'Mi'), ('F2', 'Fa')
    ]

    note_positions = {
        'E': 0, 'F': 0.5, 'G': 1, 'A': 1.5, 'B': 2,
        'C': 2.5, 'D': 3, 'E2': 3.5, 'F2': 4
    }

    note, solfege = random.choice(notes)
    st.markdown(f"### {text['round']} {st.session_state.round}")

    fig, ax = plt.subplots(figsize=(5, 1))
    ax.set_xlim(-1, 9)
    ax.set_ylim(-1, 5)
    ax.set_axis_off()
    for i in range(5):
        ax.hlines(i, 0, 8, color='black')
    y_pos = note_positions[note]
    ax.plot(4, y_pos, 'ro', markersize=12)
    st.pyplot(fig)

    options = random.sample(notes, 2)
    options.append((note, solfege))
    random.shuffle(options)
    choice = st.radio(text["choose_answer"], [f"{s} ({n})" for n, s in options], key=f"choice_{st.session_state.round}")

    if st.button("Submit"):
        selected_note = [n for n, s in options if f"{s} ({n})" == choice][0]
        if selected_note == note:
            st.success(text["correct"])
            st.session_state.score += 1
        else:
            st.error(f"{text['incorrect']} {solfege} ({note})")
        st.session_state.round += 1
        time.sleep(1.5)
        st.experimental_rerun()
