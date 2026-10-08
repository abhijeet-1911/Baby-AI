NOTES_FILE = "notes.txt"


def save_note(note):

    with open(
        NOTES_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(note + "\n")


def read_notes():

    try:

        with open(
            NOTES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except:

        return ""