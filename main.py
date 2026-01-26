from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Dynamusic API", version="1.0.0")

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
    return {
        "status": "Dynamusic API live",
        "version": "1.0.0",
        "available_segments": list(SEGMENTS.keys())
    }

@app.get("/segments")
def list_segments():
    """List all available audio segments"""
    return {
        "segments": SEGMENTS
    }

@app.post("/get-audio")
def get_audio(req: AudioRequest):
    """Get personalized audio based on segment"""
    audio = SEGMENTS.get(req.segment_id, SEGMENTS["young_energy"])
    return {
        "campaign_id": req.campaign_id,
        "segment_id": req.segment_id,
        "creative_id": req.creative_id,
        "audio_url": audio["audio_url"],
        "description": audio["description"]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
