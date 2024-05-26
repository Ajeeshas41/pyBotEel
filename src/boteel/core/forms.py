from bottle import request
from typing import Dict


def form_data(data: Dict=None) -> Dict:
    if not data:
        data = request.forms

    cleaned_data: Dict = {}
    for key, value in data.items():
        cleaned_data[key] = value

    return cleaned_data
