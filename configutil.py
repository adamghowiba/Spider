import yaml
import fileutil


def get_value(path, key):
    with open(fileutil.get_project_file('Spider', 'settings.yaml')) as f:
        config = yaml.safe_load(f)
        f.close()

        value = config[path][key]

        if str(value).isdigit():
            return int(value)
        else:
            return value


def update_key(path, key, value):
    with open(fileutil.get_project_file("Spider", "settings.yaml")) as f:
        doc = yaml.safe_load(f)

    # Set the last row to the current row + new rows - 1 for the header
    doc[path][key] = str(value)

    with open(fileutil.get_project_file("Spider", "settings.yaml"), 'w') as f:
        yaml.safe_dump(doc, f)


def add_last_row(row):
    with open(fileutil.get_project_file("Spider", "settings.yaml")) as f:
        doc = yaml.safe_load(f)

    # Set the last row to the current row + new rows - 1 for the header
    doc['excel']["lastRow"] = int(doc['excel']['lastRow']) + int(row) - 1

    with open(fileutil.get_project_file("Spider", "settings.yaml"), 'w') as f:
        yaml.dump(doc, f)


def get_last_row():
    try:
        with open(fileutil.get_project_file("Spider", "settings.yaml")) as fs:

            config = yaml.safe_load(fs)

            fs.close()
            return int(config['excel']['lastRow'])
    except yaml.YAMLError as exc:
        print(exc)
