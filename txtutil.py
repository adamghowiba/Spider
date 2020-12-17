import fileutil


# TODO Is this memory Intensive? Can' it be made easier.
def create_new_line_with_text(text):
    with open("Spider/companies.txt", 'a') as a:
        a.write("\n")
        a.write(text)
        a.close()


def append_company_safe(text):
    with open('Spider/companies.txt') as r:
        lines = r.readlines()
        if len(lines) == 0:
            append_company(text)
            return
        if not lines[-1].endswith("\n"):
            create_new_line_with_text(text)
            r.close()
        else:
            print("nothing in file")


def append_company(text):
    with open("Spider/companies.txt", 'a') as a:
        a.write(text)
        a.close()


def generate_list_of_companies():
    companies = []
    with open(fileutil.get_project_file('Spider', 'companies.txt'), 'r+') as f:
        for line in f.readlines():
            companies.append(str(line).strip())
            f.close()
    return companies
