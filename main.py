# import des bibliothèques
import csv

import requests
from bs4 import BeautifulSoup


# requête sur l'url de la page et extraction des données html

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

#---------------PHASE 1 ---------------------


   # Extraction de l'url de la page du produit

product_catalogue_url = soup.find_all("ol", class_="row")

for links in product_catalogue_url:
    link = links.find_all("a")

url_catalogue = link[0].get('href')
product_page_url = url + url_catalogue



    # Extraction des données de la page du livre choisi, avec BeautifulSoup


book_response = requests.get(product_page_url)
book_soup = BeautifulSoup(book_response.content, "html.parser")

    # extraction des informations produit

product_information = book_soup.find("table", class_="table table-striped")
informations = product_information.find_all("tr")



    # Extraction de l'UPC

universal_product_code = informations[0].find("td")


    # Extraction du titre du livre

column = book_soup.find("div", class_="col-sm-6 product_main")
title = column.find("h1")


    # Extraction du prix avec taxes

price_including_tax = informations[3].find("td")


    #Extraction du prix sans taxes

price_excluding_tax = informations[2].find("td")



    # Extraction du nombre de livre disponibles

number_available = informations[5].find("td")



    # Extraction de la catégorie du livre

cat = book_soup.find("ul", class_="breadcrumb")
cat_book = cat.find_all("li")
category = cat_book[2]


    # Desciption du produit

article = book_soup.find("article", class_="product_page")
articles = article.find_all("p")
product_description = articles[3]


    # Extraction de l'évaluation du livre

rating = column.find_all("p")
review_rating_text = rating[2]["class"][1]


    # Extraction de l'url de l'image

section = book_soup.find("div", class_="col-sm-6")
image_url_text = section.find("img").get("src")
image_url = url + image_url_text[6:]



informations = (product_page_url, universal_product_code.text, title.text,
                price_including_tax.text, price_excluding_tax.text, number_available.text,
                category.text.strip(), product_description.text, review_rating_text, image_url)


    # Création d'un fichier CSV avec les informations obtenues

headers = ["product_page_url", "universal_product_code", "title", "price_including_tax",
           "price_excluding_tax", "number_available","product_description", "category", "review_rating", "image_url"]
with open("book.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(headers)
    writer.writerow(informations)



#---------------PHASE 2 ---------------------

    # je choisis la catégorie Mystery : 32 livres sur 2 pages

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
    image_url = url+image_url_text[6:]
    description = [books_url, universal_product_code.text, title.text, price_including_tax.text,
                   price_excluding_tax.text, number_available.text, product_description.text,
                   category.text.strip(),"".join(review_rating), image_url]
    descriptions.append(description)


    # Création d'un fichier CSV avec les informations obtenues

headers = ["books_url", "universal_product_code", "title", "price_including_tax",
           "price_excluding_tax", "number_available","product_description",
           "category", "review_rating", "image_url"]
with open("category.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(headers)
    for description in descriptions:
        writer.writerow(description)





    # cas où la catégorie comporte plusieurs pages, je recommence le processus ci-dessus avec les
    # pages "next" détectées

next_page = mystery_soup.find("li", class_="next")

while next_page is not None:
    next_page_relative_url = next_page.find("a")["href"]
    next_page_url = url_mystery[0:len(url_mystery)-10] + next_page_relative_url
    page = requests.get(next_page_url)
    soup2 = BeautifulSoup(page.content, "html.parser")
    next_page = soup2.find("li", class_="next")

    mystery_column_next = soup2.find("ol", class_="row")
    mystery_books_next = mystery_column_next.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    mystery_books_urls_next = mystery_column_next.find_all("h3")

    descriptions_next = []
    for mystery_books_url_next in mystery_books_urls_next:
        links = mystery_books_url_next.find_all("a")
        link = links[0]
        books_next_page_urls = url + "catalogue" + link.get("href")[8:]
        books_next_response = requests.get(books_next_page_urls)
        books_next_soup = BeautifulSoup(books_next_response.content, "html.parser")
        products_next_information = books_next_soup.find("table", class_="table table-striped")
        books_next_informations = products_next_information.find_all("tr")
        universal_product_code = books_next_informations[0].find("td")
        column = books_next_soup.find("div", class_="col-sm-6 product_main")
        title = column.find("h1")
        price_including_tax = books_next_informations[3].find("td")
        price_excluding_tax = books_next_informations[2].find("td")
        number_available = books_next_informations[5].find("td")
        cat = books_next_soup.find("ul", class_="breadcrumb")
        cat_book = cat.find_all("li")
        category = cat_book[2]
        article = books_next_soup.find("article", class_="product_page")
        articles = article.find_all("p")
        product_description = articles[3]
        rating = column.find_all("p")
        review_rating_text = rating[2]["class"][1]
        review_rating = review_rating_text.split()
        section = books_next_soup.find("div", class_="col-sm-6")
        image_url_text = section.find("img").get("src")
        image_url_next = url + image_url_text[6:]

        description_next = [books_next_page_urls, universal_product_code.text, title.text,price_including_tax.text,
                            price_excluding_tax.text, number_available.text, product_description.text,
                            category.text.strip(),"".join(review_rating), image_url_next]
        descriptions_next.append(description_next)



#     # Création d'un fichier CSV avec les informations obtenues
#
headers = ['books_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax',
           'number_available','product_description', 'category', 'review_rating', 'image_url' ]
with open("category_next.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(headers)
    for description_next in descriptions_next:
        writer.writerow(description_next)

    # Création du fichier csv contenant l'ensemble des informations de la catégorie


with open("category.csv", "r") as file1:
    data1 = list(csv.reader(file1, delimiter=","))

with open("category_next.csv", "r") as file2:
    data2 = list(csv.reader(file2, delimiter=","))
for line in data2[1:]:
    data1.append(line)

headers = data1[0]
with open("full_category.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(headers)
    for element in data1[1:]:
        writer.writerow(element)



#---------------PHASE 3 ---------------------


    #extraction des catégories de livres

aside = soup.find("div", class_="side_categories")
categories = aside.find("ul").find("li").find("ul")
urls_categories = categories.find_all("li")

descriptions_books_categories = []
for urls_category in urls_categories:
    links = urls_category.find_all("a")
    link = links[0]
    category_urls = url + link.get("href")

    response_category = requests.get(category_urls)
    category_soup = BeautifulSoup(response_category.content, "html.parser")

    category_column = category_soup.find("ol", class_="row")
    category_books = category_column.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    category_books_urls = category_column.find_all("h3")

    # on boucle - pour chaque catégorie - sur l'ensemble des livres de la première page

    for category_books_url in category_books_urls:
        links = category_books_url.find_all("a")
        link = links[0]
        every_books_url = url + "catalogue" + link.get("href")[8:]
        every_books_response = requests.get(every_books_url)
        every_book_soup = BeautifulSoup(every_books_response.content, "html.parser")
        products_next_information = every_book_soup.find("table", class_="table table-striped")
        books_next_informations = products_next_information.find_all("tr")
        universal_product_code = books_next_informations[0].find("td")
        column = every_book_soup.find("div", class_="col-sm-6 product_main")
        title = column.find("h1")
        price_including_tax = books_next_informations[3].find("td")
        price_excluding_tax = books_next_informations[2].find("td")
        number_available = books_next_informations[5].find("td")
        cat = every_book_soup.find("ul", class_="breadcrumb")
        cat_book = cat.find_all("li")
        category = cat_book[2]
        article = every_book_soup.find("article", class_="product_page")
        articles = article.find_all("p")
        product_description = articles[3]
        rating = column.find_all("p")
        review_rating_text = rating[2]["class"][1]
        review_rating = review_rating_text.split()
        section = every_book_soup.find("div", class_="col-sm-6")
        image_url_text = section.find("img").get("src")
        image_url_category_first_page = url + image_url_text[6:]

#         description_books_categories = [every_books_url, universal_product_code.text, title.text,
#                                         price_including_tax.text, price_excluding_tax.text, number_available.text,
#                                         product_description.text.strip(),
#                                         category.text.strip(), "".join(review_rating), image_url_category_first_page]
#
#         descriptions_books_categories.append(description_books_categories)
#
#
# headers = ["books_url", "universal_product_code", "title", "price_including_tax",
#            "price_excluding_tax", "number_available","product_description",
#            "category", "review_rating", "image_url"]
# with open("books_category_first_page.csv", "w", encoding='utf-8', newline="") as csv_file:
#     writer = csv.writer(csv_file, delimiter=",")
#     writer.writerow(headers)
#     for description_books_categories in descriptions_books_categories:
#         writer.writerow(description_books_categories)

# on réitère le processus pour chaque "page suivante" de chaque catégorie

descriptions_next = []
for urls_category in urls_categories:
    links = urls_category.find_all("a")
    link = links[0]
    category_urls = url + link.get("href")

    category_reponse = requests.get(category_urls)
    category_soup = BeautifulSoup(category_reponse.content, "html.parser")

    next_page = category_soup.find("li", class_="next")

    while next_page is not None:
        next_page_relative_url = next_page.find("a")["href"]
        next_page_url = category_urls[0:len(category_urls) - 10] + next_page_relative_url
        page = requests.get(next_page_url)
        soup2 = BeautifulSoup(page.content, "html.parser")
        next_page = soup2.find("li", class_="next")

        category_column_next = soup2.find("ol", class_="row")
        category_books_next = category_column_next.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        category_books_urls_next = category_column_next.find_all("h3")

        for category_books_url_next in category_books_urls_next:
            links = category_books_url_next.find_all("a")
            link = links[0]
            books_next_page_urls = url + "catalogue" + link.get("href")[8:]
            books_next_response = requests.get(books_next_page_urls)
            books_next_soup = BeautifulSoup(books_next_response.content, "html.parser")
            products_next_information = books_next_soup.find("table", class_="table table-striped")
            books_next_informations = products_next_information.find_all("tr")
            universal_product_code = books_next_informations[0].find("td")
            column = books_next_soup.find("div", class_="col-sm-6 product_main")
            title = column.find("h1")
            price_including_tax = books_next_informations[3].find("td")
            price_excluding_tax = books_next_informations[2].find("td")
            number_available = books_next_informations[5].find("td")
            cat = books_next_soup.find("ul", class_="breadcrumb")
            cat_book = cat.find_all("li")
            category = cat_book[2]
            article = books_next_soup.find("article", class_="product_page")
            articles = article.find_all("p")
            product_description = articles[3]
            rating = column.find_all("p")
            review_rating_text = rating[2]["class"][1]
            review_rating = review_rating_text.split()
            section = books_next_soup.find("div", class_="col-sm-6")
            image_url_text = section.find("img").get("src")
            image_url_next = url + image_url_text[6:]

            filename = title.text
            image = requests.get(image_url_category_first_page)
            with open(filename.strip()+".jpg", "wb") as f:
                f.write(image.content)



#             description_next = [books_next_page_urls, universal_product_code.text, title.text, price_including_tax.text,
#                                 price_excluding_tax.text, number_available.text, product_description.text.strip(),
#                                 category.text.strip(), "".join(review_rating), image_url_next]
#             descriptions_next.append(description_next)
#
# headers = ["books_url", "universal_product_code", "title", "price_including_tax",
#            "price_excluding_tax", "number_available", "product_description",
#            "category", "review_rating", "image_url"]
# with (open("books_category_next_page.csv", "w", encoding='utf-8', newline="") as csv_file):
#     writer = csv.writer(csv_file, delimiter=",")
#     writer.writerow(headers)
#     for description_next in descriptions_next:
#         writer.writerow(description_next)



#---------------PHASE 4 ---------------------










