import json
from datetime import datetime, date

def custom_encoder(obj):
  if isinstance(obj, (datetime, date)):
    return obj.isoformat()
  if hasattr(obj, "__dict__"):
    return obj.__dict__
  return str(obj)

def save_json(data, filename):
  with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2, default=custom_encoder)

def load_json(filename):
  try:
    with open(filename, "r", encoding="utf-8") as f:
      return json.load(f)
  except FileNotFoundError:
    return None
