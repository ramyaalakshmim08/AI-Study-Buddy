import sqlite3


DATABASE_NAME = "study_buddy.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Tasks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT DEFAULT 'Medium',
            completed INTEGER DEFAULT 0
        )
    """)

    # Notes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            folder TEXT,
            created_at TEXT
        )
    """)

    # Habits
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            frequency TEXT,
            streak INTEGER DEFAULT 0,
            last_completed TEXT
        )
    """)

    # Goals
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            target_date TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    # Calendar events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_date TEXT,
            event_time TEXT,
            description TEXT
        )
    """)

    # Study sessions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            duration INTEGER,
            session_date TEXT
        )
    """)

    connection.commit()
    connection.close()


def get_task_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 0"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


def get_goal_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM goals WHERE completed = 0"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


def get_best_habit_streak():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(MAX(streak), 0)
        FROM habits
    """)

    streak = cursor.fetchone()[0]

    connection.close()

    return streak


def get_total_focus_minutes():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(duration), 0)
        FROM study_sessions
    """)

    minutes = cursor.fetchone()[0]

    connection.close()

    return minutes


def get_today_tasks():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT title, priority
        FROM tasks
        WHERE completed = 0
        AND due_date = date('now')
        ORDER BY priority
    """)

    tasks = cursor.fetchall()

    connection.close()

    return tasks
def get_upcoming_events(limit=5):
    from datetime import date

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT title, event_date, event_time, description
        FROM calendar_events
        WHERE event_date >= ?
        ORDER BY event_date ASC, event_time ASC
        LIMIT ?
    """, (date.today().isoformat(), limit))

    events = cursor.fetchall()
    connection.close()

    return events

