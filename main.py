from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from winery_lib import generate_year_form, get_winery_age
import pandas as pd
import argparse


def main():
    parser = argparse.ArgumentParser(
                    prog='Сайт винодельни',
                    description='Скрипт генерирует index.html для сайта',
                    epilog='--file_path')
    parser.add_argument("--file_path", help="Путь к файлу с данными", default="wine.xlsx")
    args = parser.parse_args()

    excel_data_df = pd.read_excel(io=args.file_path, na_values=' ', keep_default_na=False)

    winery_age = get_winery_age(1920)
    year_form = generate_year_form(winery_age)

    env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
    template = env.get_template('template.html')

    wines = excel_data_df.to_dict(orient='records')
    grouped_wines = {}

    for wine in wines:
        wine_item = {'Категория': wine['Категория'], 'Название': wine['Название'], 'Сорт': wine['Сорт'], 'Цена': wine['Цена'], 'Картинка': wine['Картинка'], 'Акция': wine['Акция']}
        grouped_wines.setdefault(wine_item['Категория'], []).append(wine_item)

    output = template.render(wines=grouped_wines, winery_age=winery_age, year_form=year_form, grouped_wines=grouped_wines)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(output)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
