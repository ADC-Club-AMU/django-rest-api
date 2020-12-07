# Sample Django API
A sample api with Django Rest Framework.
> Still in Development

## Setup project locally
> Use a virtual env
* Clone repo : ```$ git clone https://github.com/ADC-Club-AMU/django-rest-api.git```
* ```$ cd django-rest-api```
* Create a virtualenv: ```$ mkvirtualenv env``` or ```$ python -m venv env```
* Activate env : ```$ workon env``` or ```$ source env/bin/activate```
* Install dependencies : ```$ pip install -r requirements.txt```
* Run project : ```$ python manage.py runserver```

## API Endpoints

* http://127.0.0.1:8000/api/v1/calendar/<year>/<month>/<day>
> It will return all the events, holidays and university wide events for the day.

* http://127.0.0.1:8000/api/v1/calendar/<faculty>/<year>/<month>/<day>
> It will return all the events, and university wide events for the particular faculty.

* http://127.0.0.1:8000/api/v1/calendar/examinations/all/<year>/<month>/<day>
> It will return all the available exams for the day.

* http://127.0.0.1:8000/api/v1/faculty/
> Returns data of all faculties.

* http://127.0.0.1:8000/api/v1/faculty/<faculty>
> Returns data of a single faculty.

* http://127.0.0.1:8000/api/v1/department/
> Returns data of all departments.

* http://127.0.0.1:8000/api/v1/department/<faculty>/<department>
> Returns data of a department.

## ToDo
* Create a Web UI for admins.
* Add models for entrance exams and Holidays
* Generate endpoints that returns all entrance examinations and holidays.
