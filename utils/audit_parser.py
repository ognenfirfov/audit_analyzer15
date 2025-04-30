from openai import OpenAI
import fitz  # PyMuPDF
import pandas as pd
import os
import time
from openai import RateLimitError

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def ask_ai_to_summarize(text):
    prompt = f"""You are an audit report analyzer. Given the following audit report, extract the following:
    - Main Audit Topic
    - Main Findings
    - Measures Taken
    - Recommended Next Steps

Report:
{text}

Return in this format:
Main Audit Topic: ...
Main Findings: ...
Measures Taken: ...
Next Steps: ...
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        return response.choices[0].message.content
    except RateLimitError:
        return "⚠️ Rate limit exceeded. Please wait and try again later."
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

def process_audits(file_paths):
    data = []
    for i, path in enumerate(file_paths):
        text = extract_text_from_pdf(path)
        summary = ask_ai_to_summarize(text)
        time.sleep(1)  # Add delay between API calls to reduce rate limiting risk

        # Parse structured summary
        summary_lines = summary.splitlines()
        parsed = {"Company": f"Audit {i+1}"}
        for line in summary_lines:
            if ":" in line:
                key, val = line.split(":", 1)
                parsed[key.strip()] = val.strip()
        data.append(parsed)

    return pd.DataFrame(data)
