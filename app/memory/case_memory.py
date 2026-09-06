from app.database import get_connection
from datetime import datetime


def create_case(item_name, description, location, lost_date_time):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO investigation_cases
    (item_name, description, lost_location, lost_date_time,
     status, current_step, possible_matches, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item_name,
        description,
        location,
        lost_date_time,
        "searching",
        "Case created",
        "",
        datetime.now().isoformat()
    ))

    case_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return case_id


def get_case(case_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT *
    FROM investigation_cases
    WHERE id = ?
    """, (case_id,))

    case = cursor.fetchone()

    connection.close()

    return case


def update_case(case_id, step, matches="", status="searching"):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE investigation_cases
    SET current_step = ?,
        possible_matches = ?,
        status = ?,
        last_updated = ?
    WHERE id = ?
    """, (
        step,
        matches,
        status,
        datetime.now().isoformat(),
        case_id
    ))

    connection.commit()
    connection.close()