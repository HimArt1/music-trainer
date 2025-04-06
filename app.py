


import streamlit as st
import random
import time
import os
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

st.set_page_config(page_title="Note Reading Trainer (G Clef)", layout="centered")

if "language" not in st.session_state:
    st.session_state.language = None

if st.session_state.language is None:
    st.image("Logo.PNG", width=150)
    st.markdown("## Welcome | مرحباً بك")
    lang = st.radio("Choose Language | اختر اللغة", ["English", "العربية"])
    if st.button("Start | ابدأ"):
        st.session_state.language = lang
        st.rerun()

if st.session_state.language is not None:
    lang = st.session_state.language
    is_ar = lang == "العربية"

    st.image("Logo.PNG", width=150)
    st.title("مدرب قراءة النوتات (مفتاح صول)" if is_ar else "Note Reading Trainer (G Clef)")

    notes = [
        ('E', 'Mi'), ('F', 'Fa'), ('G', 'Sol'), ('A', 'La'),
        ('B', 'Si'), ('C', 'Do'), ('D', 'Re'), ('E2', 'Mi'), ('F2', 'Fa')
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

        clef_img = mpimg.imread("Sol.PNG")
        ax.imshow(clef_img, aspect='auto', extent=(-0.8, 0.5, 0, 4.5), zorder=1)

        ax.plot(2.5, note_positions[note], 'ro', markersize=14, zorder=2)
        st.pyplot(fig)

    if "score" not in st.session_state:
        st.session_state.round = 1
        st.session_state.score = 0
        st.session_state.correct_count = 0
        st.session_state.wrong_count = 0
        st.session_state.start_time = time.time()
        st.session_state.current_question = 1
        st.session_state.total_rounds = 5
        st.session_state.questions_per_round = 5
        st.session_state.feedback = None
        st.session_state.last_note = None
        st.session_state.last_answer = None

    if st.session_state.round > st.session_state.total_rounds:
        elapsed = int(time.time() - st.session_state.start_time)
        st.markdown("### النهاية" if is_ar else "### Game Over")
        st.markdown(f"النتيجة: {st.session_state.score}/25")
        st.markdown(f"✅ {st.session_state.correct_count}    ❌ {st.session_state.wrong_count}")
        st.markdown(f"الوقت المستغرق: {elapsed} ثانية" if is_ar else f"Time taken: {elapsed} seconds")
        if st.button("إعادة التشغيل" if is_ar else "Restart"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    else:
        st.markdown(f"### الجولة {st.session_state.round} - السؤال {st.session_state.current_question}" if is_ar else f"### Round {st.session_state.round} - Q{st.session_state.current_question}")

        if st.session_state.feedback is None:
            current_note = random.choice(notes)
            st.session_state.last_note = current_note
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

            draw_note(current_note[0])
            options_list = [f"{n[1]} ({n[0]})" for n in options]
            answer = st.radio(
                "اختر اسم النغمة الصحيحة:" if is_ar else "Choose the correct note name:",
                options_list,
                index=None,
                key=f"answer_q{st.session_state.round}_{st.session_state.current_question}"
            )

            if answer:
                st.session_state.last_answer = answer
                if answer.startswith(current_note[1]):
                    st.session_state.score += 1
                    st.session_state.correct_count += 1
                    st.session_state.feedback = "correct"
                else:
                    st.session_state.wrong_count += 1
                    st.session_state.feedback = "wrong"
                st.rerun()
        else:
            draw_note(st.session_state.last_note[0])
            if st.session_state.feedback == "correct":
                st.success("إجابة صحيحة!" if is_ar else "Correct!")
                st.markdown("✅")
            else:
                st.error(
                    f"إجابة خاطئة! النغمة الصحيحة هي {st.session_state.last_note[1]} ({st.session_state.last_note[0]})"
                    if is_ar else f"Incorrect! The correct answer was {st.session_state.last_note[1]} ({st.session_state.last_note[0]})"
                )
                st.markdown("❌")

            st.markdown(f"✅ {st.session_state.correct_count}    ❌ {st.session_state.wrong_count}")

            if st.session_state.current_question < st.session_state.questions_per_round:
                if st.button("التالي" if is_ar else "Next"):
                    st.session_state.current_question += 1
            else:
                if st.button("الجولة التالية" if is_ar else "Next Round"):
                    st.session_state.round += 1
                    st.session_state.current_question = 1

            st.session_state.feedback = None
            st.rerun()

