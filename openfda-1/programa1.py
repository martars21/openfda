#El programa entra en OpenFDA, se descarga los medicamentos, coge uno y extrae la información pedida.
#Importo los módulos que voy a utilizar
import http.client
import json

headers = {'User-Agent': 'http-client'} #Cabeceras de mi petición. Le digo qué navegador soy.
conn = http.client.HTTPSConnection("api.fda.gov") #Variable para establecer la conexión con la página web.
conn.request("GET", "/drug/label.json", None, headers) #Mando una petición a la web de tipo GET.
#"/drug/label.json" es el recurso, donde me quiero conectar en concreto.


resp1 = conn.getresponse() #Esta es la respuesta de la página web.
print(resp1.status, resp1.reason) #Status es un número, y reason muestra lo que quiere decir ese número. (Para comprobar que funciona bien)
respuesta = resp1.read().decode("utf-8") #"utf-8" descodifica la respuesta y lee resp1 al completo en formato json.
conn.close()

#EL módulo json sirve para tratar algo en formato json como listas y diccionarios.
#Para "llamar" a los elementos de una lista, pongo entre corchetes la posición donde se encuentra el elemento que quiero imprimir.
resultado = json.loads(respuesta)
informacion_medicamento=resultado['results'][0] #Para meterme en el resultado


#Extraigo el ID, el propósito y el fabricante del medicamento.
ID = informacion_medicamento['id']
Proposito = informacion_medicamento['purpose'][0]
Fabricante = informacion_medicamento['openfda']['manufacturer_name'][0]

print ('El ID del medicamento es: ',ID)
print ('El propósito del medicamento es: ',Proposito)
print ('El fabricante del medicamento es: ',Fabricante)