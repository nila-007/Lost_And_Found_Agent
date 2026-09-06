from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.llm_agent import run_agent
from app.database import get_connection
from app.memory.case_memory import create_case, get_case, update_case
from app.tools.search_tools import search_found_items
from app.tools.location_tool import calculate_distance
from app.tools.matching_tool import calculate_match_score
from app.tools.notification_tool import send_notification
from app.tools.verification_tool import verify_ownership
app = FastAPI(
    title="LOSTIQ API",
    description="Autonomous Lost and Found Recovery System",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# REQUEST MODELS
# ==========================================

class LostItemRequest(BaseModel):
    item_name: str
    description: str
    location: str
    lost_date_time: str


class FoundItemRequest(BaseModel):
    item_name: str
    category: str
    description: str
    location: str
    found_date_time: str


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "LOSTIQ API is running",
        "status": "active"
    }


# ==========================================
# REPORT LOST ITEM
# ==========================================

@app.post("/report-lost")
def report_lost_item(item: LostItemRequest):

    case_id = create_case(
        item.item_name,
        item.description,
        item.location,
        item.lost_date_time
    )

    return {
        "message": "Lost item reported successfully",
        "case_id": case_id,
        "status": "searching"
    }


# ==========================================
# REPORT FOUND ITEM
# ==========================================

@app.post("/report-found")
def report_found_item(item: FoundItemRequest):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO found_items
        (item_name, category, description, location, found_date_time)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            item.item_name,
            item.category,
            item.description,
            item.location,
            item.found_date_time
        )
    )

    item_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "message": "Found item reported successfully",
        "item_id": item_id,
        "status": "found"
    }


# ==========================================
# GET FOUND ITEMS
# ==========================================

@app.get("/found-items")
def get_found_items():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            item_name,
            category,
            description,
            location,
            found_date_time,
            status
        FROM found_items
        """
    )

    rows = cursor.fetchall()

    connection.close()

    items = []

    for row in rows:

        items.append({
            "id": row[0],
            "item_name": row[1],
            "category": row[2],
            "description": row[3],
            "location": row[4],
            "found_date_time": row[5],
            "status": row[6]
        })

    return {
        "count": len(items),
        "items": items
    }


# ==========================================
# GET CASE
# ==========================================

@app.get("/case/{case_id}")
def get_case_details(case_id: int):

    case = get_case(case_id)

    if case is None:

        return {
            "error": "Case not found"
        }

    return {
        "case_id": case[0],
        "item_name": case[1],
        "description": case[2],
        "lost_location": case[3],
        "lost_date_time": case[4],
        "status": case[5],
        "current_step": case[6],
        "possible_matches": case[7],
        "last_updated": case[8]
    }
# ==========================================
# INVESTIGATE LOST ITEM
# ==========================================

@app.post("/investigate/{case_id}")
def investigate_case(case_id: int):

    case = get_case(case_id)

    if case is None:
        return {
            "error": "Case not found"
        }

    case_item = case[1]
    case_description = case[2]
    case_location = case[3]

    # SEARCH
    search_keyword = case_item

    results = search_found_items(search_keyword)

    if not results:

        update_case(
            case_id,
            "Search completed - no match found",
            "",
            "searching"
        )

        return {
            "case_id": case_id,
            "status": "no_match",
            "message": "No matching found item was discovered."
        }

    # FIRST CANDIDATE
    found = results[0]

    found_item = {
        "item_name": found[1],
        "category": found[2],
        "description": found[3],
        "location": found[4]
    }

    # DEMO LOCATION
    lost_lat = 13.0827
    lost_lon = 80.2707

    found_lat = 13.0830
    found_lon = 80.2710

    # DISTANCE
    distance = calculate_distance(
        lost_lat,
        lost_lon,
        found_lat,
        found_lon
    )

    # MATCH SCORE
    match_result = calculate_match_score(
        case_item,
        case_description,
        case_location,
        found_item,
        distance
    )

    update_case(
        case_id,
        f"Match score calculated: {match_result['score']}/100",
        f"Item #{found[0]}",
        "searching"
    )

    # NOTIFICATION
    if (
        match_result["level"] == "STRONG MATCH"
        and distance <= 500
    ):

        send_notification(
            "Student",
            f"Potential match found for your {case_item}. "
            f"Match score: {match_result['score']}%. "
            f"Distance: {distance} meters. "
            f"Please verify ownership."
        )

        update_case(
            case_id,
            "Notification sent",
            f"Item #{found[0]}",
            "verification"
        )

    return {
        "case_id": case_id,
        "status": "verification",
        "match": {
            "item_id": found[0],
            "item_name": found[1],
            "description": found[3],
            "location": found[4],
            "distance_meters": distance,
            "score": match_result["score"],
            "level": match_result["level"],
            "factors": match_result["factors"]
        }
    }# ==========================================
# VERIFY OWNERSHIP
# ==========================================

class VerificationRequest(BaseModel):

    user_detail: str


@app.post("/verify/{case_id}")
def verify_case(case_id: int, request: VerificationRequest):

    case = get_case(case_id)

    if case is None:
        return {
            "error": "Case not found"
        }

    result = verify_ownership(
        request.user_detail,
        "Blue ID card"
    )

    if result["verified"]:

        update_case(
            case_id,
            "Ownership verified",
            "Item #1",
            "verified"
        )

        return {
            "case_id": case_id,
            "status": "verified",
            "message": result["message"]
        }

    else:

        update_case(
            case_id,
            "Ownership verification failed",
            "Item #1",
            "verification"
        )

        return {
            "case_id": case_id,
            "status": "verification",
            "message": result["message"]
        }
@app.post("/ai-investigate/{case_id}")
def ai_investigate_case(case_id: int):

    case = get_case(case_id)

    if case is None:
        return {
            "error": "Case not found"
        }

    result = run_agent(
        case_id=case_id,
        item_name=case[1],
        description=case[2],
        location=case[3],
        lost_date_time=case[4],
        user_name="Student"
    )

    return {
        "case_id": case_id,
        "status": "completed",
        "agent_result": result
    }