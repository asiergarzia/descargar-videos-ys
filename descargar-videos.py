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

while True:
    entrada = input("- categorias --> pulsa 1\n- canales --> pulsa 2\n- pornstars --> pulsa 3: \n")
    try:
        i = int(entrada) - 1
        if i in [0, 1, 2]:
            url = base+menu[i]
            print("has escogido : " + menu[i])
            break
        else:
            print("Por favor, introduce 1, 2 o 3.")
    except ValueError:
        print("Por favor, introduce un número.")


print(f"Configurada la que url de la que se extraerán los videos.\nEs:\n- {base}")
try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
except requests.RequestException as e:
    print(f"Error al solicitar la URL {url}: {e}")
    sys.exit(1)

categorias = []
if i==0:
	buscar = "/category/"
elif i==1:
    buscar = "/channels/"
else:
    buscar = "/pornstar/"
for link in soup.find_all('a'):
	href = link.get('href')
	
	if href and href.startswith(buscar):
		categorias.append(href[10:])
for categoria in categorias:
	print(categorias.index(categoria)+1,"-", categoria)
numero=1
numerotxt = input("Escoge una categoria: \n")
varios = []
for posicion in numerotxt:
	if posicion == ",":
		varios = numerotxt.split(",")
		break
if len(varios) < 1:   
	varios.append(numerotxt)
print("longitud varios: ",len(varios)) 
for v in varios:    
	n = int(v)-1
	print(f"Se descargaran los videos de la categoria: {categorias[n]}")
	cate = categorias[n]
	url = base+buscar+categorias[n]
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
	comando = f"youtube-dl -i -g -a {fileout} > {fileout}.m3u8"
	resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
	if resultado.returncode == 0:
		print("El comando se ejecutó correctamente:")
		print(resultado.stdout)
	else:
		print("Se produjo un error al ejecutar el comando:")
		print(resultado.stderr)
