import os


def get_project_file(project_name, filename):
    file_path = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.abspath(os.path.join(file_path, os.path.pardir))

    data_path = os.path.join(project_path, project_name + "\\" + filename)
    return data_path
