import ollama
import json
import re
import os

def extract_missing_fields(
    document_text,
    missing_fields
):

    prompt = f"""
You are an expert insurance First Notice of Loss (FNOL) semantic inference engine with deep knowledge of insurance claim processing, policy structures, and loss assessment procedures.

Your task is to analyze the provided FNOL document and infer values for missing fields using contextual reasoning, domain expertise, and semantic understanding.

═══════════════════════════════════════
INFERENCE RULES
═══════════════════════════════════════

1. CONTEXTUAL INFERENCE
   - Cross-reference all available fields to infer missing ones
   - Use timestamps, locations, descriptions, and named entities as inference signals
   - Apply insurance domain knowledge (e.g., loss type → coverage type, vehicle year → depreciation bracket)

2. CONFIDENCE SCORING
   - 0.90–1.00 → Explicitly stated or mathematically derived
   - 0.70–0.89 → Strongly implied by context or standard practice
   - 0.50–0.69 → Reasonable inference with some ambiguity
   - 0.30–0.49 → Speculative; multiple interpretations possible
   - 0.00–0.29 → Weak signal; return null instead unless partial value is useful

3. DATA INTEGRITY
   - Never fabricate policy numbers, claim IDs, phone numbers, or monetary values not grounded in the document
   - Do not assume claimant identity without textual evidence
   - If a field could have multiple valid values, pick the most probable and reflect uncertainty in the confidence score

4. FIELD-SPECIFIC GUIDANCE
   - Dates: Normalize to ISO 8601 format (YYYY-MM-DD); infer from event descriptions if explicit date is absent
   - Monetary values: Return as numeric strings without currency symbols; use document currency context
   - Enumerations (e.g., loss_type, coverage_type): Map to closest standard insurance taxonomy value
   - Boolean fields: Return true/false strings, not 1/0
   - Names: Use "Last, First" format unless document convention differs

5. NULL HANDLING
   - Return null (not "", not "unknown", not "N/A") when inference confidence would be below 0.30
   - Never guess PII (SSN, DOB, license numbers) without direct document evidence

═══════════════════════════════════════
OUTPUT FORMAT (STRICT JSON ONLY)
═══════════════════════════════════════

Return a single flat JSON object. No preamble, no explanation, no markdown fences.

{{
  "field_name": {{
    "value": <inferred value or null>,
    "confidence": <float between 0.00 and 1.00>,
    "inference_basis": "<one short phrase explaining the signal used, e.g., 'derived from incident timestamp' or 'standard liability default for auto collision'>"
  }}
}}

═══════════════════════════════════════
MISSING FIELDS TO INFER
═══════════════════════════════════════

{missing_fields}

═══════════════════════════════════════
FNOL DOCUMENT
═══════════════════════════════════════

{document_text}

═══════════════════════════════════════
BEGIN INFERENCE — OUTPUT JSON ONLY
═══════════════════════════════════════
"""

    client = ollama.Client(

        host=os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434"
        )
    )

    try:

        response = client.chat(

        model='phi3:mini',

        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],

        options={
            "num_predict": 100,
            "temperature": 0
        }
    )

    except Exception as e:

        print(f"Ollama Error: {e}")

        return {}

    content = response['message']['content']

    return parse_json(content)


def parse_json(text):

    match = re.search(
        r'\{.*\}',
        text,
        re.DOTALL
    )

    if match:

        try:
            return json.loads(match.group())

        except:
            return {}

    return {}