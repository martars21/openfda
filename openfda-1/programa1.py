#Importo los módulos que voy a utilizar
import http.client
import json

headers = {'User-Agent': 'http-client'}

#Establecemos la conexión con la página web
conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json", None, headers)
#"/drug/label.json" es el recurso, donde me quiero conectar en concreto.

#Respuesta de la página web
resp1 = conn.getresponse()

#Comprobamos si fuciona bien
print(resp1.status, resp1.reason)
if resp1.status == 200:
    print ("Todo correcto")
else:
    print("El recurso no está disponible")

respuesta = resp1.read().decode("utf-8") #Descodificamos la respuesta
conn.close()

resultado = json.loads(respuesta) #Loads convierte al json en un objeto de python (con listas y diccionarios)

informacion_medicamento=resultado['results'][0]


#Extraigo el ID, el propósito y el fabricante del medicamento.
ID = informacion_medicamento['id']
Proposito = informacion_medicamento['purpose'][0]
Fabricante = informacion_medicamento['openfda']['manufacturer_name'][0]

print ('El ID del medicamento es: ',ID)
print ('El propósito del medicamento es: ',Proposito)
print ('El fabricante del medicamento es: ',Fabricante)