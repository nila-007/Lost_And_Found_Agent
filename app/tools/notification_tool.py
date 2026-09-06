from datetime import datetime


def send_notification(user_name, message):
    """
    Simulates sending a notification to a user.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    notification = f"""
========================================
 LOSTIQ NOTIFICATION
========================================
Time: {timestamp}
To: {user_name}

{message}

========================================
"""

    print(notification)

    return True