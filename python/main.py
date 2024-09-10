import cv2
import mediapipe as mp
import numpy as np
from location import *
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import pygame
import time
from routes.combine import multiThreadingCalls
import threading


app = FastAPI()

stopAnalysis = threading.Event()
pygame.mixer.init()
music = pygame.mixer.Sound('./assets/iphone_14.mp3')  # Use Sound for shorter clips

origins = ["http://localhost:5500"] 
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/playMusic")
async def play_music(background_tasks: BackgroundTasks):
    background_tasks.add_task(play_background_music)
    return {"message": "Music playback started"}

def play_background_music():
    music.play()
    while music.get_busy():
        time.sleep(0.1)  

@app.get("/stopMusic")
async def stopMusic(backgroundTasks: BackgroundTasks):
    backgroundTasks.add_task(stopMusic)
    return {"message":"Music is stopped"}
def stopMusic():
    music.stop()

@app.get("/startDetection")
async def startThreat(backgroundTask: BackgroundTasks):
    stopAnalysis.clear()
    backgroundTask.add_task(multiThreadingCalls, stopAnalysis)
    return {"message":"Threat detection started"}

@app.get("/stopDetection")
async def stopThreat():
    stopAnalysis.set()
    return {"message":"Analysis is stopped"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000)

