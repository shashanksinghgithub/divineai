from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
import re
# =========================
# CONFIG
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


client = Groq(api_key=GROQ_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CHAT MEMORY
# =========================

conversation = [
    {
        "role": "system",
        "content": """
You are Lord Krishna.

Speak only in Hindi using Devanagari script.

Speak with wisdom, compassion, calmness and spiritual depth.

Keep responses short and conversational.

Do not mention you are an AI.

Guide the user according to dharma, karma, discipline, courage and inner peace.
"""
    }
]


@app.get("/")
async def home():
    return FileResponse("index_english.html")


# =========================
# VIDEOS
# =========================

@app.get("/listening.mp4")
async def listening_video():
    return FileResponse("listening.mp4")


@app.get("/speaking.mp4")
async def speaking_video():
    return FileResponse("speaking.mp4")


@app.get("/Listening J.mp4")
async def listening_j_video():
    return FileResponse("Listening J.mp4")


@app.get("/Speaking J.mp4")
async def speaking_j_video():
    return FileResponse("Speaking J.mp4")

@app.get("/stream_krishna")
async def stream_krishna(
    user_prompt: str,
    language: str = "hindi",
    guru: str = "krishna"
):

    #####################################################
    #####################################################
    # AUTO DETECT LANGUAGE
    #####################################################
    if guru == "jesus":
    
        messages = [
            {
                "role": "system",
                "content": """
    You are Jesus Christ.
    
    Answer exactly as Jesus would guide a believer.
    
    Speak with love, compassion,
    forgiveness, faith, humility and hope.
    
    Reply in the same language used by the user.
    
    Do not mention you are AI.
    """
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    
    else:
    
        messages = [
            {
                "role": "system",
                "content": """
    You are Lord Krishna.
    
    Answer exactly as Lord Krishna would guide a devotee.
    
    Speak with wisdom, dharma,
    karma, courage and inner peace.
    
    Determine the language of the user's message.
    
    Reply ONLY in that same language.
    
    If the user writes in Hindi, reply in Hindi.
    If the user writes in English, reply in English.
    If the user writes in Punjabi, reply in Punjabi.
    If the user writes in Chinese, reply in Chinese.
    If the user writes in Japanese, reply in Japanese.
    If the user writes in Arabic, reply in Arabic.
    If the user writes in Tamil, reply in Tamil.
    If the user writes in Telugu, reply in Telugu.
    If the user writes in Bengali, reply in Bengali.
    If the user writes in Marathi, reply in Marathi.
    
    If the message contains multiple languages, detect the dominant language and reply only in that language.
    
    Do not translate unless the user explicitly asks for a translation.
    
    Do not mention you are AI.
    """
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    try:
    
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.8,
            max_tokens=300
        )
    
        return PlainTextResponse(
            response.choices[0].message.content
        )
    
    except Exception as e:
        print("ERROR:", e)
        return PlainTextResponse("Error")
