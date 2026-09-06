from app.tools.search_tools import search_found_items
from app.tools.location_tool import calculate_distance
from app.tools.notification_tool import send_notification

from app.memory.case_memory import (
    create_case,
    get_case,
    update_case
)


class LostIQAgent:

    def __init__(self):
        self.tools = {
            "search": search_found_items,
            "distance": calculate_distance,
            "notify": send_notification
        }

    def investigate(
        self,
        item_name,
        description,
        location,
        lost_date_time,
        lost_lat,
        lost_lon,
        user_name="Student"
    ):

        print("\nLOSTIQ AGENT")
        print("==============================")

        # 1. Create case memory
        case_id = create_case(
            item_name,
            description,
            location,
            lost_date_time
        )

        print(f" Memory created → Case #{case_id}")

        # 2. Agent chooses SEARCH tool
        print("\n Agent decision: SEARCH")

        search_tool = self.tools["search"]

        matches = search_tool(item_name)

        if not matches:
            update_case(
                case_id,
                "Search completed - no matches",
                "",
                "searching"
            )

            print(" No possible matches.")

            return get_case(case_id)

        print(f" Found {len(matches)} possible match(es).")

        # 3. Agent chooses DISTANCE tool
        print("\n Agent decision: CHECK LOCATION")

        nearby_matches = []

        for item in matches:

            found_id = item[0]

            # Temporary demo coordinates
            found_lat = 13.0830
            found_lon = 80.2710

            distance_tool = self.tools["distance"]

            distance = distance_tool(
                lost_lat,
                lost_lon,
                found_lat,
                found_lon
            )

            print(
                f" Item #{found_id} → "
                f"{distance} meters away"
            )

            if distance <= 500:
                nearby_matches.append(
                    (found_id, distance)
                )

        # 4. Agent decides what to do next
        if nearby_matches:

            match_text = ", ".join(
                f"Item #{item_id} ({distance}m)"
                for item_id, distance in nearby_matches
            )

            update_case(
                case_id,
                "Nearby match found",
                match_text,
                "verification"
            )

            # Agent chooses NOTIFY tool
            print("\n Agent decision: NOTIFY")

            notify_tool = self.tools["notify"]

            notify_tool(
                user_name,
                f"Potential match found for your "
                f"{item_name}: {match_text}. "
                f"Please verify ownership."
            )

        else:

            update_case(
                case_id,
                "No nearby matches",
                "",
                "searching"
            )

            print("\n Agent decision: CONTINUE SEARCH")

        # 5. Retrieve memory
        print("\n Retrieving case memory...")

        return get_case(case_id)
    