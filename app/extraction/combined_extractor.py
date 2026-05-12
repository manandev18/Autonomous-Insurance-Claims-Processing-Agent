from app.schemas.field_validators import (
    clean_llm_output,
    normalize_claim_type
)
from app.extraction.regex_extractor import (
    extract_fields
)

from app.extraction.llm_extractor import (
    extract_missing_fields
)

from app.validation.validator import (
    find_missing_fields
)

from app.schemas.field_validators import (
    clean_llm_output
)


def process_document(text):

    # STEP 1
    # REGEX EXTRACTION

    regex_data = extract_fields(text)

    # STEP 2
    # FIND MISSING FIELDS

    missing = find_missing_fields(
        regex_data
    )

    # STEP 3
    # REMOVE CLAIM TYPE FROM AI EXTRACTION

    if "claim_type" in missing:
        missing.remove("claim_type")

    # STEP 4
    # AI EXTRACTION

    llm_data = {}

    if missing:

        llm_data = extract_missing_fields(
            text,
            missing
        )

    # STEP 5
    # CLEAN AI OUTPUT

    llm_data = clean_llm_output(
        llm_data
    )

    # STEP 6
    # MERGE RESULTS

    final_data = {
        **regex_data,
        **llm_data
    }
    

    # STEP 7
    # CLAIM TYPE FALLBACK

    # STEP 7
# FORCE CLAIM TYPE NORMALIZATION

    claim_source = ""

# PRIORITY 1
# Existing claim type if present

    if final_data.get("claim_type"):

        claim_source = final_data["claim_type"]

# PRIORITY 2
# Asset type

    elif final_data.get("asset_type"):

        claim_source = final_data["asset_type"]

# PRIORITY 3
# Description fallback

    else:

        claim_source = final_data.get(
        "description",
        ""
    )

    normalized = normalize_claim_type(
    claim_source
)

    final_data["claim_type"] = normalized

    


    # STEP 7
    # CLAIM TYPE FALLBACK

    if not final_data.get("claim_type"):

        normalized = normalize_claim_type(
            final_data.get("description", "")
        )

        final_data["claim_type"] = normalized

    return final_data