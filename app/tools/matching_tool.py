def calculate_match_score(
    lost_item,
    lost_description,
    lost_location,
    found_item,
    distance
):

    score = 0
    factors = []


    # ==========================================
    # ITEM NAME MATCH
    # ==========================================

    lost_name = lost_item.lower()
    found_name = found_item["item_name"].lower()

    if lost_name in found_name or found_name in lost_name:
        score += 25
        factors.append("Item name matches")


    # ==========================================
    # CATEGORY MATCH
    # ==========================================

    if lost_name == found_item["category"].lower():
        score += 15
        factors.append("Category matches")


    # ==========================================
    # DESCRIPTION MATCH
    # ==========================================

    lost_words = set(
        lost_description.lower().split()
    )

    found_words = set(
        found_item["description"].lower().split()
    )

    common_words = lost_words.intersection(found_words)

    if len(common_words) >= 3:
        score += 30
        factors.append("Multiple description details match")

    elif len(common_words) >= 1:
        score += 15
        factors.append("Description has matching details")


    # ==========================================
    # LOCATION MATCH
    # ==========================================

    if (
        lost_location.lower()
        == found_item["location"].lower()
    ):
        score += 15
        factors.append("Location matches")


    # ==========================================
    # DISTANCE
    # ==========================================

    if distance <= 100:
        score += 15
        factors.append("Very close location")

    elif distance <= 500:
        score += 10
        factors.append("Nearby location")


    # ==========================================
    # MATCH LEVEL
    # ==========================================

    if score >= 80:
        level = "STRONG MATCH"

    elif score >= 50:
        level = "POSSIBLE MATCH"

    else:
        level = "WEAK MATCH"


    return {
        "score": score,
        "level": level,
        "factors": factors
    }