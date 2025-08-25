def format_date(date_str):
    from datetime import datetime
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def load_json(file_path):
    import json
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    import json
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def generate_unique_id(prefix, existing_ids):
    import uuid
    new_id = f"{prefix}_{uuid.uuid4().hex}"
    while new_id in existing_ids:
        new_id = f"{prefix}_{uuid.uuid4().hex}"
    return new_id

def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None