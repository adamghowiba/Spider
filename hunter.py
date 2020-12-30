from pyhunter import PyHunter
import json

hunter = PyHunter('c4e079986010a8232d7fe93767b194e6ff9f3a78')


def get_company_data(website):
    search_results = hunter.domain_search(website, limit=40, emails_type='personal')

    company_data = []

    for data in search_results['emails']:
        company_data.append((data["value"], data["first_name"], data["last_name"], data["phone_number"], data['type']))

    return company_data


def get_company_json(website):
    search_results = hunter.domain_search(website, limit=40, emails_type='personal')

    return search_results


# def create_mock_data():
#     search_results = hunter.domain_search("https://dunhill.net/")
#     file_path = os.path.dirname(os.path.abspath(__file__))
#     project_path = os.path.abspath(os.path.join(file_path, os.path.pardir))
#
#     data_path = os.path.join(project_path, 'Spider\\test.txt')
#
#     with open(data_path, "w") as t:
#         json.dump(search_results, t, indent=3)
#         t.close()
