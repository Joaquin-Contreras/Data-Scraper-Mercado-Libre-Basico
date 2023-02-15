from bs4 import BeautifulSoup as bs
import requests
import csv
import pandas as pd



peticion1 = str(input('¿Que querés buscar?: ')).replace(' ','%20')
peticion2 = peticion1.replace('%20','-')

html = requests.get(f'https://listado.mercadolibre.com.ar/{peticion2}#D[A:{peticion1}]').text

soup = bs(html, 'lxml')








paginaMaxima = soup.find('li',class_='andes-pagination__page-count').text.replace('de ','')
paginaMaxima = int(paginaMaxima)
print(paginaMaxima)




lista = soup.find_all('li', class_='ui-search-layout__item shops__layout-item')

listaNombre = []
listaPrecio = []
link = f'https://listado.mercadolibre.com.ar/{peticion2}#D[A:{peticion1}]'

while True:
    
    pagina = soup.find('span', 
    class_='andes-pagination__link').text
    pagina = int(pagina)
    print(pagina)


    html = requests.get(link).text

    soup = bs(html, 'lxml')

    lista = soup.find_all('li', class_='ui-search-layout__item shops__layout-item')


    for href in soup.find_all('a',href=True,class_='andes-pagination__link shops__pagination-link ui-search-link'):
        link = href.get('href')


  
    for elementos in lista:
        nombreProducto = elementos.find('div', class_='ui-search-item__group ui-search-item__group--title shops__items-group').text.strip()
        precioProducto = elementos.find('span', class_='price-tag-amount').text.replace('$','').strip()
        texto = nombreProducto + " " + precioProducto
    

        listaNombre.append(nombreProducto)
    
        listaPrecio.append(precioProducto)


    if pagina == paginaMaxima:
        break
    




columnas = ['Nombre','Precio']

df = pd.DataFrame(list(zip(listaNombre,listaPrecio)), columns=columnas).drop_duplicates()


print(df)

df.to_csv(f'{peticion2}.csv', index=False)



