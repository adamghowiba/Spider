import time


# TODO Is this memory Intensive? Can' it be made easier.
# TODO Just create text util?
# TODO - Error when adding to a empty file.
def create_new_line():
    with open("companies.txt", 'a') as a:
        a.write("\n")
        a.close()

def last_line_empty():
    with open('companies.txt', 'r') as r:
        lines = r.readlines()
        if lines[-1].endswith("\n"):
            print("File ends in new line")
            r.close()
            return True
        else:
            print("File doesn't end in new line, creating one.")
            r.close()
            return False

def append_company(text):
    a = open("companies.txt", 'a')
    if last_line_empty():
        a.write(text)
        a.close()
    else:
        create_new_line()
        a.write(text)
        a.close()

def generate_list_of_companies():
    companies = []
    with open("companies.txt", 'r') as f:
        for line in f.readlines():
            companies.append(str(line).strip())
            f.close()

    return companies