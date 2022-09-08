import os
import pprint
import requests

from dotenv import load_dotenv

def predict_salary(salary_from, salary_to):
    expected_salary = 0
    if (salary_from and salary_to) or salary_from*salary_to > 0:
        expected_salary = (salary_from + salary_to)/2
    elif (salary_from and not salary_to) or (salary_to==0 and salary_from>0):
        expected_salary=1.2*salary_from
    elif (not salary_to and salary_from) or (salary_from==0 and salary_to>0):
        expected_salary = 0.8*salary_to
    else:
        expected_salary = None
    return expected_salary

def predict_rub_salary_sj(vacancy):
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    return predict_salary(salary_from, salary_to)
    
        

if __name__ == '__main__':

    
    load_dotenv()
    pp=pprint.PrettyPrinter()

    vacancies_list=[]

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
    empty_dicts=[{} for _ in range(len(most_popular_languages))]

    vacancies_dict=dict(zip(most_popular_languages, empty_dicts))
    
    
    url = 'https://api.superjob.ru/2.0/vacancies/'
    
    headers = {'X-Api-App-Id':os.environ['X-Api-App-Id']}

    for language in most_popular_languages:

        page = 0
        pages_number = 1
        per_page = 25
        
        response_json=[]
        vacancy_text = f'Программист {language}'       
        vacancy_cnt = 0        
        avg_salary = 0
        found = 0
        
        print(f'Программист {language}')
        
        while page < pages_number:
        
            params={'keyword':vacancy_text,
                    'town':4,
                    'page':page,
                    'count':per_page}
        
            response=requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            page_json = response.json()
            pages_number = page_json['total']
            found = page_json['total']
            print(page_json['total'])
            pp.pprint(page_json)
            page += 1
            print('Page', page)
            response_json.append(page_json)
            
        for json in response_json:
            for item in json['objects']:
                if predict_rub_salary_sj(item):
                    vacancy_cnt += 1
                    avg_salary += predict_rub_salary_sj(item)
                
        vacancies_dict[language]['vacancies_found'] = page_json['total']        
        vacancies_dict[language]['vacancies_processed'] = vacancy_cnt
        vacancies_dict[language]['average_salary'] = int(avg_salary/vacancy_cnt)
        pp.pprint(vacancies_dict)

    pp.pprint(vacancies_dict)
    
   

