import streamlit as st

# In-memory task list
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("AI-Powered To-Do App (Prototype)")

# --- Task Form ---
st.subheader("Add a Task")
title = st.text_input("Task Title")
priority = st.slider("Priority (1 = low, 10 = high)", 1, 10, 5)
urgency = st.selectbox("Urgency", ["Low", "Medium", "High"])
due = st.time_input("Due time (optional)", value=None)

if st.button("Add Task"):
    st.session_state.tasks.append({
        "title": title,
        "priority": priority,
        "urgency": urgency,
        "done": False
    })

# --- Task List ---
st.subheader("Today's Tasks")
for i, task in enumerate(st.session_state.tasks):
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(
            f"**{task['title']}** — Priority: {task['priority']}, Urgency: {task['urgency']}"
        )
    with col2:
        if st.checkbox("Done", key=i):
            task["done"] = True
            st.session_state.tasks[i] = task
            st.success(f"✅ Task '{task['title']}' completed!")

            # Ask about habit
            make_habit = st.radio(
                f"Make '{task['title']}' a habit?", ["No", "Yes"], key=f"habit_{i}"
            )
            if make_habit == "Yes":
                st.write("Great! In the real app, this would open habit settings.")

