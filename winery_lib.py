from datetime import datetime


def generate_year_form(number):
    if number % 100 in [11, 12, 13, 14]:
        return 'лет'
    elif number % 10 == 1:
        return 'год'
    elif number % 10 in [2, 3, 4]:
        return 'года'
    else:
        return 'лет'


def todays_year():
    current_year = datetime.now().year
    winery_founded_year = 1920
    winery_age = current_year - winery_founded_year
    year = generate_year_form(winery_age)
    full_date = winery_age, year
    return full_date