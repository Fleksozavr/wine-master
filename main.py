from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from winery_lib import todays_year, generate_year_form
import pandas as pd
import argparse


def main(file_path=None):
    if file_path:
        excel_data_df = pd.read_excel(io=file_path, na_values=' ', keep_default_na=False)
    else:
        excel_data_df = pd.read_excel(io='wine.xlsx', na_values=' ', keep_default_na=False)

    full_date = todays_year()

    env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
    template = env.get_template('template.html')

    wines = excel_data_df.to_dict(orient='records')
    res = {}

    for wine in wines:
        wine_list = [{'Категория': wine['Категория'], 'Название': wine['Название'], 'Сорт': wine['Сорт'], 'Цена': wine['Цена'], 'Картинка': wine['Картинка'], 'Акция': wine['Акция']}]
        for x in wine_list:
            res.setdefault(x['Категория'], []).append(x)

    output = template.render(winery_age=full_date[0], year=full_date[1], wines=wines, full_date=full_date, res=res)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(output)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="Путь к файлу с данными")
    args = parser.parse_args()
    
    main(args.file_path)