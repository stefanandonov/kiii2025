import streamlit as st
import requests
import pandas as pd
import os

# API Setup
API_HOST = os.getenv("API_HOST", "frontend")
API_PORT = os.getenv("API_PORT", "5001")
API_URL = f"http://{API_HOST}:{API_PORT}/tasks"

st.title("To-Do List App")

# Form to Add Tasks
st.subheader("Add a New Task")
with st.form("add_task"):
    name = st.text_input("Task Name", "")
    category = st.text_input("Category", "")
    description = st.text_area("Description", "")
    deadline = st.date_input("Deadline")
    priority = st.selectbox("Priority", [1, 2, 3, 4, 5])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        response = requests.post(API_URL, json={
            "name": name,
            "category": category,
            "description": description,
            "deadline": str(deadline),
            "priority": priority
        })
        st.rerun()

# Fetch and Display Tasks
st.subheader("Task List")
tasks = requests.get(API_URL).json()

if tasks:
    df = pd.DataFrame(tasks)
    st.dataframe(df, hide_index=True, use_container_width=True)

    for task in tasks:
        with st.expander(f"🔧 {task['name']}"):
            st.markdown(f"**Category:** {task['category']}")
            st.markdown(f"**Description:** {task['description']}")
            st.markdown(f"**Deadline:** {task['deadline']}")
            st.markdown(f"**Priority:** {task['priority']}")

            col1, col2 = st.columns(2)

            # Delete
            if col1.button("🗑️ Delete", key=f"delete_{task['id']}"):
                requests.delete(f"{API_URL}/{task['id']}")
                st.rerun()

            # Edit
            with col2.popover("✏️ Edit"):
                new_name = st.text_input("Task Name", task['name'], key=f"edit_name_{task['id']}")
                new_category = st.text_input("Category", task['category'], key=f"edit_category_{task['id']}")
                new_description = st.text_area("Description", task['description'], key=f"edit_desc_{task['id']}")
                new_deadline = st.date_input("Deadline", pd.to_datetime(task['deadline']), key=f"edit_deadline_{task['id']}")
                new_priority = st.selectbox("Priority", [1, 2, 3, 4, 5], index=task['priority'] - 1, key=f"edit_prio_{task['id']}")

                if st.button("💾 Save", key=f"save_{task['id']}"):
                    requests.put(f"{API_URL}/{task['id']}", json={
                        "name": new_name,
                        "category": new_category,
                        "description": new_description,
                        "deadline": str(new_deadline),
                        "priority": new_priority
                    })
                    st.success("Task updated!")
                    st.rerun()

else:
    st.write("No tasks found.")
