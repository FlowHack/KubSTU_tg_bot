from ujson import JSONDecodeError, dump, load


def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                return load(file)
            except JSONDecodeError as error:
                print(str(error) + f'. (read_json) При чтении: {file_path}')
                return None
    except FileNotFoundError:
        with open(file_path, 'w', encoding='utf-8') as file:
            return None


def write_json(file_path, text, ensure_ascii=True, indent=4):
    with open(file_path, 'w', encoding='utf-8') as file:
        dump(text, file, ensure_ascii=ensure_ascii, indent=indent)
