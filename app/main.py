import json
import os

from fastapi import FastAPI, UploadFile, File

from app.parser.pdf_parser import (
    extract_text_from_pdf
)

from app.parser.text_parser import (
    extract_text_from_txt
)

from app.extraction.combined_extractor import (
    process_document
)

from app.validation.validator import (
    find_missing_fields
)

from app.routing.router import (
    determine_route
)


app = FastAPI(
    title="Insurance Claims Processing Agent"
)


@app.post("/process-claim")

async def process_claim(
    file: UploadFile = File(...)
):

    # SAVE TEMP FILE

    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # DETECT FILE TYPE

    extension = file.filename.split(".")[-1]

    # PARSE DOCUMENT

    if extension == "pdf":

        text = extract_text_from_pdf(
            temp_path
        )

    elif extension == "txt":

        text = extract_text_from_txt(
            temp_path
        )

    else:

        os.remove(temp_path)

        return {
            "error": "Unsupported file type"
        }

    # EXTRACTION

    data = process_document(text)

    # VALIDATION

    missing_fields = find_missing_fields(
        data
    )

    # ROUTING

    route, reasoning = determine_route(
        data,
        missing_fields
    )

    # CLEANUP

    os.remove(temp_path)

    # FINAL OUTPUT

    output = {

        "extractedFields": data,

        "missingFields": missing_fields,

        "recommendedRoute": route,

        "reasoning": reasoning
    }

    return output