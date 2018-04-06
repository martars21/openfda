#Importo las librerías que voy a utilizar
import http.server
import socketserver
import http.client
import json

PORT = 9898

def lista_medic():

    lista_nombres = []
    headers = {'User-Agent': 'http-client'}

    #Establecemos la conexión con la página web
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=10", None, headers)

    #Respuesta de la página web
    resp1 = conn.getresponse()
    print(resp1.status, resp1.reason)
    if resp1.status == 200:
        print ("Todo correcto")
    else:
        ("El recurso no está disponible")
    respuesta = resp1.read().decode("utf-8") #Descodificamos la respuesta
    conn.close() #Cerramos la conexión


    resultado = json.loads(respuesta) #Convertimos el json en un objeto de python

    #Extraemos la información y la metemos en listas
    for i in range(len(resultado['results'])):
        informacion_medicamento = resultado['results'][i]
        if (informacion_medicamento['openfda']):
            nombre_medicamento = informacion_medicamento['openfda']['substance_name'][0]
            nuevai = i + 1

            print('El medicamento ',nuevai,' es: ',nombre_medicamento )

            lista_nombres.append(nombre_medicamento)
        else:
            nuevai=i+1
            print('El nombre del medicamento ',nuevai,' no está especificado ')
            lista_nombres.append("El nombre del medicamento no esta especificado")

    return lista_nombres

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200) #Respuesta del status. Indicando que funciona bien.

        self.send_header('Content-type', 'text/html') #Indica el tipo de información que me va a devolver
        self.end_headers()

        #Creación del html
        contenido_html="""<!doctype html>
                <html>
                <body style = 'background-color: pink'>
                        <h1>Medicamentos</h2>
                </body>
                </html>"""

        lista_nombres = lista_medic () #Llamo a la función que crea la lista con los datos
        for i in lista_nombres:
            contenido_html =contenido_html + '<ul><li>' + i + '</li></ul>' + '</br>'

        #Ya está el html creado

        self.wfile.write(bytes(contenido_html, "utf8"))

        return


# Servidor
Handler = testHTTPRequestHandler #El manejador es nuestra propia clase

#Conexión al servidor
httpd = socketserver.TCPServer(("", PORT), Handler)
print("Sirviendo en el puerto", PORT)

#El servidor estará siempre activo
try:
    httpd.serve_forever()

#Si paramos el servidor
except KeyboardInterrupt:
    print("El usuario ha parado el servidor")
httpd.server_close()
print("Servidor en pausa")









