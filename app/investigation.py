from app.memory.case_memory import (
    create_case,
    get_case,
    update_case
)

from app.tools.search_tools import search_found_items
from app.tools.location_tool import calculate_distance
from app.tools.notification_tool import send_notification


def investigate_lost_item(
    item_name,
    description,
    location,
    lost_date_time,
    lost_lat,
    lost_lon,
    user_name="Student"
):
    print("\n LOSTIQ Investigation Started")
    print("--------------------------------")

    # STEP 1: Create case memory
    case_id = create_case(
        item_name,
        description,
        location,
        lost_date_time
    )

    print(f" Case created: #{case_id}")

    # STEP 2: Update memory
    update_case(
        case_id,
        "Searching found items"
    )

    print(" Searching found items...")

    # STEP 3: Use Search Tool
    results = search_found_items(item_name)

    if not results:
        update_case(
            case_id,
            "No matching items found",
            "",
            "searching"
        )
        print(" No possible matches found.")

        return get_case(case_id), []

    print(f" {len(results)} possible match(es) found.")

    # STEP 4: Check locations
    nearby_matches = []

    for item in results:

        # item structure:
        # id, item_name, category,
        # description, location, found_date_time

        found_id = item[0]

        # Demo coordinates for the found item.
        # Later these will come from the database.
        found_lat = 13.0830
        found_lon = 80.2710

        distance = calculate_distance(
            lost_lat,
            lost_lon,
            found_lat,
            found_lon
        )

        print(
            f" Found Item #{found_id}: "
            f"{distance} meters away"
        )

        if distance <= 500:
            nearby_matches.append(
                (found_id, distance)
            )

    # STEP 5: Update memory
    if nearby_matches:

        match_text = ", ".join(
            f"Item #{item_id} ({distance}m away)"
            for item_id, distance in nearby_matches
        )

        update_case(
            case_id,
            "Nearby possible match found",
            match_text,
            "verification"
        )

        print(" Nearby match found!")

        # STEP 6: Notification Tool
        send_notification(
            user_name,
            f"Potential match found for your {item_name}. "
            f"Possible match: {match_text}. "
            f"Please verify ownership."
        )

    else:

        update_case(
            case_id,
            "Found items exist but none are nearby",
            "",
            "searching"
        )

        print(" No nearby matches found.")

    # STEP 7: Retrieve memory
    case = get_case(case_id)

    return case, nearby_matches