import http.server
import http.client
import json
import socketserver

PORT=8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):


    URL="api.fda.gov"
    EVENT="/drug/label.json"
    DRUG='&search=active_ingredient:'
    COMPANY='&search=openfda.manufacturer_name:'


    def pagina_principal(self): #Para devolver el formulario cuando se pide el recurso /
        #Creación de la página web html con los cinco formularios. Todos de método Get
        web_html = """
            <html>
            <body style = 'background-color: pink'>
                <head>
                    <title>APLICACION DE OPENFDA</title>
                </head>
                <body>
                    <h1>OpenFDA Formulario</h1>
                    <img src = "https://lasaludmovil.files.wordpress.com/2014/06/openfda_logo.jpg">
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    _________________________________________________
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    _________________________________________________
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    _________________________________________________
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    _________________________________________________
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                </body>
            </html>
                """
        return web_html

    #Función que me devuelve la página html con la información solicitada
    def pagina_web (self, lista):
        lista_html = """
                                <html>
                                <body style = 'background-color: pink'>
                                    <head>
                                        <title>APLICACION DE OpenFDA</title>
                                    </head>
                                    <body>
                                    <h1>Listado con la informacion solicitada</h1>
                                        <ul>
                            """
        #Para hacer una lista en el html
        for item in lista:
            lista_html = lista_html + "<li>" + item + "</li>"

        lista_html = lista_html +  """
                                        </ul>
                                    </body>
                                </html>
                            """
        return lista_html

    #Función para obtener los resultados de la página de openFDA
    def resultados_genericos (self, limit=10):
        conn = http.client.HTTPSConnection(self.URL) #Establecemos conexión con la página de OpenFDA
        conn.request("GET", self.EVENT + "?limit="+str(limit))
        print (self.EVENT + "?limit="+str(limit))
        resp1 = conn.getresponse() #Respuesta de la página web
        respuesta = resp1.read().decode("utf8") #Descodificamos la respuesta
        resultado = json.loads(respuesta)  #Convertimos el json en un objeto de python
        resultados = resultado['results']
        return resultados

    def do_GET(self):

        #Obtener parámetros
        recurso_list = self.path.split("?") #Separamos en la url por donde haya ?
        if len(recurso_list) > 1:
            parametro = recurso_list[1]
        else:
            parametro = ""

        limit = 1 #Límite por defecto

        # Obtener el límite
        if parametro:
            parse_limit = parametro.split("=") #Separamos por donde haya =
            if parse_limit[0] == "limit":
                limit = int(parse_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("SIN PARAMETROS")


        if self.path=='/': #Este recurso tiene 5 formularios, es la página principal
            self.send_response(200) #Respuesta para indicar que funciona correctamente
            self.send_header('Content-type', 'text/html') #Tipo de contenido
            self.end_headers()
            html=self.pagina_principal() #Llamamos a la función de página principal
            self.wfile.write(bytes(html, "utf8"))


        elif 'listDrugs' in self.path: #Recurso para la lista de medicamentos
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            medicamentos_lista = [] #Creamos una lista vacía donde se añadirán los elementos del json
            resultados = self.resultados_genericos(limit)
            #Añado los medicamentos a la lista
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    medicamentos_lista.append (resultado['openfda']['generic_name'][0])
                else:
                    medicamentos_lista.append('Nombre de medicamento no especificado')
            resultado_html = self.pagina_web (medicamentos_lista) #Llamamos a la función de la web html con la lista de medicamentos
            self.wfile.write(bytes(resultado_html, "utf8"))


        elif 'listCompanies' in self.path: #Recurso para la lista de fabricantes
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            companies_lista = [] #Creamos una lista vacía donde se añadirán los elementos del json
            resultados = self.resultados_genericos (limit)
            #Añado los fabricantes a la lista
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    companies_lista.append (resultado['openfda']['manufacturer_name'][0])
                else:
                    companies_lista.append('Nombre de fabricante no especificado')
            resultado_html = self.pagina_web(companies_lista) #Llamamos a la función de la web html con la lista de fabricantes
            self.wfile.write(bytes(resultado_html, "utf8"))


        elif 'listWarnings' in self.path: #Recurso para la lista de warnings
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            warnings_lista = [] #Creamos una lista vacía donde se añadirán los elementos del json
            resultados = self.resultados_genericos (limit)
            #Añado los warnings a la lista
            for resultado in resultados:
                if ('warnings' in resultado):
                    warnings_lista.append (resultado['warnings'][0])
                else:
                    warnings_lista.append('No especificado')
            resultado_html = self.pagina_web(warnings_lista) #Llamamos a la función de la web html con la lista de warnings
            self.wfile.write(bytes(resultado_html, "utf8"))


        elif 'searchDrug' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            #Por defecto 10 medicamentos
            limit = 10
            #Extraigo el nombre del medicamento
            drug=self.path.split('=')[1]
            drugs_lista = [] #Creo una lista vacía
            #Me conecto a OpenFDA y meto en la lista los medicamentos
            conn = http.client.HTTPSConnection(self.URL) #Establecemos conexión con la página web
            conn.request("GET", self.EVENT + "?limit="+str(limit) + self.DRUG + drug)
            resp1 = conn.getresponse() #Respuesta de la página web
            respuesta = resp1.read().decode("utf8") #Descodificamos la respuesta
            resultado = json.loads(respuesta) #Convertimos el json en un objeto de python
            search_drug = resultado['results']
            for resultado in search_drug:
                if ('active_ingredient' in resultado['openfda']):
                    drugs_lista.append(resultado['openfda']['active_ingredient'][0])
                else:
                    drugs_lista.append('Medicamento desconocido')
            resultado_html = self.pagina_web(drugs_lista) #Llamamos a la función de la página html
            self.wfile.write(bytes(resultado_html, "utf8"))


        elif 'searchCompany' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            #Por defecto 10 fabricantes
            limit = 10
            #Extraigo el nombre del fabricante
            company=self.path.split('=')[1]
            companies_lista1 = [] #Creo una lista vacía
            #Me conecto a openFDA y meto en la lista los fabricantes
            conn = http.client.HTTPSConnection(self.URL) #Establecemos conexión con la página web
            conn.request("GET", self.EVENT + "?limit=" + str(limit) + self.COMPANY + company)
            resp1 = conn.getresponse() #Respuesta de la página web
            respuesta = resp1.read().decode("utf8") #Descodificamos la respuesta
            resultado = json.loads(respuesta) #Convertimos el json en un objeto de python
            search_company = resultado['results']
            for event in search_company:
                companies_lista1.append(event['openfda']['manufacturer_name'][0])
            resultado_html = self.pagina_web(companies_lista1) #Llamamos a la función de la página html
            self.wfile.write(bytes(resultado_html, "utf8"))


        #Con el recurso redirect se redirige a la página principal, la del formulario
        elif 'redirect' in self.path:
            print ("Redirección a la página principal")
            self.send_response(302)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()


        #Secret nos indica que no estamos autorizados
        elif 'secret' in self.path:
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()

        #Si no es ninguno de los casos anteriores, enviamos código de error 404, recurso no encontrado
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())


        return


#Aquí empieza a funcionar.
socketserver.TCPServer.allow_reuse_address= True

#Manejador que controla nuestra clase
Handler = testHTTPRequestHandler

#Asocia la IP al puerto. Se inicia el servidor que funcionará para siempre
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()