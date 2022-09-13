import os
import requests

from dotenv import load_dotenv
from terminaltables import AsciiTable

MOST_POPULAR_LANGUAGES = (
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

URL_HH = "https://api.hh.ru/vacancies"
URL_SJ = "https://api.superjob.ru/2.0/vacancies/"

MOSCOW_ID_SJ = 4
MOSCOW_ID_HH = 1


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
    expected_salary = None
    if salary_from and salary_to:
        expected_salary = (salary_from + salary_to) / 2
    elif salary_from and not salary_to:
        expected_salary = 1.2 * salary_from
    else:
        expected_salary = 0.8 * salary_to
    return expected_salary


def predict_salary_sj(vacancy):
    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]
    return predict_salary(salary_from, salary_to)


def predict_salary_hh(vacancy):
    exp_salary = None
    salary = vacancy["salary"]
    if not salary or salary["currency"] != "RUR" : return None
    exp_salary = (predict_salary(salary["from"], salary["to"])
    return exp_salary


def get_vacancies(
    url,
    pages_alias,
    location,
    responce_items_alias,
    parameters_name,
    salary_count_function,
    headers=None,
):

    vacancy_description = [{} for _ in range(len(MOST_POPULAR_LANGUAGES))]
    vacancies = dict(zip(MOST_POPULAR_LANGUAGES, vacancy_description))

    for language in MOST_POPULAR_LANGUAGES:
        vacancy_pages = []
        vacancy_text = f"Программист {language}"
        vacancy_cnt = 0
        vacancy_total = 0
        avg_salary = 0
        page = 0
        pages_number = 1
        parameters = dict(zip(parameters_name, [vacancy_text, location, page]))
        while page < pages_number:
            try:
                page_response = requests.get(
                    url, params=parameters, headers=headers
                     )
                page_json = page_response.json()
                pages_number = page_json[pages_alias]
                vacancy_pages.append(page_json)
            except HTTPError:
                page_json=[]
                
            page += 1
            parameters["page"] = page

        for page in vacancy_pages:
            for vacancy in page[responce_items_alias]:
                vacancy_total += 1
                if salary_count_function(vacancy):
                    vacancy_cnt += 1
                    avg_salary += salary_count_function(vacancy)

        vacancies[language]["vacancies_found"] = vacancy_total
        vacancies[language]["vacancies_processed"] = vacancy_cnt
        try:
            vacancies[language]["average_salary"] = int(
                avg_salary / vacancy_cnt
            )
        except ZeroDivisionError:
            vacancies[language]["average_salary"] = 0

    return vacancies


if __name__ == "__main__":

    load_dotenv()

    headers = {"X-Api-App-Id": os.environ["X-API-APP-ID"]}

    vacancies_hh = get_vacancies(
        URL_HH,
        "pages",
        MOSCOW_ID_HH,
        "items",
        ("text", "area", "page"),
        predict_salary_hh,
    )

    vacancies_sj = get_vacancies(
        URL_SJ,
        "total",
        MOSCOW_ID_SJ,
        "objects",
        ("keyword", "town", "page"),
        predict_salary_sj,
        headers,
    )

    show_table(vacancies_hh, "HeadHunter")
    show_table(vacancies_sj, "SuperJob")
