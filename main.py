
import argparse
import speech_recognition as sr
import sys

from commands import execute_command
from voice import speak
from brain import ask_baby
from memory import remember, recall
from reminder import set_reminder
from todo import add_task, get_tasks, remove_task
from notes import save_note, read_notes

r = sr.Recognizer()

# CLI: allow listing microphones or specifying a device index
parser = argparse.ArgumentParser(description="Baby AI voice assistant")
parser.add_argument("--list-devices", action="store_true", help="List available microphone devices")
parser.add_argument("--device-index", type=int, default=1, help="Microphone device index to use (default: 1)")
args = parser.parse_args()

if args.list_devices:
    names = sr.Microphone.list_microphone_names()
    for i, name in enumerate(names):
        print(i, name)
    sys.exit(0)
greeting = (
    "Welcome back Honey. "
    "How can I help you today?"
)

speak(greeting)
print("MAIN.PY LOADED")
print("Baby is awake.")

while True:
    try:
        # Select microphone: use the provided device index if given
        mic_kwargs = {}
        if args.device_index is not None:
            mic_kwargs["device_index"] = args.device_index

        with sr.Microphone(**mic_kwargs) as source:
            print("\nListening...")

            r.adjust_for_ambient_noise(source, duration=1)

            audio = r.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )

        try:
            user_text = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand audio")
            continue
        except sr.RequestError as e:
            print("Could not request results from recognition service:", e)
            continue

        print("You:", user_text)

        text = user_text.lower().strip()

        # ----------------------------------
        # EXIT COMMANDS
        # ----------------------------------

        if (
            "bye" in text
            or "goodbye" in text
            or text == "stop"
            or text == "exit"
        ):
            print("EXIT DETECTED")
            print("TEXT RECEIVED:", repr(text))

            speak("Goodbye Honey. Have a great day.")

            break

        # ----------------------------------
        # WAKE WORD
        # ----------------------------------

       
        text = user_text.lower()

        print("Detected text:", text)
        

        # ----------------------------------
        # REMEMBER NAME
        # ----------------------------------

        if "my name is" in text:

            name = text.split(
                "my name is"
            )[-1].strip()

            remember(
                "user_name",
                name
            )

            reply = (
                f"I will remember that your name is {name}"
            )

            print("Baby:", reply)

            speak(reply)

            continue

        # ----------------------------------
        # RECALL NAME
        # ----------------------------------

        if (
            "what is my name" in text
            or
            "tell me my name" in text
        ):

            name = recall("user_name")

            if name:

                reply = f"Your name is {name}"

            else:

                reply = (
                    "I don't know your name yet."
                )

            print("Baby:", reply)

            speak(reply)

            continue

        # ----------------------------------
        # REMEMBER FAVORITE CHARACTER
        # ----------------------------------

        if (
            "favorite character is" in text
            or
            "favourite character is" in text
        ):

            value = text

            value = value.replace(
                "baby",
                ""
            )

            value = value.replace(
                "remember my favorite character is",
                ""
            )

            value = value.replace(
                "remember my favourite character is",
                ""
            )

            value = value.replace(
                "my favorite character is",
                ""
            )

            value = value.replace(
                "my favourite character is",
                ""
            )

            value = value.strip()

            remember(
                "favorite_character",
                value
            )

            reply = (
                f"I will remember that your favorite character is {value}"
            )

            print("Baby:", reply)

            speak(reply)

            continue

        # ----------------------------------
        # RECALL FAVORITE CHARACTER
        # ----------------------------------

        if (
            "what is my favorite character" in text
            or
            "what is my favourite character" in text
            or
            "who is my favorite character" in text
            or
            "who is my favourite character" in text
            or
            "tell me my favorite character" in text
            or
            "tell me my favourite character" in text
        ):

            value = recall(
                "favorite_character"
            )

            if value:

                reply = (
                    f"Your favorite character is {value}"
                )

            else:

                reply = (
                    "I don't know your favorite character yet."
                )

            print("Baby:", reply)

            speak(reply)

            continue

        # ----------------------------------
        # GENERIC MEMORY SAVE
        # ----------------------------------

        if (
            "remember" in text
            and
            " as " in text
        ):

            memory_text = text.replace(
                "remember",
                ""
            ).strip()

            parts = memory_text.split(
                " as "
            )

            if len(parts) == 2:

                key = parts[0].strip()

                value = parts[1].strip()

                key = key.replace(
                    " ",
                    "_"
                )

                remember(
                    key,
                    value
                )

                reply = (
                    f"I will remember that {parts[0]} is {value}"
                )

                print("Baby:", reply)

                speak(reply)

                continue

        # ----------------------------------
        # GENERIC MEMORY RECALL
        # ----------------------------------

        if text.startswith(
            "what is "
        ):

            key = text.replace(
                "what is",
                ""
            ).strip()

            key = key.replace(
                " ",
                "_"
            )

            value = recall(key)

            if value:

                reply = (
                    f"{key.replace('_', ' ')} is {value}"
                )

                print("Baby:", reply)

                speak(reply)

                continue

        # ----------------------------------
        # REMINDER
        # ----------------------------------

        if (
            "remind me to" in text
            and
            " in " in text
        ):

            try:

                task_part = text.split(
                    "remind me to"
                )[1]

                task = task_part.rsplit(
                    " in ",
                    1
                )[0].strip()

                time_text = text.rsplit(
                    " in ",
                    1
                )[1].strip()

                # Seconds

                if "second" in time_text:

                    number = int(
                        time_text.replace(
                            "seconds",
                            ""
                        ).replace(
                            "second",
                            ""
                        ).strip()
                    )

                    seconds = number

                # Minutes

                elif "minute" in time_text:

                    number = int(
                        time_text.replace(
                            "minutes",
                            ""
                        ).replace(
                            "minute",
                            ""
                        ).strip()
                    )

                    seconds = number * 60

                # Hours

                elif "hour" in time_text:

                    number = int(
                        time_text.replace(
                            "hours",
                            ""
                        ).replace(
                            "hour",
                            ""
                        ).strip()
                    )

                    seconds = number * 3600

                else:

                    raise ValueError(
                        "Unknown time format"
                    )

                set_reminder(
                    seconds,
                    task
                )

                reply = (
                    f"Okay Honey. "
                    f"I will remind you to "
                    f"{task} in {time_text}."
                )

                print("Baby:", reply)

                speak(reply)

                continue

            except Exception as e:

                print(e)

                reply = (
                    "Please say something like "
                    "remind me to study in 30 seconds "
                    "or remind me to sleep in 1 hour."
                )

                print("Baby:", reply)

                speak(reply)

                continue

        # ----------------------------------
        # SAVE NOTE
        # ----------------------------------

        if (
            text.startswith("note")
            or text.startswith("not")
            or "save note" in text
        ):

            note_text = text.replace(
                "note",
                "",
                1
            ).strip()

            if note_text:

                save_note(note_text)

                reply = "Your note has been saved."

                print("Baby:", reply)

                speak(reply)

                continue

        # ----------------------------------
        # READ NOTES
        # ----------------------------------

        if (
            "read my notes" in text
            or
            "show my notes" in text
        ):

            print("READ NOTES COMMAND DETECTED")

            notes = read_notes()

            if notes.strip():

                reply = (
                    "Here are your notes. "
                    + notes
                )

            else:

                reply = (
                    "You do not have any notes."
                )

            print("Baby:", reply)

            speak(reply)

            continue

        # ----------------------------------
        # ADD TASK
        # ----------------------------------

        if "add task" in text:

            task = text.replace(
                "add task",
                ""
            ).strip()

            if task:

                add_task(task)

                reply = "Task added."

                print("Baby:", reply)

                speak(reply)

                continue

        # ----------------------------------
        # SHOW TASKS
        # ----------------------------------

        if (
            "task" in text
            and
            (
                "show" in text
                or "read" in text
                or "list" in text
            )
        ):

            tasks = get_tasks()

            if tasks:

                count = len(tasks)

                reply = f"You have {count} tasks. "

                for i, task in enumerate(tasks, start=1):

                    reply += f"Number {i}. {task}. "

            else:

                reply = "You do not have any tasks."

            print("Baby:", reply)

            speak(reply)

            continue

        # ----------------------------------
        # COMPLETE TASK
        # ----------------------------------

        if (
            "complete task" in text
            or
            "remove task" in text
        ):

            task = text

            task = task.replace(
                "complete task",
                ""
            )

            task = task.replace(
                "remove task",
                ""
            )

            task = task.strip()

            remove_task(task)

            reply = "Task completed."

            print("Baby:", reply)

            speak(reply)

            continue

        # ----------------------------------
        # EXIT COMMANDS
        # ----------------------------------

        if text in [
            "bye baby",
            "goodbye baby",
            "stop",
            "exit"
        ]:

            speak(
                "Goodbye Honey. Have a great day."
            )

            break

        # ----------------------------------
        # COMMANDS
        # ----------------------------------

        command_result = execute_command(
            user_text
        )

        if command_result:

            print("Baby:", command_result)

            speak(command_result)

            continue

        # ----------------------------------
        # NORMAL AI CHAT
        # ----------------------------------

        reply = ask_baby(
            user_text
        )

        print("Baby:", reply)

        speak(reply)

    except SystemExit:
        raise

    except sr.WaitTimeoutError:
        print("No speech detected.")

    except Exception as e:
        print("ERROR TYPE:", type(e))
        print("ERROR MESSAGE:", repr(e))
