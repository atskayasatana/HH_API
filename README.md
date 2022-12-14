# Поиск вакансий на сайтах HH и SuperJob

Скрипт для поиска вакансий программистов на двух ресурсах: hh.ru и SuperJob.ru.

Результаты поиска отображаются на экране в виде 2 таблиц с данными:

-язык программирования

-количество вакансий

-количество вакансий с заработной платой

-средняя ожидаемая заработная плата
### Запуск

Для работы понадобится Python3 и ряд библиотек из файла requirements.txt.
Для сайта Superjob.ru нужен токен, зарегистрироваться и получить токен можно здесь: https://api.superjob.ru/.

Токен нужно сохранить в .env файл в директории проекта:

```Python
X-Api-App-Id = # токен для API Superjob
```

Запускаем командную строку, переходим в директорию проекта и устанавливаем зависимости:
```
pip install -r requirements.txt
```
Запускаем проект:

```
python main.py
```

Результат:

![](https://github.com/atskayasatana/Images/blob/cab8f567e77b2cd10ec4035ddcdbaf62c44dfae6/hh_api_res.png)


### Функции

#### def show_table(vacancy_dictionary, table_title)

Отображает словарь vacancy_dictionary в таблицу с заголовком table_title, где каждое значение ключа отображается в отдельном столбце.

#### def predict_salary(salary_from, salary_to)

Вычисляет среднюю ожидаемую зарплату:
* если задана только конечная зарплата salary_to, то ожидаемая зарплата равна 80% от конечной зарплаты
* если задана только начальная зарплата salary_from, то ожидаемая зарплата равна начальная зарплата +20% 
* если заданы и начальная и конечная зарплата, то ожидаемая зарплата равна среднему арифметическому

#### def predict_salary_sj(vacancy), def predict_salary_hh(vacancy)

Функции для вычисления ожидаемой зарплаты для вакансии для каждого сайта отдельно.

#### def get_response_json(url, params, headers=None)

Возвращает JSON файл для страницы из запроса

#### def create_response_param(parameter_name, parameter_value)

Создает словарь с параметрами и значениями для передачи с запросом.

#### def create_vacancy_dict()

Функция для получения информации по вакансиям с сайта url.

Аргументы:

* pages_alias - название поля, где указано количество страниц, удовлетворяющих запросу

* location - значение местоположения

* responce_items_alias - название элементов объекта JSON, который вернет запрос: items - для HH, objects - для SuperJob

* responce_vacancy_cnt_alias - название поля, где указано количество вакансий, удовлетворяющих запросу

* parameters_name - список параметров для передачи в запросе

* salary_count_function - функция, которая будет использоваться для подсчета ожидаемой зарплаты

* headers - заголовки(если необходимы)








