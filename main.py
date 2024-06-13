# import des bibliothèques
import csv

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


# extraction de l'url de la page du livre choisi

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

#---------------PHASE 1 ---------------------

# Extraction de l'url de la page du produit

product_catalogue_url = soup.find_all("ol", class_="row")

for links in product_catalogue_url:
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

cat = book_soup.find("ul", class_="breadcrumb")
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

print(review_rating[0])

# Extraction de l'url de l'image

section = book_soup.find("div", class_="col-sm-6")
image_url_text = section.find("img").get("src")

    # je transforme image_url_text en liste pour l'intégrer dans le fichier CSV

image_url = image_url_text.split()

print(url + "/catalogue/" + image_url_text)



# Création d'un fichier CSV avec les informations obtenues

headers = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available","product_description", "category", "review_rating", "image_url"]
with open("book.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(headers)
    for product_catalogue_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url in zip(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url):
        writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])


#---------------PHASE 2 ---------------------

# je choisis la catégorie Mystery (32 livres) sur 2 pages

url_mystery = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
response_mystery = requests.get(url_mystery)
mystery_soup = BeautifulSoup(response_mystery.content, "html.parser")


# je vise où se situent l'ensemble des livres de la page (mystery_column)
# et je selectionne tous les livres (mystery_books)


mystery_column = mystery_soup.find("ol", class_="row")
mystery_books = mystery_column.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

# le lien de chaque livre est situé dans les balises h3 :

mystery_books_urls = mystery_column.find_all("h3")

# je boucle sur l'ensemble des url des livres de la catégorie "Mystery" pour obtenir les informations
# de chaque livre de la première page comme dans la phase 1

# for mystery_books_url in mystery_books_urls:
#     links = mystery_books_url.find_all("a")
#     link = links[0]
#     books_url = url + "catalogue" + link.get("href")[8:]
#     books_response = requests.get(books_url)
#     books_soup = BeautifulSoup(books_response.content, "html.parser")
#     products_information = books_soup.find("table", class_="table table-striped")
#     books_informations = products_information.find_all("tr")
#     universal_product_code = books_informations[0].find("td")
#     column = books_soup.find("div", class_="col-sm-6 product_main")
#     title = column.find("h1")
#     price_including_tax = books_informations[3].find("td")
#     price_excluding_tax = books_informations[2].find("td")
#     number_available = books_informations[5].find("td")
#     cat = books_soup.find("ul", class_="breadcrumb")
#     cat_book = cat.find_all("li")
#     category = cat_book[2]
#     article = books_soup.find("article", class_="product_page")
#     articles = article.find_all("p")
#     product_description = articles[3]
#     rating = column.find_all("p")
#     review_rating_text = rating[2]["class"][1]
#     review_rating = review_rating_text.split()
#     section = books_soup.find("div", class_="col-sm-6")
#     image_url_text = section.find("img").get("src")
#     image_url = image_url_text.split()
#
#     print(books_url)
#     print(universal_product_code.text)
#     print(title.text)
#     print(price_including_tax.text)
#     print(price_excluding_tax.text)
#     print(number_available.text)
#     print(category.text)
#     print(product_description.text)
#     print(review_rating[0])
#     print(url + "/catalogue/" + image_url_text)

descriptions = []
for mystery_books_url in mystery_books_urls:

    links = mystery_books_url.find_all("a")
    link = links[0]
    books_url = url + "catalogue" + link.get("href")[8:]
    books_response = requests.get(books_url)
    books_soup = BeautifulSoup(books_response.content, "html.parser")
    products_information = books_soup.find("table", class_="table table-striped")
    books_informations = products_information.find_all("tr")
    universal_product_code = books_informations[0].find("td")
    column = books_soup.find("div", class_="col-sm-6 product_main")
    title = column.find("h1")
    price_including_tax = books_informations[3].find("td")
    price_excluding_tax = books_informations[2].find("td")
    number_available = books_informations[5].find("td")
    cat = books_soup.find("ul", class_="breadcrumb")
    cat_book = cat.find_all("li")
    category = cat_book[2]
    article = books_soup.find("article", class_="product_page")
    articles = article.find_all("p")
    product_description = articles[3]
    rating = column.find_all("p")
    review_rating_text = rating[2]["class"][1]
    review_rating = review_rating_text.split()
    section = books_soup.find("div", class_="col-sm-6")
    image_url_text = section.find("img").get("src")
    image_url = image_url_text.split()
    description = [books_url, universal_product_code.text, title.text, price_including_tax.text, price_excluding_tax.text, number_available.text, product_description.text, category.text,"".join(review_rating), "".join(image_url)]
    descriptions.append(description)
    # print(description)

    # Création d'un fichier CSV avec les informations obtenues

    headers = ["books_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available","product_description", "category", "review_rating", "image_url"]
    with open("category.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(headers)
        for description in zip(descriptions):
            writer.writerow([description])




# cas où la catégorie comporte plusieurs pages, je recommence le processus ci-dessus avec les
# pages "next" détectées

# next_page = mystery_soup.find("li", class_="next")
#
# while next_page is not None:
#     next_page_relative_url = next_page.find("a")["href"]
#     next_page_url = url_mystery[0:len(url_mystery)-10] + next_page_relative_url
#     page = requests.get(next_page_url)
#     soup2 = BeautifulSoup(page.content, "html.parser")
#     next_page = soup2.find("li", class_="next")
#     # donne None
#     mystery_column_next = soup2.find("ol", class_="row")
#     mystery_books_next = mystery_column_next.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
#     mystery_books_urls_next = mystery_column_next.find_all("h3")
#
#     for mystery_books_url_next in mystery_books_urls_next:
#         links = mystery_books_url_next.find_all("a")
#         link = links[0]
#         product_page_url = url + "catalogue" + link.get("href")[8:]
#         products_next_information = soup2.find("table", class_="table table-striped")
#         books_next_informations = products_next_information.find_all("tr")
#         universal_product_code = books_next_informations[0].find("td")
#         # column = soup2.find("div", class_="col-sm-6 product_main")
#         # title = column.find("h1")
#         # price_including_tax = books_next_informations[3].find("td")
#         # price_excluding_tax = books_next_informations[2].find("td")
#         # number_available = books_next_informations[5].find("td")
#         # cat = soup2.find("ul", class_="breadcrumb")
#         # cat_book = cat.find_all("li")
#         # category = cat_book[2]
#         # article = soup2.find("article", class_="product_page")
#         # articles = article.find_all("p")
#         # product_description = articles[3]
#         # rating = column.find_all("p")
#         # review_rating_text = rating[2]["class"][1]
#         # review_rating = review_rating_text.split()
#         # section = soup2.find("div", class_="col-sm-6")
#         # image_url_text = section.find("img").get("src")
#         # image_url = image_url_text.split()
#
#         print(product_page_url)
#         # print(universal_product_code.text)
#         # print(title.text)
#         # print(price_including_tax.text)
#         # print(price_excluding_tax.text)
#         # print(number_available.text)
#         # print(category.text)
#         # print(product_description.text)
#         # print(review_rating.text)
#         # print(url + "/catalogue/" + image_url_text)
#
#
#
# # Création d'un fichier CSV avec les informations obtenues
#
# headers = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available','product_description', 'category', 'review_rating', 'image_url' ]
# with open("book.csv", "w") as csv_file:
#     writer = csv.writer(csv_file, delimiter=",")
#     writer.writerow(headers)
#     for product_catalogue_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url in zip(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url):
#         writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
#





