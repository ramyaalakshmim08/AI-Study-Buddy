
import streamlit as st

from components.theme import THEMES, apply_theme

from database import (
    initialize_database,
    get_task_count,
    get_goal_count,
    get_best_habit_streak,
    get_total_focus_minutes,
    get_today_tasks,
    get_upcoming_events,
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# RESTORE SAVED THEME
# --------------------------------------------------

saved_theme = st.query_params.get("theme")

if saved_theme in THEMES:
    st.session_state.setdefault("selected_theme", saved_theme)


def save_theme():
    st.query_params["theme"] = st.session_state["selected_theme"]


# Set a default theme if none is selected
if "selected_theme" not in st.session_state:
    st.session_state["selected_theme"] = next(iter(THEMES))


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

initialize_database()


# --------------------------------------------------
# RESTORE DASHBOARD NAVIGATION
# --------------------------------------------------

if "dashboard_target" in st.session_state:
    st.session_state["selected_page"] = st.session_state.pop(
        "dashboard_target"
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("# 🎓 Study Buddy")
    st.caption("Your personal learning space")

    st.divider()

    st.markdown("### 🎨 Appearance")

    st.selectbox(
        "Choose your theme",
        options=list(THEMES.keys()),
        key="selected_theme",
        on_change=save_theme,
    )

    st.divider()

    st.markdown("### 🧭 Navigation")

    page = st.radio(
        "Go to",
        [
            "Dashboard",
            "AI Study Assistant",
            "My Materials",
            "Notes & Folders",
            "Tasks",
            "Calendar",
            "Habits",
            "Goals",
            "Focus",
            "Study Planner",
            "Progress",
        ],
        key="selected_page",
        label_visibility="collapsed",
    )

    st.divider()

    st.caption("✨ Learn something new every day.")


# --------------------------------------------------
# APPLY THEME
# --------------------------------------------------

apply_theme()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.markdown(
        """
        <div class="welcome-banner">
            <div class="welcome-label">
                YOUR PERSONAL LEARNING SPACE
            </div>
            <h1>Welcome back! 👋</h1>
            <p>
                Small steps every day lead to big achievements.
                Let's make today productive.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")

    # Dashboard statistics

    task_count = get_task_count()
    goal_count = get_goal_count()
    habit_streak = get_best_habit_streak()
    focus_minutes = get_total_focus_minutes()

    st.markdown("### 📊 Your Overview")

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, "📝", "Total Tasks", task_count),
        (c2, "🎯", "Study Goals", goal_count),
        (c3, "🔥", "Best Habit Streak", f"{habit_streak} days"),
        (c4, "⏱️", "Focus Time", f"{focus_minutes} min"),
    ]

    for column, icon, label, value in metrics:
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.write("")

    # Today's overview

    st.markdown("### 📅 Today's Overview")

    left, right = st.columns(2, gap="large")

    # Today's tasks

    with left:
        with st.container(border=True):
            st.markdown("#### 📝 Today's Tasks")
            st.caption("Stay focused on what matters today.")

            today_tasks = get_today_tasks()

            if today_tasks:
                for title, priority in today_tasks:
                    st.markdown(f"**{title}**")
                    st.caption(f"Priority: {priority}")
                    st.divider()
            else:
                st.info(
                    "No tasks scheduled for today. "
                    "A fresh page awaits! 🌱"
                )

            if st.button(
                "Manage Tasks →",
                key="manage_tasks",
                use_container_width=True,
            ):
                st.session_state["dashboard_target"] = "Tasks"
                st.rerun()

    # Upcoming events

    with right:
        with st.container(border=True):
            st.markdown("#### 🗓️ Upcoming Deadlines")
            st.caption("Keep important dates on your radar.")

            upcoming_events = get_upcoming_events()

            if upcoming_events:
                for title, event_date, event_time, description in upcoming_events:
                    st.markdown(f"**📌 {title}**")
                    st.caption(f"📅 {event_date} · 🕒 {event_time}")

                    if description:
                        st.write(description)

                    st.divider()
            else:
                st.info(
                    "No upcoming events yet. "
                    "Add an important date to stay organised. 🌷"
                )

            if st.button(
                "Open Calendar →",
                key="open_calendar",
                use_container_width=True,
            ):
                st.session_state["dashboard_target"] = "Calendar"
                st.rerun()

    st.write("")

    # Quick actions

    st.markdown("### ⚡ Quick Start")
    st.caption("Jump straight into your next activity.")

    a1, a2, a3 = st.columns(3, gap="medium")

    with a1:
        if st.button(
            "🤖 AI Study Assistant",
            use_container_width=True,
        ):
            st.session_state["dashboard_target"] = "AI Study Assistant"
            st.rerun()

    with a2:
        if st.button(
            "✅ Manage Tasks",
            use_container_width=True,
        ):
            st.session_state["dashboard_target"] = "Tasks"
            st.rerun()

    with a3:
        if st.button(
            "📚 My Materials",
            use_container_width=True,
        ):
            st.session_state["dashboard_target"] = "My Materials"
            st.rerun()

    # Footer

    st.write("")

    st.markdown(
        """
        <div class="dashboard-footer">
            Made for your learning journey · One step at a time ✨
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# OTHER PAGES
# --------------------------------------------------

elif page == "Calendar":
    from pages.calendar import render_calendar

    render_calendar()


elif page == "Habits":
    from pages.habits import render_habits

    render_habits()


elif page == "Focus":
    from pages.focus import render_focus

    render_focus()


elif page == "Tasks":
    from pages.tasks import render_tasks

    render_tasks()


elif page == "Goals":
    from pages.goals import render_goals

    render_goals()


elif page == "Notes & Folders":
    from pages.notes import render_notes

    render_notes()


elif page == "My Materials":
    from pages.materials import render_materials

    render_materials()


elif page == "AI Study Assistant":
    from pages.assistant import render_assistant

    render_assistant()


elif page == "Study Planner":
    from pages.planner import render_planner

    render_planner()


elif page == "Progress":
    from pages.progress import render_progress

    render_progress()

