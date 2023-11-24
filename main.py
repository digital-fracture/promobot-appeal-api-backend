import csv
import io

import aiofiles
import aiocsv
from charset_normalizer import from_bytes

from fastapi import FastAPI, UploadFile, Body
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from promobot_appeal_processing import predict_async, predict_many

from logic.database import database
from misc.util import get_temp_file_path, prediction_to_csv_dict
from misc.config import field_name_mapping


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    await database.create()


@app.on_event("shutdown")
async def startup():
    await database.close()


@app.get("/")
async def index():
    return {"message": "I <3 Scarlett"}


@app.post("/api")
async def api(text: str = Body(embed=True)):
    prediction = await predict_async(text)
    await database.insert_appeal(text, prediction)
    await database.commit()

    return prediction


@app.post("/file")
async def file(file: UploadFile):
    contents = str(from_bytes(await file.read()).best()).strip()
    csv_reader = csv.DictReader(io.StringIO(contents), delimiter=";")
    texts = tuple(map(lambda row: row["Текст инцидента"], csv_reader))

    predictions = await predict_many(texts, max_workers=4)

    async with aiofiles.open(path := get_temp_file_path("csv"), "w", encoding="utf-8") as out_file:
        csv_writer = aiocsv.AsyncDictWriter(
            out_file,
            fieldnames=[*csv_reader.fieldnames, *tuple(field_name_mapping.values())]
        )
        await csv_writer.writeheader()

        for text, prediction in zip(texts, predictions):
            await database.insert_appeal(text, prediction)
            await csv_writer.writerow(prediction_to_csv_dict(text, prediction))

        await database.commit()

    return FileResponse(
        path,
        media_type="text/csv",
        filename="predictions.csv"
    )


@app.get("/history")
async def history():
    return await database.fetch_non_processed_appeals()


@app.put("/mark_processed")
async def mark_processed(id: int = Body(embed=True)):
    await database.mark_processed(id)
    return {"message": "success"}
