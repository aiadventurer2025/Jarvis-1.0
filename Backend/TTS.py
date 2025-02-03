import pygame
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables from a .env file
env_vars = dotenv_values(".env")

AssistantVoice = env_vars.get("AssistantVoice")

async def TextToAudioFile(text) -> None:
    file_path = r"Backend\Data\speech.mp3"

    if os.path.exists(file_path):
        os.remove(file_path)

    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(r'Backend\Data\speech.mp3')

def TTS(Text, stop_func=lambda: False):
    try:
        asyncio.run(TextToAudioFile(Text))

        pygame.mixer.init()
        pygame.mixer.music.load(r"Backend\Data\speech.mp3")
        pygame.mixer.music.play()

        # Continuously check for the stop signal while playing
        while pygame.mixer.music.get_busy():
            if stop_func():  # If the stop signal is received, stop playback
                pygame.mixer.music.stop()
                print("Playback stopped.")
                break

            pygame.time.Clock().tick(10)  # Limit the loop to 10 ticks per second

    except Exception as e:
        print(f"Error in TTS: {e}")
    
    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in finally block: {e}")

def TextToSpeech(Text, stop_func=lambda: False):
    TTS(Text, stop_func)

