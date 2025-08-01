import streamlit as st
from datetime import datetime, timedelta, time

# In-memory task list
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "habbits" not in st.session_state:
    st.session_state.habbits = []


st.title("AI-Powered To-Do App (Prototype)")



# --- Task Form ---
st.subheader("Add a Task")
title = st.text_input("Task Title")
priority = st.slider("importance (1 = low, 10 = high)", 1, 23, 8)
dura = st.checkbox("do you know how long the task will take aprox?")
duration = "none"
if dura == True:
    options = [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345, 360]

    duration = st.select_slider(
        "⏱️ Approximately how long will this task take? (optional)",
        options=options,
        format_func=lambda x: f"{x} min" if x < 60 else f"{x//60} hr" if x % 60 == 0 else f"{x//60} hr {x%60} min"
    )

    st.write(f"✅ You selected: {duration} minutes")

due = st.radio("Does this task have a specific date or time deadline?" , ["yes", "no"])
if due == "no":
    urgency = st.selectbox("Pick urgency level", ["Low", "Medium", "High"])

if due == "yes":
    today = datetime.now().date()
    now = datetime.now()

    st.title("Pick a date and time")

    date = st.date_input("Pick a date", min_value=today)

    specific_time = st.selectbox("Specific time?", ["yes", "no"])

    if specific_time == "yes":
        time = st.time_input("Pick a time")
        datetime_selected = datetime.combine(date, time)
        if date==today and time < now.time():
            st.error("You cannot pick a time that has already passed!")
        else:
            st.write("Deadline date and time:", datetime_selected)
        # --- Calculate urgency based on time left
        time_remaining = datetime_selected - now

        if time_remaining <= timedelta(hours=2):
            urgency = "High"
        elif time_remaining <= timedelta(hours=7):
            urgency = "Medium"
        else:
            urgency = "Low"

        st.write(f"🔥 Automatically set urgency: **{urgency}**")
    if specific_time == "no":
        urgency = st.selectbox("Pick urgency level", ["Low", "Medium", "High"])


else:
    today = datetime.now().date()
    st.write("✅ Deadline date only:", today )
    # Let user pick urgency manually in this case


if st.button("Add Task"):
    if due == "yes" and specific_time == "yes" and date == today and time < now.time():
        st.error("❌ You cannot pick a time that has already passed!")
    else:
        if due == "yes" and specific_time == "yes":
            st.session_state.tasks.append({
                "title": title,
                "priority": priority,
                "urgency": urgency,
                "duration" : duration,
                "deadline day": datetime_selected.date(),
                "deadline time": datetime_selected.time(),
                "done": False
              })
        elif due == "yes" and specific_time == "no":
            st.session_state.tasks.append({
                "title": title,
                "priority": priority,
                "urgency": urgency,
                "duration": duration,
                "deadline day": date,
                "deadline time": "none",
                "done": False
            })
        else:
            st.session_state.tasks.append({
                "title": title,
                "priority": priority,
                "urgency": urgency,
                "duration" : duration,
                "deadline day" : "none",
                "deadline time": "none",
                "done": False
         })

# --- Task List ---
today = datetime.now().date()
completed_tasks = []
st.subheader("Today's Tasks")


# 1. Filter today's tasks
todays_tasks = [task for task in st.session_state.tasks if task["deadline day"] == today]

# 2. Sort by time if exists, else priority
todays_tasks.sort(key=lambda task: (
    task["deadline time"] if task["deadline time"] != "none" else time.max,
    -task["priority"]  # negative because higher priority means should come first
))


for i, task in enumerate(todays_tasks):
    if task["deadline day"] == datetime.now().date():
        col1, col2 = st.columns([6, 1])
        with col1:
            if task["deadline day"] == datetime.now().date():
                st.markdown(
                    f"**{task['title']}** — Priority: {task['priority']}, Urgency: {task['urgency']}, Duration: {task['duration']} min, Deadline day: {task['deadline day']}, Deadline time: {task['deadline time']}"
                )

        with col2:
            if task["deadline day"] == datetime.now().date():
                if st.checkbox("Done", key=f"today_{i}"):
                    task["done"] = True
                    st.session_state.tasks[i] = task
                    st.success(f"✅ Task '{task['title']}' completed!")

                    # Ask about habit
                    make_habit = st.radio(
                        f"Make '{task['title']}' a habit?", ["No", "Yes"], key=f"habit_{i}"
                    )
                    if make_habit == "Yes":
                        st.write("Great! In the real app, this would open habit settings.")

st.subheader("Future Tasks")
# Filter future tasks
future_tasks = [task for task in st.session_state.tasks if task["deadline day"] != "none" and task["deadline day"] > today]
future_tasks.sort(key=lambda task: (
    task["deadline day"] ,task["deadline time"] if task["deadline time"] != "none" else time.max,
    -task["priority"]
))


for i, task in enumerate(future_tasks):
    if task["deadline day"] != datetime.now().date():
        col1, col2 = st.columns([6, 1])
        with col1:

                st.markdown(
                    f"**{task['title']}** — Priority: {task['priority']}, Urgency: {task['urgency']}, Duration: {task['duration']} min, Deadline day: {task['deadline day']}, Deadline time: {task['deadline time']}"
                )

        with col2:

                if st.checkbox("Done", key=f"future_{i}"):
                    task["done"] = True
                    st.session_state.tasks[i] = task
                    st.success(f"✅ Task '{task['title']}' completed!")

                    # Ask about habit
                    make_habit = st.radio(
                        f"Make '{task['title']}' a habit?", ["No", "Yes"], key=f"habit_{i}"
                    )
                    if make_habit == "Yes":
                        st.write("Great! In the real app, this would open habit settings.")

st.subheader("undated tasks")
undated_tasks  = [task for task in st.session_state.tasks if task["deadline day"] == "none"]

undated_tasks.sort(key=lambda task: (-task["priority"],task["urgency"]))
for i, task in enumerate(undated_tasks):
    if task["deadline day"] != datetime.now().date():
        col1, col2 = st.columns([6, 1])
        with col1:

                st.markdown(
                    f"**{task['title']}** — Priority: {task['priority']}, Urgency: {task['urgency']}, Duration: {task['duration']} min, Deadline day: {task['deadline day']}, Deadline time: {task['deadline time']}"
                )

        with col2:

                if st.checkbox("Done", key=f"undated_{i}"):
                    task["done"] = True
                    st.session_state.tasks[i] = task
                    st.success(f"✅ Task '{task['title']}' completed!")
                    completed_tasks.append(task)

                    # Ask about habit
                    make_habit = st.radio(
                        f"Make '{task['title']}' a habit?", ["No", "Yes"], key=f"habit_{i}"
                    )
                    if make_habit == "Yes":
                        habit_frequency = st.select_slider("how often do you plan to do this habit?", ["daily","weekly", "monthly", "custom"])

                        habit_importance = st.slider("priority (1 = low, 10 = high)", 1, 23, 8, key="habit_importance")
                        habit_specfic_time = st.checkbox("do you wish to start this habit a specfic time?")
                        if habit_specfic_time == True:
                            habit_time = st.time_input( "Pick a starting time")
                        else:
                            habit_time = "none"
                    if st.button("Add habit"):
                        if habit_specfic_time == True:
                            st.session_state.habbits.append({
                                "title": task["title"],
                                "importance": habit_importance,
                                "duration": task["duration"],
                                "frequency": habit_frequency,
                                "starting time": habit_time,

                            })
                        else:
                            st.session_state.habbits.append({
                                "title": task["title"],
                                "importance": habit_importance,
                                "duration": task["duration"],
                                "frequency": habit_frequency,
                                "starting time": "none",

                            })




st.subheader("completed tasks")
for i in completed_tasks:
    st.markdown(
    f"**{i['title']}** — Priority: {i['priority']}, Urgency: {i['urgency']}, Duration: {i['duration']} min, Deadline day: {i['deadline day']}, Deadline time: {i['deadline time']}"
    )

st.subheader("habits")

