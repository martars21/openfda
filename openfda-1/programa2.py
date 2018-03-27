#Importo los módulos que voy a utilizar
import http.client
import json

headers = {'User-Agent': 'http-client'} #Cabeceras de mi petición. Le digo que navegador soy.
conn = http.client.HTTPSConnection("api.fda.gov") #Variable para establecer la conexión con la página web.
conn.request("GET", "/drug/label.json?limit=10", None, headers) #Mando una petición a la web de tipo GET.
#"/drug/label.json?limit=10" es el recurso que quiero en concreto.
#Pongo limit=10 porque quiero que baje 10 objetos. Si no indico nada, bajará por defecto uno (programa anterior).

resp1 = conn.getresponse() #Esta es la respuesta de la página web.
print(resp1.status, resp1.reason) #Status es un número, y reason muestra lo que quiere decir ese número. (Para comprobar que funciona bien)
respuesta = resp1.read().decode("utf-8") #"utf-8" descodifica la respuesta y lee resp1 al completo en formato json.
conn.close()

#EL módulo json sirve para tratar algo en formato json como listas y diccionarios.
resultado = json.loads(respuesta) #Para depurar json

#Ahora el json tiene una lista de 10 medicamentos, entonces la recorro con un bucle for a lo largo de toda su longitud.
for i in range (len (resultado['results'])):
    informacion_medicamento=resultado['results'][i] #El valor de la i irá de 0 y 9 (un número por cada medicamento).

    #Extraigo el id de cada uno de los medicamentos.
    ID = informacion_medicamento ['id']
    nuevai= i+1
    print ('El ID del medicamento ', nuevai, 'es: ', ID)
