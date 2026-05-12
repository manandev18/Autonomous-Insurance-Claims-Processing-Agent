VALID_CLAIM_TYPES = [
    "vehicle",
    "injury",
    "property"
]


def normalize_claim_type(value):

    if not value:
        return None

    value = str(value).lower()

    # VEHICLE

    if (
        "vehicle" in value
        or "collision" in value
        or "car" in value
        or "rear-end" in value
        or "accident" in value
    ):

        return "vehicle"

    # INJURY

    if (
        "injury" in value
        or "hospital" in value
        or "medical" in value
        or "bodily" in value
    ):

        return "injury"

    # PROPERTY

    if (
        "property" in value
        or "building" in value
        or "home" in value
    ):

        return "property"

    return None


def validate_estimated_damage(value):

    try:

        float(
            str(value).replace(",", "")
        )

        return True

    except:

        return False


def validate_contact_details(value):

    value = str(value)

    return (
        "@" in value
        or value.isdigit()
    )


def clean_llm_output(data):

    # CLAIM TYPE

    if "claim_type" in data:

        normalized = normalize_claim_type(
            data["claim_type"]
        )

        data["claim_type"] = normalized

    # ESTIMATED DAMAGE

    if "estimated_damage" in data:

        if not validate_estimated_damage(
            data["estimated_damage"]
        ):

            data["estimated_damage"] = None

    # CONTACT DETAILS

    if "contact_details" in data:

        if not validate_contact_details(
            data["contact_details"]
        ):

            data["contact_details"] = None

    return data