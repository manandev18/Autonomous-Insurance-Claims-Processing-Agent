import re


FIELD_PATTERNS = {

    "policy_number":
    r'POLICY NUMBER\s*([A-Z0-9\-]+)',

    "policyholder_name":
    r'POLICYHOLDER NAME\s*(.+)',

    "effective_dates":
    r'EFFECTIVE DATES\s*(.+)',

    "incident_date":
    r'DATE OF LOSS\s*(\d{2}/\d{2}/\d{4})',

    "incident_time":
    r'TIME OF LOSS\s*(.+)',

    "incident_location":
    r'LOCATION OF LOSS\s*(.+)',


    "claimant":
    r'CLAIMANT\s*(.+)',

    "third_parties":
    r'THIRD PARTY\s*(.+)',

    "contact_details":
    r'CONTACT DETAILS\s*(.+)',

    "asset_type":
    r'ASSET TYPE\s*(.+)',

    "asset_id":
    r'ASSET ID\s*(.+)',

    "estimated_damage":
    r'ESTIMATED DAMAGE\s*\$?([\d,]+)',

    "claim_type":
    r'CLAIM TYPE\s*(.+)',

    "attachments":
    r'ATTACHMENTS\s*(.+)',

    "initial_estimate":
    r'INITIAL ESTIMATE\s*\$?([\d,]+)'
}


def extract_fields(text):

    data = {}

    for field, pattern in FIELD_PATTERNS.items():

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            data[field] = match.group(1).strip()
    description = extract_description(text)

    if description:
        data["description"] = description

    return data

def extract_description(text):

    lines = text.splitlines()

    for i, line in enumerate(lines):

        if "DESCRIPTION" in line.upper():

            # SAME LINE CASE

            parts = line.split("DESCRIPTION")

            if len(parts) > 1:

                possible = parts[-1].strip()

                if possible:
                    return possible

            # NEXT LINES CASE

            description_lines = []

            for next_line in lines[i+1:]:

                clean = next_line.strip()

                # STOP at next section-like line

                if (
                    clean.isupper()
                    or clean.startswith("CLAIMANT")
                    or clean.startswith("ASSET")
                    or clean.startswith("CONTACT")
                ):
                    break

                if clean:
                    description_lines.append(clean)

            return " ".join(description_lines)

    return None