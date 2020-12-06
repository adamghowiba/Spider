from pyhunter import PyHunter
import json

hunter = PyHunter('c4e079986010a8232d7fe93767b194e6ff9f3a78')


def get_company_data(website):
    search_results = hunter.domain_search(website)

    company_data = []

    for data in search_results['emails']:
        company_data.append((data["value"], data["first_name"], data["last_name"], data["phone_number"], data['type']))

    return company_data
