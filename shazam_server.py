from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from shazamio import Shazam, Serialize
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ShazamIO API")

# Allow CORS for Vue frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to your Vue app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/recognize")
async def recognize_song(file: UploadFile = File(...)):
    try:
        # Create a new Shazam instance for each request to ensure thread safety in async context
        # Or you can manage a global instance if it supports it, but per-request is safer here
        shazam = Shazam()

        # Read the uploaded file content
        content = await file.read()
        logger.info(f"Received audio file of size: {len(content)} bytes")

        # Recognize the song
        out = await shazam.recognize(content)

        # Serialize the result using the built-in serializer
        serialized = Serialize.full_track(out)

        return serialized
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
