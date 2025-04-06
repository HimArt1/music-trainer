import streamlit as st
import random
import time
import matplotlib.pyplot as plt

# الشعار
st.image("Logo.PNG", width=150)

# إعداد الصفحة
st.set_page_config(page_title="Note Reading Trainer (G Clef)")

# النغمات واسمائها
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

# المواقع العمودية للنغمات على المدرج (مفتاح صول)
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

# اختيار نغمة عشوائية
if "note" not in st.session_state:
    st.session_state.note = random.choice(notes)

note, name = st.session_state.note

# رسم المدرج الموسيقي والنغمة
fig, ax = plt.subplots(figsize=(5, 2))
for i in range(5):
    ax.hlines(i, 0, 4, color='black')
ax.plot(2, note_positions[note], 'ro', markersize=12)
ax.set_xlim(0, 4)
ax.set_ylim(-1, 5)
ax.axis('off')
st.pyplot(fig)

st.subheader("Round 1")

# خيارات عشوائية للإجابة
choices = random.sample(notes, 3)
if st.session_state.note not in choices:
    choices[random.randint(0, 2)] = st.session_state.note

# عرض الأزرار كخيارات
for n, solfege in choices:
    if st.button(f"{solfege} ({n})"):
        if n == note:
            st.success("Correct!")
            time.sleep(1)
            st.session_state.note = random.choice(notes)
            st.rerun()
        else:
            st.error("Wrong! Try again.")
