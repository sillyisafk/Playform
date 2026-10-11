import streamlit as st
import matplotlib.pyplot as plt
from question import questions

archetypes = {
    "Socializer": (0, 0.9),
    "Challenger": (0.8, 0.5),
    "Strategist": (0.8, -0.4),
    "Creator": (0, -0.9),
    "Explorer": (-0.8, -0.5),
    "Immersive": (-0.8, 0.3)
}



if "page" not in st.session_state:
    st.session_state.page = "landing"

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}


def distance(name):
    ax, ay = archetypes[name]
    d = ((x - ax)**2 + (y - ay)**2)**(1/2)
    return d


def get_ready():
    st.session_state.page = "ready"

def start_quiz():
    st.session_state.page = "quiz"

def next_question():
    selected = st.session_state[f"q_{st.session_state.q_index}"]
    st.session_state.answers[st.session_state.q_index] = selected
    if st.session_state.q_index == len(questions) - 1:
        st.session_state.page = "result"
    else:
        st.session_state.q_index += 1

def restart():
    st.session_state.page = "ready"
    st.session_state.q_index = 0
    st.session_state.answers = {}

def go_back():
    st.session_state.q_index -= 1


if st.session_state.page == "landing":
    st.write("what is your")
    st.title("PLAYFORM")
    st.write("let's find out :)")
    st.button("play →", on_click=get_ready)
    st.caption("24 questions ~5 minutes")

elif st.session_state.page == "ready":
    st.write("Ready page")
    st.button("less go →", on_click=start_quiz)

elif st.session_state.page == "quiz":
    current = questions[st.session_state.q_index]
    st.write(current["text"])
    st.radio("Choose one", list(current["options"]),
             key=f"q_{st.session_state.q_index}",
             label_visibility="collapsed")

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.q_index > 0:
            st.button("← back", on_click=go_back)
    with col2:
        st.button("next →", on_click=next_question)

else:
    scores = {}
    for i, option in st.session_state.answers.items():
        trait = questions[i]["options"][option]
        scores[trait] = scores.get(trait, 0) + 1

    mastery = scores.get("Mastery", 0)
    discovery = scores.get("Discovery", 0)
    connection = scores.get("Connection", 0)
    freedom = scores.get("Freedom", 0)

    x = (mastery - discovery) / len(questions)
    y = (connection - freedom) / len(questions)
    closest = min(archetypes, key=distance)

    #st.write(x, y)
    st.write("Your archetype:", closest)
    #st.write(scores)
    st.button("play again", on_click=restart)

    fig, ax = plt.subplots()
    for side in ["top", "right", "bottom", "left"]:
        ax.spines[side].set_visible(False)
    ax.scatter([x], [y], color="red")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.text(1.06, 0, "Mastery")
    ax.text(-1.46, 0, "Discovery")
    ax.text(-0.23, 1.06, "Connection")
    ax.text(-0.13, -1.13, "Freedom")
    ax.axhline(0, color="black")
    ax.axvline(0, color="black")
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    for name, (px, py) in archetypes.items():
        ax.scatter([px], [py], color="gray")
        ax.text(px, py, name)
    st.pyplot(fig)