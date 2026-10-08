import os
import webbrowser
import pywhatkit
import psutil
import requests
import pyautogui
import socket
import ctypes
import winshell

from datetime import datetime


def execute_command(user_text):

    text = user_text.lower()

    # OPEN CHROME

    if "open chrome" in text:

        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

        os.startfile(chrome_path)

        return "Opening Chrome"

    # OPEN VS CODE

    if (
        "open vs code" in text
        or "open vscode" in text
        or "open visual studio code" in text
    ):

        vscode_path = r"C:\Users\abhij\AppData\Local\Programs\Microsoft VS Code\Code.exe"

        os.startfile(vscode_path)

        return "Opening VS Code"

    # OPEN NOTEPAD

    if "open notepad" in text:

        os.system("notepad")

        return "Opening Notepad"

    # OPEN CALCULATOR

    if "open calculator" in text:

        os.system("calc")

        return "Opening Calculator"

    # OPEN YOUTUBE

    if "open youtube" in text:

        webbrowser.open("https://www.youtube.com")

        return "Opening YouTube"

    # OPEN GMAIL

    if "open gmail" in text:

        webbrowser.open("https://mail.google.com")

        return "Opening Gmail"

    # OPEN DOWNLOADS

    if "download" in text and "open" in text:

        downloads = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        os.startfile(downloads)

        return "Opening Downloads"

    # OPEN DESKTOP

    if "desktop" in text and "open" in text:

        desktop = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )

        os.startfile(desktop)

        return "Opening Desktop"

    # OPEN DOCUMENTS

    if "document" in text and "open" in text:

        documents = os.path.join(
            os.path.expanduser("~"),
            "Documents"
        )

        os.startfile(documents)

        return "Opening Documents"

    # OPEN PICTURES

    if "picture" in text and "open" in text:

        pictures = os.path.join(
            os.path.expanduser("~"),
            "Pictures"
        )

        os.startfile(pictures)

        return "Opening Pictures"

    # PLAY SONG

    if "play" in text:

        song = text

        song = song.replace("baby", "")
        song = song.replace("play", "")
        song = song.strip()

        pywhatkit.playonyt(song)

        return f"Playing {song}"

    # WEATHER

    if "weather" in text:

        try:

            data = requests.get(
                "https://wttr.in/?format=j1"
            ).json()

            current = data["current_condition"][0]

            temp = current["temp_C"]

            humidity = current["humidity"]

            desc = current["weatherDesc"][0]["value"]

            return (
                f"Current weather is {desc}. "
                f"Temperature is {temp} degrees Celsius. "
                f"Humidity is {humidity} percent."
            )

        except:

            return "Sorry, I could not get the weather."

    # TIME

    if (
        "what time is it" in text
        or "tell me the time" in text
        or text == "time"
    ):

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The time is {current_time}"

    # GOOGLE SEARCH

    if "search google for" in text:

        query = text.replace(
            "search google for",
            ""
        ).strip()

        webbrowser.open(
            f"https://www.google.com/search?q={query}"
        )

        return f"Searching Google for {query}"

    # BATTERY

    if (
        "battery percentage" in text
        or "battery level" in text
        or "battery status" in text
    ):

        battery = psutil.sensors_battery()

        if battery:

            return f"Your battery is at {battery.percent} percent"

        return "I cannot detect the battery"

    # SCREENSHOT

    if "take a screenshot" in text:

        screenshot = pyautogui.screenshot()

        screenshot.save("baby_screenshot.png")

        return "Screenshot saved"

    # IP ADDRESS

    if "ip address" in text:

        ip = socket.gethostbyname(
            socket.gethostname()
        )

        return f"Your IP address is {ip}"

    # CPU USAGE

    if "cpu usage" in text:

        cpu = psutil.cpu_percent(interval=1)

        return f"CPU usage is {cpu} percent"

    # RAM USAGE

    if (
        "ram usage" in text
        or "memory usage" in text
    ):

        ram = psutil.virtual_memory()

        return f"RAM usage is {ram.percent} percent"
    
        # SEARCH YOUTUBE

    if "search youtube for" in text:

        query = text.replace(
            "search youtube for",
            ""
        ).strip()

        webbrowser.open(
            f"https://www.youtube.com/results?search_query={query}"
        )

        return f"Searching YouTube for {query}"
    
        # OPEN GITHUB

    if "open github" in text:

        webbrowser.open("https://github.com")

        return "Opening GitHub"
    
        # OPEN CHATGPT

    if "open chatgpt" in text:

        webbrowser.open("https://chatgpt.com")

        return "Opening ChatGPT"
    
        # OPEN LINKEDIN

    if "open linkedin" in text:

        webbrowser.open("https://www.linkedin.com")

        return "Opening LinkedIn"
    
        # LOCK COMPUTER

    if "lock computer" in text:

        ctypes.windll.user32.LockWorkStation()

        return "Locking your computer"
    
        # SHUTDOWN COMPUTER

    if "shutdown computer" in text:

        os.system("shutdown /s /t 5")

        return "Shutting down computer"
    
    # Cancel SHUTDOWN COMPUTER

    if (
        "cancel shutdown" in text
        or "abort shutdown" in text
        or "shutdown abort" in text
        or "shutdown cancel" in text
        or "stop shutdown" in text
    ):

        # Cancel any pending system shutdown
        try:
            os.system("shutdown /a")
            return "Shutdown cancelled"
        except Exception:
            return "Could not cancel shutdown"

        # RESTART COMPUTER

    if "restart computer" in text:

        os.system("shutdown /r /t 5")

        return "Restarting computer"
    
    # EMPTY RECYCLE BIN

    if "empty recycle bin" in text:

        winshell.recycle_bin().empty(
            confirm=False,
            show_progress=False,
            sound=True
        )

        return "Recycle bin emptied"

    return None