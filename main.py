import json
import pprint
import requests

def predict_salary(vacancy):
    salary = vacancy['salary']
    exp_salary = 0
    if salary and salary['currency']:
        salary_from = salary['from']
        salary_to = salary['to']
        if salary_from and salary_to:
            exp_salary = (salary_from + salary_to)/2
        elif salary_from and not salary_to:
            exp_salary = 1.2*salary_from
        else:
            exp_salary = 0.8*salary_to
    else:
        exp_salary = None
    return exp_salary
        
 

if __name__ == '__main__':

    pp = pprint.PrettyPrinter()
    
    most_popular_languages=('Javascript',
                            'Java',
                            'Python',
                            'Ruby',
                            'PHP',
                            'C++',
                            'C#',
                            'C',
                            'Go',
                            'Scala')

    vacancies_dict=dict.fromkeys(most_popular_languages,
                                 {'vacancies_found': 0,
                                  'vacancies_processed': 0,
                                  'average_salary': 0})
    
    url = 'https://api.hh.ru/vacancies'

    for language in vacancies_dict:      
        print(language)        
        vacancy_cnt = 0
        avg_salary = 0
        
        vacancy_text = f'Программист {language}'
        payload = {'text':vacancy_text,
                   'area':1
                   }
        response = requests.get(url, params=payload)
        response_json = response.json()
        print(response_json['found'])
        for item in response_json['items']:
            if predict_salary(item):
                vacancy_cnt += 1
                avg_salary += predict_salary(item)
        print(vacancy_cnt)
        print(avg_salary/vacancy_cnt)
        vacancies_dict[language]['vacancies_found'] = response_json['found']        
        vacancies_dict[language]['vacancies_processed'] = vacancy_cnt
        vacancies_dict[language]['average_salary'] = int(avg_salary/vacancy_cnt)
        
    pp.pprint(vacancies_dict)


