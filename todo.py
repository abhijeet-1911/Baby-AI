import json

TODO_FILE = "tasks.json"


def load_tasks():

    try:

        with open(
            TODO_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return []


def save_tasks(tasks):

    with open(
        TODO_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            tasks,
            file,
            indent=4
        )


def add_task(task):

    tasks = load_tasks()

    tasks.append(task)

    save_tasks(tasks)


def get_tasks():

    return load_tasks()


def remove_task(task):

    tasks = load_tasks()

    tasks = [
        t
        for t in tasks
        if t.lower() != task.lower()
    ]

    save_tasks(tasks)