from fastapi import FastAPI, Form, File, UploadFile
import openai
import zipfile
import pandas as pd
from io import BytesIO

app = FastAPI()

import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("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")

@app.post("/api/")
async def answer_question(
    question: str = Form(...), file: UploadFile = None
):
    # Handle ZIP file (if uploaded)
    if file and file.filename.endswith(".zip"):
        with zipfile.ZipFile(BytesIO(await file.read()), 'r') as z:
            csv_file_name = [f for f in z.namelist() if f.endswith(".csv")][0]
            with z.open(csv_file_name) as f:
                df = pd.read_csv(f)

        # Extract value from the "answer" column
        if "answer" in df.columns:
            return {"answer": str(df["answer"].iloc[0])}

    # Use OpenAI's LLM to answer if no file is provided
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )

    return {"answer": response["choices"][0]["message"]["content"]}
