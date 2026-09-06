from app.database import get_connection


def search_found_items(keyword):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT id, item_name, category, description, location, found_date_time
    FROM found_items
    WHERE item_name LIKE ?
       OR category LIKE ?
       OR description LIKE ?
    """

    search = f"%{keyword}%"

    cursor.execute(query, (search, search, search))

    results = cursor.fetchall()

    connection.close()

    return results