import mysql.connector
from mysql.connector import Error


#Creating Connection with database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="muni",
        database="db_to_do-gpt"
    )

#Create new Task:
# 0 - False(Task not completed)
# 1 - True(Task completed
# )
def create_task(priority_id, task):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO To_Do (Task, Priority_ID, Completed) VALUES (%s, %s, 0)" #By default, completed is 0.
        cursor.execute(sql, (task, priority_id))
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

# Get pending tasks (priority-wise)
def get_pending_tasks():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = "SELECT id, priority_id, task FROM To_Do WHERE completed = 0 ORDER BY priority_id ASC, id ASC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()



# Get completed tasks
def get_completed_tasks():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM To_Do WHERE Completed=1 ORDER BY id ASC"
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# Update task (modify)
def update_task(task_id, priority_id=None, task=None, completed=None):
    conn = get_connection()
    cursor = conn.cursor()

    updates = []
    values = []

    if priority_id is not None:
        updates.append("priority_id = %s")
        values.append(priority_id)
    if task is not None:
        updates.append("task = %s")
        values.append(task)
    if completed is not None:
        updates.append("completed = %s")
        values.append(completed)

    values.append(task_id)
    sql = f"UPDATE To_Do SET {', '.join(updates)} WHERE id = %s"
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

# Gets all task there
def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, Task, Priority_ID, Completed FROM To_Do ORDER BY Priority_ID ASC, id ASC")
    rows = cursor.fetchall()  # returns list of tuples
    cursor.close()
    conn.close()
    return rows

# Delete task
def delete_task(id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM To_Do WHERE id=%s"
        cursor.execute(sql, (id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
