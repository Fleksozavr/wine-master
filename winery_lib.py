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


def get_winery_age(founded_year):
    current_year = datetime.now().year
    return current_year - founded_year


def get_todays_date():
    winery_founded_year = 1920
    winery_age = get_winery_age(winery_founded_year)
    year_form = generate_year_form(winery_age)
    full_date = winery_age, year_form
    return full_date