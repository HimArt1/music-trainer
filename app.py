import streamlit as st
import random
import time
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="Note Reading Trainer (G Clef)")

# الشعار
st.image("Logo.PNG", width=150)

# النغمات وأسمائها
notes = [
    ('E', 'Mi'),
    ('F', 'Fa'),
    ('G', 'Sol'),
    ('A', 'La'),
    ('B', 'Si'),
    ('C', 'Do'),
    ('D', 'Re'),
    ('E2', 'Mi'),
    ('F2', 'Fa'),
]

# مواقع النغمات على المدرج (مفتاح صول)
note_positions = {
    'E': 0,
    'F': 0.5,
    'G': 1,
    'A': 1.5,
    'B': 2,
    'C': 2.5,
    'D': 3,
    'E2': 3.5,
    'F2': 4,
}

# اللعبة
st.title("Note Reading Trainer (G Clef)")
score = 0
rounds = 5

for i in range(rounds):
    st.subheader(f"Round {i+1}")
    note, name = random.choice(notes)

    fig, ax = plt.subplots(figsize=(4, 1))
    ax.plot([0.5], [note_positions[note]], 'ro', markersize=10)
    ax.set_yticks(range(5))
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, 4.5)
    ax.invert_yaxis()
    ax.set_facecolor("white")
    for y in range(5):
        ax.hlines(y, 0, 1, colors='black')
    st.pyplot(fig)

    options = random.sample(notes, 2)
    options.append((note, name))
    random.shuffle(options)
    answer = st.radio("Choose the correct note name:", [f"{n[1]} ({n[0]})" for n in options])
    if answer == f"{name} ({note})":
        st.success("Correct!")
        score += 1
    else:
        st.error(f"Incorrect! The correct answer was {name} ({note})")

    st.write("---")
    time.sleep(0.5)

st.subheader(f"Your score: {score}/{rounds}")
