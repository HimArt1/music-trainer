

import streamlit as st
import random
import time
import os
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

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

    def draw_note(note):
        fig, ax = plt.subplots(figsize=(8, 2.5))
        ax.set_xlim(-1, 6)
        ax.set_ylim(-1, 5)
        ax.axis('off')

        for i in range(5):
            ax.hlines(i, 0, 5, color='black', linewidth=1.5)

        clef_img = mpimg.imread("Sol.png")
        ax.imshow(clef_img, aspect='auto', extent=(-0.8, 0.5, 0, 4.5), zorder=1)

        ax.plot(2.5, note_positions[note], 'ro', markersize=14, zorder=2)

        st.pyplot(fig)

    if "score" not in st.session_state:
        st.session_state.round = 1
        st.session_state.score = 0
        st.session_state.start_time = time.time()

    current_note = random.choice(notes)
    options = random.sample(notes, 2)
    if current_note not in options:
        options.append(current_note)
    else:
        options = list(set(options))
    while len(options) < 3:
        opt = random.choice(notes)
        if opt not in options:
            options.append(opt)
    random.shuffle(options)

    st.markdown(f"### الجولة {st.session_state.round}" if is_ar else f"### Round {st.session_state.round}")
    draw_note(current_note[0])

    options_list = [f"{n[1]} ({n[0]})" for n in options]
    answer = st.radio(
        "اختر اسم النغمة الصحيحة:" if is_ar else "Choose the correct note name:",
        options_list,
        index=None,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '''
        <style>
        div.row-widget.stRadio > div {
            flex-direction: column;
        }
        div.row-widget.stRadio > div > label {
            font-size: 18px;
            padding: 8px 0;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )

    if st.button("تأكيد" if is_ar else "Submit"):
        if answer and answer.startswith(current_note[1]):
            st.success("إجابة صحيحة!" if is_ar else "Correct!")
            st.session_state.score += 1
        else:
            st.error(
                f"إجابة خاطئة! النغمة الصحيحة هي {current_note[1]} ({current_note[0]})"
                if is_ar else f"Incorrect! The correct answer was {current_note[1]} ({current_note[0]})"
            )

        st.session_state.round += 1

        if st.session_state.round > 5:
            elapsed = int(time.time() - st.session_state.start_time)
            st.markdown("---")
            st.markdown("### النهاية" if is_ar else "### Game Over")
            st.markdown(f"النتيجة: {st.session_state.score}/5" if is_ar else f"Score: {st.session_state.score}/5")
            st.markdown(f"الوقت المستغرق: {elapsed} ثانية" if is_ar else f"Time taken: {elapsed} seconds")
            if st.button("إعادة التشغيل" if is_ar else "Restart"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
