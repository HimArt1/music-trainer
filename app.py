
import streamlit as st
import random
import time
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="Note Reading Trainer", layout="centered")

st.image("Logo.PNG", width=150)

# تعريف النغمات ومواقعها على المدرج (مفتاح صول)
notes = [
    ('E', 'Mi'),
    ('F', 'Fa'),
    ('G', 'Sol'),
    ('A', 'La'),
    ('B', 'Si'),
    ('C', 'Do'),
    ('D', 'Re'),
    ('E2', 'Mi'),
    ('F2', 'Fa')
]

note_positions = {
    'E': 0,
    'F': 0.5,
    'G': 1,
    'A': 1.5,
    'B': 2,
    'C': 2.5,
    'D': 3,
    'E2': 3.5,
    'F2': 4
}

# رسم المدرج الموسيقي مع النغمة
def draw_staff(note_letter, result=None):
    fig, ax = plt.subplots(figsize=(6, 2))
    for i in range(5):
        ax.plot([0, 6], [i, i], color='black')

    y = note_positions[note_letter]
    color = 'red'
    if result == "Correct":
        color = 'green'
    elif result == "Wrong":
        color = 'red'
    ax.plot(3, y, 'o', markersize=14, color=color)

    ax.text(0.2, 2, "𝄞", fontsize=30, color='black')
    ax.set_xlim(0, 6)
    ax.set_ylim(-1, 5)
    ax.axis('off')
    return fig

# حالة الجلسة
if "score" not in st.session_state:
    st.session_state.round = 1
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.correct_note = random.choice(notes)
    st.session_state.start_time = time.time()

st.title("Note Reading Trainer (G Clef)")
st.subheader(f"Round {st.session_state.round}")

fig = draw_staff(st.session_state.correct_note[0])
st.pyplot(fig)

# توليد الخيارات (دائماً مع النغمة الصحيحة)
wrong_choices = [n for n in notes if n != st.session_state.correct_note]
options = random.sample(wrong_choices, 2)
options.append(st.session_state.correct_note)
random.shuffle(options)

# عرض الأزرار للاختيار
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]
for i, (eng, lat) in enumerate(options):
    if cols[i].button(f"{lat} ({eng})"):
        end_time = time.time()
        response_time = round(end_time - st.session_state.start_time, 2)
        selected_note = (eng, lat)
        is_correct = selected_note == st.session_state.correct_note

        st.session_state.history.append({
            "Round": st.session_state.round,
            "Your Choice": f"{lat} ({eng})",
            "Correct Answer": f"{st.session_state.correct_note[1]} ({st.session_state.correct_note[0]})",
            "Time (s)": response_time,
            "Result": "Correct" if is_correct else "Wrong"
        })

        if is_correct:
            st.success("Correct!")
            st.session_state.score += 1
        else:
            st.error(f"Wrong! The correct answer was: {st.session_state.correct_note[1]} ({st.session_state.correct_note[0]})")

        st.session_state.round += 1
        st.session_state.correct_note = random.choice(notes)
        st.session_state.start_time = time.time()
        st.experimental_rerun()

# عرض النتيجة في النهاية
if st.session_state.round > 5:
    st.header("Results")
    st.write(f"Final Score: {st.session_state.score}/5")
    st.dataframe(st.session_state.history)
    if st.button("Restart"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
