def verify_ownership(
    user_detail,
    expected_detail
):
    """
    Verify whether the user's identifying detail
    matches the stored item detail.
    """

    user_detail = user_detail.lower().strip()
    expected_detail = expected_detail.lower().strip()

    if user_detail == expected_detail:

        return {
            "verified": True,
            "message": "Ownership successfully verified."
        }

    else:

        return {
            "verified": False,
            "message": "Ownership could not be verified."
        }