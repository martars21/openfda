#Importo los módulos que voy a utilizar
import http.client
import json

headers = {'User-Agent': 'http-client'}

#Establecemos la conexión con la página web
conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json?limit=10", None, headers)
#Pongo limit=10 porque quiero que baje 10 objetos.

#Respuesta de la página web
resp1 = conn.getresponse()

#Comprobamos que funciona correctamente
print(resp1.status, resp1.reason)
if resp1.status == 200:
    print ("Todo correcto")
else:
    print("El recurso no está disponible")

respuesta = resp1.read().decode("utf-8") #Descodificamos la respuesta

conn.close()


resultado = json.loads(respuesta) #Loads convierte el json en un objeto de python.

for i in range (len (resultado['results'])):
    informacion_medicamento=resultado['results'][i] #El valor de la i irá de 0 y 9 (un número por cada medicamento).

    #Extraigo el id de cada uno de los medicamentos.
    ID = informacion_medicamento ['id']
    nuevai= i+1
    print ('El ID del medicamento ', nuevai, 'es: ', ID)
