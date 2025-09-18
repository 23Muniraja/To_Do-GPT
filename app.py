import streamlit as st
from db_helper import create_task, get_pending_tasks, get_completed_tasks, update_task, delete_task, get_all_tasks

st.set_page_config(page_title="To-Do App", layout="centered")

# Session state to manage navigation
if "page" not in st.session_state:
    st.session_state.page = "welcome"

def go_to(page):
    st.session_state.page = page

# -----------------------------
# Welcome Page
# -----------------------------
def welcome_page():
    st.title("📝 Welcome to the To-Do App")
    st.markdown("""
    This app helps you organize tasks by **priority**:
    - 🔴 Priority 1 = High (do first!)  
    - 🟠 Priority 2 = Medium  
    - 🟢 Priority 3 = Low  

    Choose an action below:
    """)
    st.button("➕ Create a Task", on_click=lambda: go_to("create"))
    st.button("📋 View Pending Tasks", on_click=lambda: go_to("pending"))
    st.button("✅ View Completed Tasks", on_click=lambda: go_to("completed"))
    st.button("✏️ Modify / Delete Tasks", on_click=lambda: go_to("modify"))

# -----------------------------
# Page Placeholders
# -----------------------------
def create_page():
    st.header("➕ Create a Task")
    # Input fields
    task = st.text_input("Enter Task")
    priority = st.selectbox("Select Priority", [1, 2, 3])
    completed = st.checkbox("Completed?")

    if st.button("Add Task"):
        if task.strip() == "":
            st.error("Task cannot be empty!")
        else:
            try:
                create_task(priority, task)  # call helper
                st.success(f"✅ Task '{task}' with priority {priority} added successfully!")
            except Exception as e:
                st.error(f"❌ Error adding task: {e}")

if st.button("⬅ Back", key="back_create"):
        go_to("welcome")

def pending_page():
    st.header("📌 Pending Tasks (by Priority)")

    try:
        tasks = get_pending_tasks()
        if not tasks:
            st.info("No pending tasks 🎉")
        else:
            # Show tasks grouped by priority
            for priority in [1, 2, 3]:
                priority_tasks = [t for t in tasks if t[1] == priority]
                if priority_tasks:
                    for t in priority_tasks:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"🔹 {t[2]}")
                        with col2:
                            if st.button("✅ Complete", key=f"complete_{t[0]}"):
                                try:
                                    update_task(t[0], completed=1)  # update only status
                                    st.success(f"Task '{t[2]}' marked as completed ✅")
                                    st.rerun()  # refresh the page so task disappears
                                except Exception as e:
                                    st.error(f"❌ Error: {e}")
    except Exception as e:
        st.error(f"❌ Error fetching tasks: {e}")

    if st.button("⬅ Back", key="back_pending"):
        go_to("welcome")


def completed_page():
    st.header("✅ Completed Tasks")

    try:
        tasks = get_completed_tasks()
        if not tasks:
            st.info("No completed tasks yet 🎉")
        else:
            # Show tasks grouped by priority
            for priority in [1, 2, 3]:
                priority_tasks = [t for t in tasks if t[1] == priority]
                if priority_tasks:
                    st.subheader(f"Priority {priority}")
                    for t in priority_tasks:
                        st.write(f"🔹 {t[2]} -> Completed")
                        # t[0] = id, t[1] = priority_id, t[2] = task, t[3] = completed
    except Exception as e:
        st.error(f"❌ Error fetching completed tasks: {e}")

    if st.button("⬅ Back", key="back_completed"):
        st.session_state.page = "welcome"
        st.rerun()


def modify_page():
    st.header("✏️ Modify / Delete Tasks")

    try:
        # Fetch all tasks
        tasks = get_all_tasks()  # Returns list of tuples
        if not tasks:
            st.info("No tasks available to modify ❌")
            return

        # Select task to modify
        task_options = [f"{t[0]}: {t[1]}" for t in tasks]  # Format: "id: Task"
        selected = st.selectbox("Select a Task to Modify/Delete", task_options)
        task_id = int(selected.split(":")[0])
        selected_task = next(t for t in tasks if t[0] == task_id)

        # Editable fields with type conversion
        new_task_text = st.text_input("Task", value=selected_task[1])
        new_priority = st.selectbox(
            "Priority",
            [1, 2, 3],
            index=int(selected_task[2]) - 1  # Convert Priority_ID to int
        )
        new_completed = st.checkbox(
            "Completed?",
            value=bool(int(selected_task[3]))  # Convert Completed to int -> bool
        )

        # Action buttons
        col1, col2 = st.columns(2)

        # Update button
        with col1:
            if st.button("💾 Update Task"):
                update_task(
                    task_id,
                    task=new_task_text,
                    priority_id=int(new_priority),
                    completed=int(new_completed)
                )
                st.success("Task updated successfully ✅")

        # Delete button
        with col2:
            if st.button("🗑 Delete Task"):
                delete_task(task_id)
                st.success("Task deleted successfully ❌")

    except Exception as e:
        st.error(f"❌ Error loading tasks: {e}")

    # Back button
    if st.button("⬅ Back", key="back_modify"):
        go_to("welcome")



# -----------------------------
# Render the chosen page
# -----------------------------
if st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "create":
    create_page()
elif st.session_state.page == "pending":
    pending_page()
elif st.session_state.page == "completed":
    completed_page()
elif st.session_state.page == "modify":
    modify_page()