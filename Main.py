from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SEGMENTS = {
    "young_energy": {
        "description": "Electronic upbeat tag (young energy)",
        "audio_url": "https://dyna-assets.s3.eu-north-1.amazonaws.com/audio/Electronic.mp3"
    },
    "rock": {
        "description": "Feel good Rock version",
        "audio_url": "https://dyna-assets.s3.eu-north-1.amazonaws.com/audio/Rock.mp3"
    },
    "late_night": {
        "description": "Late Night Classical",
        "audio_url": "https://dyna-assets.s3.eu-north-1.amazonaws.com/audio/Classical+Demo.mp3"
    }
}

class AudioRequest(BaseModel):
    campaign_id: str
    segment_id: str
    creative_id: str

@app.get("/")
def health():
    return {"status": "Dynamusic API live"}

@app.post("/get-audio")
def get_audio(req: AudioRequest):
    audio = SEGMENTS.get(req.segment_id, SEGMENTS["young_energy"])
    return {
        "campaign_id": req.campaign_id,
        "segment_id": req.segment_id,
        "audio_url": audio["audio_url"],
        "description": audio["description"]
    }
