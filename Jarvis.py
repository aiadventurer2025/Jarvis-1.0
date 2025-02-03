from  Backend import TTS, STT, Brain
from Functions import GerenalChat, RealTimeInformation, SimpleActions
from colorama import Fore
import time

def handle_command(Querry):
    print(Fore.WHITE + "User : ", Querry)
    Category = Brain.FirstLayerDMX(Querry)

    if Category == ['General']:
        Output = GerenalChat.ChatBot(Querry)
        print(Fore.YELLOW + "JARVIS : ", Output)
        TTS.TextToSpeech(Output)

    elif Category == ['Realtime']:
        Output = RealTimeInformation.RealtimeSearchEngine(Querry)
        print(Fore.YELLOW + "JARVIS : "+ Output, Output)
        TTS.TextToSpeech(Output)

    elif Category == ['SimpleAutomation']:
        SimpleActions.execute_code(Querry)

    else:
        print(type(Category), Category)

def main_loop():
    print(Fore.GREEN + "System: Say JARVIS to start...")
    while True:
        try:
            command = STT.SpeechRecognition()
            if command:
                handle_command(command)
            else:
                print(Fore.RED + "System: Deactivated. Say 'Jarvis' to reactivate")
        except Exception as e:
            print(Fore.RED + f"System Error: {e}")
            print(Fore.YELLOW + "Restarting recognition system...")
            time.sleep(2)  # Wait before restarting

if __name__ == "__main__":
    main_loop()