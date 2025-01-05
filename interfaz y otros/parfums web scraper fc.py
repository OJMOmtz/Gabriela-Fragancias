import requests
from bs4 import BeautifulSoup
import certifi

# URL base
url_base = "https://www.farmacenter.com.py/perfumes"

# Lista para almacenar los datos
productos = []

# Hacer una solicitud GET a la página web
for i in range(1, 189):
    if i == 1:
        url = url_base
    else:
        url = f"{url_base}.{i}"
    
    respuesta = requests.get(url, verify=certifi.where())
    
    # Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(respuesta.text, "html.parser")
    
    # Encontrar todos los elementos que contengan los datos de los productos
    elementos = soup.find_all("div", class_="product-item")
    
    # Extraer los datos de cada producto
    for elemento in elementos:
        nombre = elemento.find("h2", class_="product-name").text.strip()
        precio = elemento.find("span", class_="price").text.strip()
        
        # Agregar los datos a la lista
        productos.append({"nombre": nombre, "precio": precio})

# Imprimir los datos extraídos
for producto in productos:
    print(f"Nombre: {producto['nombre']}")
    print(f"Precio: {producto['precio']}")
    print()