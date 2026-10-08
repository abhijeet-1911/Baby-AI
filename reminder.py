import threading
import time

from voice import speak


def set_reminder(seconds, message):

    def reminder_task():

        time.sleep(seconds)

        reminder_text = (
            f"Honey, this is your reminder. {message}"
        )

        print("\nBaby:", reminder_text)

        speak(reminder_text)

    thread = threading.Thread(
        target=reminder_task
    )

    thread.daemon = True

    thread.start()