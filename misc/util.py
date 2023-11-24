from pathlib import Path
from uuid import uuid4
from dataclasses import asdict

from promobot_appeal_processing import Prediction

from misc.config import Paths, field_name_mapping


def get_temp_file_path(extension: str = None) -> Path:
    return Path(
        Paths.temp_dir,
        str(uuid4()) + ("" if extension.startswith(".") else ".") + (extension if extension else "")
    )


def prediction_to_csv_dict(text: str, prediction: Prediction) -> dict[str, str]:
    return {"Текст инцидента": text} | {field_name_mapping[key]: value for key, value in asdict(prediction).items()}
