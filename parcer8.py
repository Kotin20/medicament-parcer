import requests
from bs4 import BeautifulSoup
import json
import lxml
from datetime import datetime
import csv

# https://www.lifetime.plus/
def get_data():
	url = 'https://www.lifetime.plus/api/analysis2'
	headers = {
		'accept': 'application/json, text/plain, */*',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
	}

	req = requests.get(url = url, headers = headers)
	data = req.json()
	
	data_list = []
	cur_data = datetime.now().strftime("%d_%m_%Y_%H_%M")

	with open (f'all_data_{cur_data}.csv','w', encoding = "cp1251", newline='') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(
			[
			'Категория',
			"Анализ",
			"Биоматериал",
			"Описание",
			"Стоимость",
			"Готовность в течении(дни)"
			]
		)

	categories = data['categories']
	count = 0
	for category in categories:
		category_name = category['name']
		items = category['items']
		for item in items:
			item_name = item['name']
			item_price = item['price']
			item_duration_days = item['days']
			item_biomaterial = item['biomaterial']
			item_description = item['description'].replace('\n', '')
			if 'α' in  item_description:
				item_description = item_description.replace('α','a')
			if 'β' in  item_description:
				item_description = item_description.replace('β','B')
			if 'γ' in  item_description:
				item_description = item_description.replace('γ','y')

			data_list.append(
				{
				'item_name' : item_name,
				'item_name' : item_name,
				'item_price' : item_price,
				'item_duration_days' : item_duration_days,
				'item_biomaterial' : item_biomaterial,
				'item_description' : item_description,
				}
			)

			with open (f'all_data_{cur_data}.csv','a', encoding = "cp1251", newline='') as file:
				writer = csv.writer(file, delimiter=';')
				writer.writerow(
					[
					category_name,
					item_name,
					item_biomaterial,
					item_description,
					item_price,
					item_duration_days
					]
				)

		count += 1
		print(f'Обработана категория №{count}')

	with open(f'data_{cur_data}.json', 'w', encoding = 'utf-8') as file:
		json.dump(data_list, file, indent = 4, ensure_ascii= False)


def main():
	get_data()


if __name__ == '__main__':
	main()