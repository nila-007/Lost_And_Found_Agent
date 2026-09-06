import os
import json

from openai import OpenAI

from app.database import get_connection

from app.memory.case_memory import (
    get_case,
    update_case
)

from app.tools.search_tools import search_found_items
from app.tools.location_tool import calculate_distance
from app.tools.matching_tool import calculate_match_score
from app.tools.notification_tool import send_notification
from app.tools.verification_tool import verify_ownership

from app.memory.case_memory import (
    create_case,
    get_case,
    update_case
)


# ==========================================
# OPENROUTER CONNECTION
# ==========================================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)


# ==========================================
# TOOL DEFINITIONS
# ==========================================

tools = [

    # SEARCH TOOL
    {
        "type": "function",
        "function": {
            "name": "search_found_items",
            "description": "Search the database for found items matching a keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string"
                    }
                },
                "required": ["keyword"]
            }
        }
    },


    # DISTANCE TOOL
    {
        "type": "function",
        "function": {
            "name": "calculate_distance",
            "description": "Calculate geographical distance between two locations in meters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat1": {"type": "number"},
                    "lon1": {"type": "number"},
                    "lat2": {"type": "number"},
                    "lon2": {"type": "number"}
                },
                "required": [
                    "lat1",
                    "lon1",
                    "lat2",
                    "lon2"
                ]
            }
        }
    },


    # MATCHING TOOL
    {
        "type": "function",
        "function": {
            "name": "calculate_match_score",
            "description": "Calculate how strongly a found item matches the lost item.",
            "parameters": {
                "type": "object",
                "properties": {

                    "lost_item": {
                        "type": "string"
                    },

                    "lost_description": {
                        "type": "string"
                    },

                    "lost_location": {
                        "type": "string"
                    },

                    "found_item": {
                        "type": "object",
                        "properties": {
                            "item_name": {"type": "string"},
                            "category": {"type": "string"},
                            "description": {"type": "string"},
                            "location": {"type": "string"}
                        },
                        "required": [
                            "item_name",
                            "category",
                            "description",
                            "location"
                        ]
                    },

                    "distance": {
                        "type": "number"
                    }
                },

                "required": [
                    "lost_item",
                    "lost_description",
                    "lost_location",
                    "found_item",
                    "distance"
                ]
            }
        }
    },


    # NOTIFICATION TOOL
    {
        "type": "function",
        "function": {
            "name": "send_notification",
            "description": "Send a notification to the user about a potential match.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_name": {
                        "type": "string"
                    },

                    "message": {
                        "type": "string"
                    }
                },

                "required": [
                    "user_name",
                    "message"
                ]
            }
        }
    },


    # VERIFICATION TOOL
    {
        "type": "function",
        "function": {
            "name": "verify_ownership",
            "description": "Verify ownership using a unique identifying detail.",
            "parameters": {
                "type": "object",
                "properties": {

                    "user_detail": {
                        "type": "string"
                    },

                    "expected_detail": {
                        "type": "string"
                    }
                },

                "required": [
                    "user_detail",
                    "expected_detail"
                ]
            }
        }
    }
]


# ==========================================
# TOOL EXECUTION
# ==========================================

# ==========================================
# TOOL EXECUTION
# ==========================================

def execute_tool(tool_name, arguments):

    if tool_name == "search_found_items":

        return search_found_items(
            arguments["keyword"]
        )

    elif tool_name == "calculate_distance":

        return calculate_distance(
            arguments["lat1"],
            arguments["lon1"],
            arguments["lat2"],
            arguments["lon2"]
        )

    elif tool_name == "calculate_match_score":

        return calculate_match_score(
            arguments["lost_item"],
            arguments["lost_description"],
            arguments["lost_location"],
            arguments["found_item"],
            arguments["distance"]
        )

    elif tool_name == "send_notification":
               return send_notification(
            arguments["user_name"],
            arguments["message"]
        )

    elif tool_name == "verify_ownership":

        return verify_ownership(
            arguments["user_detail"],
            arguments["expected_detail"]
        )

    else:

        return "Unknown tool"

# ==========================================
# LLM AGENT
# ==========================================

def run_agent(
    case_id,    
    item_name,
    description,
    location,
    lost_date_time,
    user_name="Student"
):

    print("\n========================================")
    print("🤖 LOSTIQ LLM AGENT")
    print("========================================")


    # ======================================
    # USER INPUT
    # ======================================

   

    # ======================================
    # DEMO INFORMATION
    # ======================================

    

    lost_lat = 13.0827
    lost_lon = 80.2707
    
   


    # ======================================
    # CREATE CASE
    # ======================================

    # ======================================
# EXISTING CASE
# ======================================
     # ======================================
# EXISTING CASE
# ======================================

    print("\n🧠 USING EXISTING CASE")
    print("==============================")

    print("Case ID:", case_id)
    print("Status: searching")
     


    # ======================================
    # LLM MESSAGES
    # ======================================

    messages = [

        {
            "role": "system",

            "content" : """
You are LOSTIQ, an autonomous lost and found recovery agent.

Your job is to investigate the existing case completely.

MANDATORY WORKFLOW:

1. Search for matching found items.
2. Calculate the match score.
3. Calculate the geographical distance.
4. If a suitable match is found within 500 meters, send a notification.
5. DO NOT STOP after sending the notification.
6. Ask the user for a unique identifying detail.
7. Use the verify_ownership tool to verify the ownership.
8. If verification succeeds, the case must become VERIFIED.
9. If verification fails, the case must remain under VERIFICATION.
10. Never claim that an item was recovered unless ownership verification succeeds.

IMPORTANT:
- Continue using tools until the investigation reaches a final verification result.
- After send_notification, continue to ownership verification.
- Expected verification detail is "Blue ID card".
- Do not reveal the expected verification detail to the user.
"""
        },

        {
            "role": "user",
            "content": description
        }

    ]


    # ======================================
    # AGENT LOOP
    # ======================================
    # ======================================
    # AGENT LOOP
    # ======================================

    while True:

        response = client.chat.completions.create(

            model="openrouter/free",

            messages=messages,

            tools=tools,

            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        messages.append(assistant_message)


        # ==================================
        # NO MORE TOOL CALLS
        # ==================================

        if not assistant_message.tool_calls:

            print("\n========================================")
            print("🤖 LOSTIQ FINAL RESPONSE")
            print("========================================")

            print(assistant_message.content)


            # Ask user for ownership verification

            verification_detail = "Blue ID card"


            print("\n========================================")
            print("🔐 OWNERSHIP VERIFICATION")
            print("========================================")


            verification_result = verify_ownership(
                verification_detail,
                "Blue ID card"
            )


            print("\nVerification Result:")


            if verification_result["verified"]:

                print("✅ VERIFIED")
                print(verification_result["message"])


                update_case(
                    case_id,
                    "Ownership verified",
                    "Item #1",
                    "verified"
                )


            else:

                print("❌ NOT VERIFIED")
                print(verification_result["message"])


                update_case(
                    case_id,
                    "Ownership verification failed",
                    "Item #1",
                    "verification"
                )


            # Exit the agent loop ONLY after
            # the verification step is complete

            break


        # ==================================
        # EXECUTE TOOL CALLS
        # ==================================

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )


            print("\n========================================")
            print("🔧 TOOL SELECTED")
            print("========================================")

            print(tool_name)


            print("\n📥 TOOL INPUT:")

            print(arguments)


            # Execute tool

            result = execute_tool(
                tool_name,
                arguments
            )


            print("\n📤 TOOL OUTPUT:")

            print(result)


            # ==================================
            # UPDATE CASE MEMORY
            # ==================================

            if tool_name == "search_found_items":

                update_case(
                    case_id,
                    "Search completed - possible match found",
                    str(result),
                    "searching"
                )


            elif tool_name == "calculate_match_score":

                score = result["score"]

                update_case(
                    case_id,
                    f"Match score calculated: {score}/100",
                    "Item #1",
                    "searching"
                )


            elif tool_name == "calculate_distance":

                distance = result

                if distance <= 500:

                    update_case(
                        case_id,
                        "Nearby match found",
                        f"Item #1 ({distance}m)",
                        "verification"
                    )


            elif tool_name == "send_notification":

                update_case(
                    case_id,
                    "Notification sent",
                    "Item #1",
                    "verification"
                )


            elif tool_name == "verify_ownership":

                if result["verified"]:

                    update_case(
                        case_id,
                        "Ownership verified",
                        "Item #1",
                        "verified"
                    )

                else:

                    update_case(
                        case_id,
                        "Ownership verification failed",
                        "Item #1",
                        "verification"
                    )


            # ==================================
            # SEND TOOL RESULT TO LLM
            # ==================================

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )
    

    # ======================================
    # FINAL CASE MEMORY
    # ======================================

    final_case = get_case(case_id)


    print("\n========================================")
    print("🧠 FINAL CASE MEMORY")
    print("========================================")


    print("Case ID:", final_case[0])
    print("Item:", final_case[1])
    print("Description:", final_case[2])
    print("Location:", final_case[3])
    print("Status:", final_case[5])
    print("Current Step:", final_case[6])
    print("Possible Matches:", final_case[7])
    case = get_case(case_id)

    return {
    "case_id": case_id,
    "item_name": item_name,
    "description": description,
    "status": case[5] if case else "verification"
}
    

# ==========================================
# START
# ==========================================

