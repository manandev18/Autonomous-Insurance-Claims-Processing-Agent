MANDATORY_FIELDS = [

    "policy_number",
    "policyholder_name",

    "incident_date",
    "incident_location",
    "description",

    "claimant",

    "asset_type",
    "estimated_damage",

    "claim_type",
    "initial_estimate"
]

def find_missing_fields(data):

    missing_fields = []

    for field in MANDATORY_FIELDS:

        value = data.get(field)

        if (
            value is None
            or value == ""
            or str(value).strip() == ""
        ):
            missing_fields.append(field)

    return missing_fields