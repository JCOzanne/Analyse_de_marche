# import des bibliothèques requests et BeautifulSoup
import csv

import requests
from bs4 import BeautifulSoup
from pprint import pprint

# extraction de l'url de la page du livre choisi

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

#---------------PHASE 1 ---------------------

# Extraction de l'url de la page du produit

product_catalogue_url = soup.find_all("ol", class_="row")

for links in product_catalogue_url :
    link = links.find_all("a")

url_catalogue = link[0].get('href')

product_page_url = url+url_catalogue


print(product_page_url)




# Extraction des données de la page du livre choisi, avec BeautifulSoup


book_response = requests.get(product_page_url)
book_soup = BeautifulSoup(book_response.content, "html.parser")

# extraction des informations produit

product_information = book_soup.find("table", class_="table table-striped")
informations = product_information.find_all("tr")



# Extraction de l'UPC


universal_product_code = informations[0].find("td")

print(universal_product_code.text)


# Extraction du titre du livre

column = book_soup.find("div", class_="col-sm-6 product_main")
title = column.find("h1")

print(title.text)

# Extraction du prix avec taxes

price_including_tax = informations[3].find("td")

print(price_including_tax.text)

#Extraction du prix sans taxes

price_excluding_tax = informations[2].find("td")

print(price_excluding_tax.text)

# Extraction du nombre de livre disponibles

number_available = informations[5].find("td")

print(number_available.text)

# Extraction de la catégorie du livre

cat = book_soup.find("ul", class_ = "breadcrumb")
cat_book = cat.find_all("li")
category = cat_book[2]

print(category.text)

# Desciption du produit

article = book_soup.find("article", class_="product_page")
articles = article.find_all("p")
product_description = articles[3]

print(product_description.text)

# Extraction de l'évaluation du livre

rating = column.find_all("p")
review_rating_text = rating[2]["class"][1]

    # je transforme eview_rating en liste pour l'intégrer dans le fichier CSV
review_rating = review_rating_text.split()

print(review_rating)

# Extraction de l'url de l'image

section = book_soup.find("div", class_="col-sm-6")
image_url_text = section.find("img").get("src")
    # je transforme image_url_text en liste pour l'intégrer dans le fichier CSV
image_url = image_url_text.split()

print(image_url)




# Création d'un fichier CSV avec les informations obtenues

headers = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available','product_description', 'category', 'review_rating', 'image_url' ]
with open("book.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(headers)
    for product_catalogue_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url  in zip(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url):
        writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])


#---------------PHASE 2 ---------------------

