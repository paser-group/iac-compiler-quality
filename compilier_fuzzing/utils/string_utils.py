

def replace_slot(text, entries):
    for key, value in entries.items():
        if not isinstance(value, str):
            value = str(value)
        text = text.replace("{{" + key +"}}", value.replace('"', "'").replace('\n', ""))
    return text

def remove_tilda(text):
    return text.split('```')[1] 