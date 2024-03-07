from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from winery_lib import get_todays_date, generate_year_form
import pandas as pd
import argparse


def main(file_path=None):
    if file_path:
        excel_data_df = pd.read_excel(io=file_path, na_values=' ', keep_default_na=False)
    else:
        excel_data_df = pd.read_excel(io='wine.xlsx', na_values=' ', keep_default_na=False)

    winery_age, year_form = get_todays_date()

    env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
    template = env.get_template('template.html')

    wines = excel_data_df.to_dict(orient='records')
    grouped_wines = {}

    for wine in wines:
        wine_data = {'Категория': wine['Категория'], 'Название': wine['Название'], 'Сорт': wine['Сорт'], 'Цена': wine['Цена'], 'Картинка': wine['Картинка'], 'Акция': wine['Акция']}
        grouped_wines.setdefault(wine_data['Категория'], []).append(wine_data)

    output = template.render(wines=wines,grouped_wines=grouped_wines, winery_age=winery_age, year_form=year_form)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(output)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Сайт винодельни',
                    description='Скрипт генерирует index.html для сайта',
                    epilog='--file_path')
    parser.add_argument("–file_path", help="Путь к файлу с данными", default="template.html")
    args = parser.parse_args()
    
    main(args.file_path)