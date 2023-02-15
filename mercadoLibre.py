from bs4 import BeautifulSoup as bs
import requests
import csv
import pandas as pd


#First, the user must enter what he want to search, I must format the strings and change the blank spaces to put it inside the url
peticion1 = str(input('¿Que querés buscar?: ')).replace(' ','%20')
peticion2 = peticion1.replace('%20','-')

#The script acces to the page
html = requests.get(f'https://listado.mercadolibre.com.ar/{peticion2}#D[A:{peticion1}]').text

soup = bs(html, 'lxml')







#The script search the total amount of pages
paginaMaxima = soup.find('li',class_='andes-pagination__page-count').text.replace('de ','')
paginaMaxima = int(paginaMaxima)
print(paginaMaxima)



#Get the total products of the page
lista = soup.find_all('li', class_='ui-search-layout__item shops__layout-item')

#The script create the list of names and prices
listaNombre = []
listaPrecio = []
#Put the link in a variable
link = f'https://listado.mercadolibre.com.ar/{peticion2}#D[A:{peticion1}]'

#A while for scrap each page of the product that we search in Mercado Libre
while True:
    #First,the scripe determine in wich page is it
    pagina = soup.find('span', 
    class_='andes-pagination__link').text
    pagina = int(pagina)
    print(pagina)

    #Get the link and parse it
    html = requests.get(link).text

    soup = bs(html, 'lxml')

    lista = soup.find_all('li', class_='ui-search-layout__item shops__layout-item')

    #Get the link to the next page
    for href in soup.find_all('a',href=True,class_='andes-pagination__link shops__pagination-link ui-search-link'):
        link = href.get('href')


    #List the name and the price of the items
    for elementos in lista:
        nombreProducto = elementos.find('div', class_='ui-search-item__group ui-search-item__group--title shops__items-group').text.strip()
        precioProducto = elementos.find('span', class_='price-tag-amount').text.replace('$','').strip()
        print(f'{nombreProducto + " " + precioProducto}')
    
        #Inser the name and price of each item and save it to the list
        listaNombre.append(nombreProducto)
        listaPrecio.append(precioProducto)

    #if the current page it equal to the total amount of pages, then the while end
    if pagina == paginaMaxima:
        break
    



#The columns of the dataFrame
columnas = ['Nombre','Precio']
#Create the dataFrame
df = pd.DataFrame(list(zip(listaNombre,listaPrecio)), columns=columnas).drop_duplicates()


print(df)
#Create the csv with the information
df.to_csv(f'{peticion2}.csv', index=False)



