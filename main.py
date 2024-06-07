# import des bibliothèques requests et BeautifulSoup
import csv

import requests
from bs4 import BeautifulSoup
import pprint

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

    # je transforme review_rating en liste pour pouvoir l'intégrer dans le fichier CSV
review_rating = review_rating_text.split()

print(review_rating)

# Extraction de l'url de l'image

section = book_soup.find("div", class_="col-sm-6")
image_url_text = section.find("img").get("src")
    # je transforme image_url_text en liste pour l'intégrer dans le fichier CSV
image_url = image_url_text.split()

print(url + image_url_text)



# Création d'un fichier CSV avec les informations obtenues

headers = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available','product_description', 'category', 'review_rating', 'image_url' ]
with open("book.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(headers)
    for product_catalogue_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url in zip(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url):
        writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])


#---------------PHASE 2 ---------------------

# je choisis la catégorie Mystery (32 livres)

url_mystery = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
response_mystery = requests.get(url_mystery)
mystery_soup = BeautifulSoup(response_mystery.content, "html.parser")

# je vise où se situent l'ensemble des livres de la page (mystery_column)
# et je selectionne tous les livres (mystery_books)


mystery_column = mystery_soup.find("ol", class_="row")
mystery_books = mystery_column.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

# le lien de chaque livre est situé dans les balises h3 :

mystery_books_urls = mystery_column.find_all("h3")

# je boucle sur l'ensemble des balises h3 et selectione la première entrée [0]
# de chaque attribut "a"
# puis je concatene le lien "attrapé" avec l'url de la page

for mystery_books_url in mystery_books_urls:
    links = mystery_books_url.find_all("a")
    link = links[0]
    print(url + link.get("href"))

# cas où la catégorie comporte plusieurs pages







