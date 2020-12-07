import yaml
import fileutils


def add_last_row(row):
    with open(fileutils.get_project_file("Spider", "settings.yaml")) as f:
        doc = yaml.safe_load(f)

    # Set the last row to the current row + new rows - 1 for the header
    doc['excel']["lastRow"] = int(doc['excel']['lastRow']) + int(row) - 1

    with open(fileutils.get_project_file("Spider", "settings.yaml"), 'w') as f:
        yaml.dump(doc, f)
    print("last row set to", row)


def get_last_row():
    try:
        with open(fileutils.get_project_file("Spider", "settings.yaml"), "r") as fs:

            config = yaml.safe_load(fs)

            fs.close()
            return int(config['excel']['lastRow'])
    except yaml.YAMLError as exc:
        print(exc)
