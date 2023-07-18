import lxml
import requests
import re
from bs4 import BeautifulSoup
import subprocess
import os
import glob

# Especifica las extensiones de los archivos que quieres eliminar
extensions = ['*.m3u8', '*.txt']
for extension in extensions:
    # Busca todos los archivos con la extensión especificada
    files_to_delete = glob.glob(extension)
    for file_name in files_to_delete:
        # Si existe, elimínalo
        os.remove(file_name)
        print(f"Archivo {file_name} eliminado.")
base = "https://www.machogaytube.com"

input(f"introduce una web, por ejemplo: {base} \n")

menu = ["/categories/", "/channels/"]

entrada = input("Ver menu categorias pulsa 1, ver menu canales pulsa 2: \n")
print(f"Pulsaste la opción: {entrada}")
i = int(entrada)-1
print("has escogido : " + menu[i])

url = base+menu[i]
print(f"Configurada la que url de la que se extraerán los videos.\nEs:\n- {base}")
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
categorias = []
for link in soup.find_all('a'):
	href = link.get('href')
	if i < 1:
		buscar = "/category/"
	else:
		buscar = "/channels/"
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

   
	
    
	






