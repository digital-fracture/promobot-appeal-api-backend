from pathlib import Path
from tempfile import gettempdir


class Paths:
    database = Path("state/sqlite.db")
    temp_dir = Path(gettempdir(), "kruase")


Paths.database.parent.mkdir(exist_ok=True)
Paths.temp_dir.mkdir(exist_ok=True)


field_name_mapping = {
    "topic": "Тема",
    "topic_group": "Группа тем",
    "executor": "Исполнитель"
}

max_parallel_processes = 4
