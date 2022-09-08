import os
import requests

from dotenv import load_dotenv
from terminaltables import AsciiTable

most_popular_languages = (
    "Javascript",
    "Java",
    "Python",
    "Ruby",
    "PHP",
    "C++",
    "C#",
    "C",
    "Go",
    "Scala",
)

url_hh = "https://api.hh.ru/vacancies"
url_sj = "https://api.superjob.ru/2.0/vacancies/"


def show_table(vacancy_dictionary, table_title):
    table_rows = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]
    for language, params in vacancy_dictionary.items():
        table_rows.append(
            [
                language,
                params["vacancies_found"],
                params["vacancies_processed"],
                params["average_salary"],
            ]
        )
    table_instance = AsciiTable(table_rows, table_title)
    print(table_instance.table)


def predict_salary(salary_from, salary_to):
    expected_salary = 0
    if salary_from and salary_to:
        expected_salary = (salary_from + salary_to) / 2
    elif salary_from and not salary_to:
        expected_salary = 1.2 * salary_from
    elif not salary_to and salary_from:
        expected_salary = 0.8 * salary_to
    else:
        expected_salary = None
    return expected_salary


def predict_salary_sj(vacancy):
    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]
    return predict_salary(salary_from, salary_to)


def predict_salary_hh(vacancy):
    salary = vacancy["salary"]
    exp_salary = 0
    if salary and salary["currency"] == "RUR":
        salary_from = salary["from"]
        salary_to = salary["to"]
        exp_salary = predict_salary(salary_from, salary_to)
    else:
        exp_salary = None
    return exp_salary


def get_response_json(url, params, headers=None):
    page_response = requests.get(url, params=params, headers=headers)
    page_json = page_response.json()
    return page_json


def create_response_param(parameter_name, parameter_value):
    return dict(zip(parameter_name, parameter_value))


def create_vacancy_dict(
    url,
    pages_alias,
    location,
    responce_items_alias,
    parameters_name,
    salary_count_function,
    headers=None,
):

    empty_dicts = [{} for _ in range(len(most_popular_languages))]
    vacancies_dict = dict(zip(most_popular_languages, empty_dicts))

    for language in most_popular_languages:
        response_json = []
        vacancy_text = f"Программист {language}"
        vacancy_cnt = 0
        avg_salary = 0
        found = 0
        page = 0
        pages_number = 1
        parameters = create_response_param(
            parameters_name, (vacancy_text, location, page)
        )
        while page < pages_number:
            page_json = get_response_json(url, parameters, headers)
            pages_number = page_json[pages_alias]
            response_json.append(page_json)
            page += 1
            parameters["page"] = page

        for json in response_json:
            for item in json[responce_items_alias]:
                if salary_count_function(item):
                    vacancy_cnt += 1
                    avg_salary += salary_count_function(item)

        vacancies_dict[language]["vacancies_found"] = pages_number
        vacancies_dict[language]["vacancies_processed"] = vacancy_cnt
        vacancies_dict[language]["average_salary"] = int(avg_salary / vacancy_cnt)

    return vacancies_dict


if __name__ == "__main__":

    load_dotenv()
    
    headers = {"X-Api-App-Id": os.environ["X-Api-App-Id"]}

    vacancies_dict_hh = create_vacancy_dict(
                        url_hh,
                        'pages',
                        1,
                        'items',
                        ('text','area','page'),
                        predict_salary_hh
                       )
    
    vacancies_dict_sj = create_vacancy_dict(
                        url_sj,
                        'total',
                        4,
                        'objects',
                        ('keyword', 'town', 'page'),
                        predict_salary_sj,
                        headers
                      )

    show_table(vacancies_dict_hh, 'HeadHunter')
    show_table(vacancies_dict_sj, 'SuperJob')
