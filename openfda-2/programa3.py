#Importamos módulos que se van a usar
import http.client
import json

headers={'User-Agent':'http-client'}
skip_cont=0

while True:

    #Establecemos la conexión con la página web.
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", '/drug/label.json?limit=100&skip='+str(skip_cont)+'&search=active_ingredient:"acetylsalicylic"', None, headers)

    resp1 = conn.getresponse()

    #Comprobamos que funciona bien
    print(resp1.status, resp1.reason)
    if resp1.status == 200:
        print ("Todo correcto")
    else:
        print("El recurso no está disponible")

    respuesta = resp1.read().decode("utf-8") #Descodificamos la respuesta
    conn.close()

    resultado = json.loads(respuesta) #Depurar el json para convertirlo en un objeto de Python.

    #Obtención de resultados
    for i in range(len (resultado['results'])):
        informacion_medicamento=resultado['results'][i]

        nuevai = i+1+skip_cont

        ID = informacion_medicamento['id']
        print('El ID del medicamento ', nuevai, 'es: ', ID)

        if (informacion_medicamento['openfda']):
            Fabricante = informacion_medicamento['openfda']['manufacturer_name'][0]
            print('El fabricante del medicamento es: ',Fabricante)
        else:
            print('El fabricante del medicamento no está especificado')

    if (len(resultado['results'])<100):
        print('Ya no hay más medicamentos')
        break

    skip_cont=skip_cont+100

    #Skip sirve para obtener medicamentos de 100 en 100.
    #El proceso de conexión y obtención de resultados está dentro de un bucle while.
    #Romperemos el bucle cuando la longitud de los resultados sea menor que 100 porque eso significará que ya no hay más medicamentos del tipo que se buscan.