import requests
import re
from bs4 import BeautifulSoup
import subprocess
import os
import glob
import sys



# Especifica las extensiones de los archivos que quieres eliminar
extensions = ['*.m3u8', '*.m3u']
for extension in extensions:
    # Busca todos los archivos con la extensión especificada
    files_to_delete = glob.glob(extension)
    for file_name in files_to_delete:
        # Si existe, elimínalo
        os.remove(file_name)
        print(f"Archivo {file_name} eliminado.")
base = "https://www.machogaytube.com"
base = input(f"introduce una web, por ejemplo: {base} \n") or "https://www.machogaytube.com"
print(f"La web ingresada es: {base}")

menu = ["/categories/", "/channels/", "/pornstars/"]
buscar = ["/category/", "/channels/", "/pornstar/"]

while True:
    entrada = input("- categorias --> pulsa 1\n- canales --> pulsa 2\n- pornstars --> pulsa 3: \n")
    try:
        i = int(entrada) - 1
        if i in [0, 1, 2]:
            url = base+menu[i]
            url_cola = str(buscar[i])
            print("has escogido : " + menu[i])
            break
        else:
            print("Por favor, introduce 1, 2 o 3.")
    except ValueError:
        print("Por favor, introduce un número.")
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
    
categorias = []
indice = []
varios = []
cola = []
k=1
for link in soup.find_all('a'):
	href = link.get('href')
	if href and href.startswith(url_cola):
		cola.append(k)
		cola.append(href[10:])
		categorias.append(href[10:])
		k+=1
for c in range (0, len(cola), 200):
	print(str(cola[c:c+200])+"\n")
	agregar_varios = input("Presiona Enter para ver más categorías...")	

indice = []
numero=1
numerotxt = input("Escoge una categoria o varias seguidas por , : \n")
for posicion in numerotxt:
	if posicion == ",":
		varios = numerotxt.split(",")
		break
	else:
		varios.append(numerotxt)
for agregar in agregar_varios:
	varios.append(agregar) 

for v in varios:
	try:
		n = int(v)-1
		if n in range(len(categorias)):
			indice.append(n)
		else:
       			print("Por favor, introduce un numero entre 1 y ", len(categorias))
	
	
	except ValueError:
  		print("Por favor, introduce un número.")


with open("archivo_urls.txt", "a") as file_out:
	for ind in indice:
		i = int(ind) 
		print(f"Se descargaran los videos de la categoria: {categorias[n]}")
		cate = categorias[n]
		url = base+url_cola+cate
		print(url)
		response2 = requests.get(url)
		soup2 = BeautifulSoup(response2.text, 'html.parser')
	enlaces= []
	fileout = f"machogaytube_{cate}.txt"
	
	for link in soup2.find_all('a'):
		href = link.get('href')
		if href and href.startswith('/movies/'):
			enlaces.append(href)
	with open(fileout, 'w') as f_output:
		for enlace in enlaces:
			print(base+enlace+"\n")
			f_output.write(base+enlace+"\n")
	with open("archivo_urls.txt", 'w') as file_output:
		for enlace in enlaces:
			print(base+enlace+"\n")
			file_output.write(base+enlace+"\n")
	comando = f"youtube-dl -i -g -a {fileout} > {fileout}.m3u8"
	resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
	if resultado.returncode == 0:
		print("El comando se ejecutó correctamente:")
		print(f"Se ha creado el archivo {fileout}.m3u8")
		print(resultado.stdout)
	else:
		print("Se produjo un error al ejecutar el comando:")
		print(resultado.stderr)
