FRAUD_KEYWORDS = [
    "fraud",
    "inconsistent",
    "staged"
]
def determine_route(data, missing_fields):

    description = str(
        data.get("description", "")
    ).lower()

    claim_type = str(
        data.get("claim_type", "")
    ).lower()

    estimated_damage = data.get(
        "estimated_damage",
        0
    )

    try:
        estimated_damage = float(
            str(estimated_damage).replace(",", "")
        )

    except:
        estimated_damage = 0

    # RULE 1
    # Investigation Flag

    for keyword in FRAUD_KEYWORDS:

        if keyword in description:

            return (
                "Investigation Flag",
                f"Detected suspicious keyword: {keyword}"
            )

    # RULE 2
    # Manual Review

    if missing_fields:

        return (
            "Manual Review",
            "Mandatory fields are missing"
        )

    # RULE 3
    # Specialist Queue

    if claim_type == "injury":

        return (
            "Specialist Queue",
            "Injury claims require specialist handling"
        )

    # RULE 4
    # Fast-track

    if estimated_damage < 25000:

        return (
            "Fast-track",
            "Estimated damage below threshold"
        )

    # DEFAULT

    return (
        "Standard Processing",
        "No special routing conditions met"
    )