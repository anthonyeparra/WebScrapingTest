# WEB SCRAPING TEST - PLATAFORM

## Requisitos de la Aplicación

La aplicación requiere tener:

1. Python en su versión 3.10
2. Serverless Framework
3. Plugin de requirements
4. Plugin offline
5. Crear entorno virtual
6. Instalar dependencia
7. Ejecutar el serverless offline
8. Base de datos

### Instrucciones

1. **Instalar Python 3.10**

   Asegúrate de tener Python 3.10 instalado. Puedes descargarlo desde [python.org](https://www.python.org/downloads/release/python-3100/).

2. **Instalar Serverless Framework**

   Para instalar Serverless Framework, ejecuta el siguiente comando:

   ```sh
   npm install -g serverless

3. **Instalar Plugin Requirements**

   Instala el plugin de requirements con el siguiente comando:

   ```sh
   serverless plugin install -n serverless-python-requirements

4. **Instalar Plugin offline**

   Instala el plugin offline con el siguiente comando:

   ```sh
   serverless plugin install -n serverless-offline

5. **Crear entorno virtual**

    Crea un entorno virtual para la aplicación con los siguientes comandos:

    ```sh
    python -m venv venv
    # Para Linux o Macos
    source venv/bin/activate
    # Para Windows
    venv\Scripts\activate

6. **Instalar dependencias**

   Asegúrate de que el archivo requirements.txt esté en el directorio del proyecto. Luego, ejecuta el siguiente comando para instalar las dependencias:

    ```sh
    pip install -r requirements.txt

7. **Ejecutar serverless offline**

   Para ejecutar el proyecto:

    ```sh
    serverless offline
    # En su defecto
    sls offline

    Esto genera en el ambiente offline

8. **Base de datos**

   Necesito un servidor de sql, podriamos Mostrar Xaamps, Una Maquina virtual como servidor ...:

    ```sh
    Ejecutar el script de la carpeta Db en archivo llamado web-scraping-db.sql

    Adjunte Modelo de base de datos.

**`URL APIS: http://localhost:3000/dev`**

## CONSULTAR INFORMACION POR CUFES

**`POST /v1/api/consult_invoice_information`**

Obtener informacion de acuerdo a cufe_id
o UUID
Argumento:

```json
{
    "cufes":[
        "e74aee1f02a03193b86ea8a0287af75a8f0443373b83e5b7fbbe173fd350da94ebf6f9f8376f78fe67401281d2f129f3",
        "b549735b1de829e79cb5b77d0ab77d51ee35aac72a866f6049d6e9c9365e343e955942469db55eeb1b8d7c12cf5a3880", "b549735b1de829e79cb5b77d0ab77d51ee35aac72a866f6049d6e9c9365e343e955942469db55eeb1b8d7c12cf5a3881"
    ]
}
```

Atributos:

**`cufes`**: (obligatorio) : Lista Cufes.

Respuesta Exitosa:

```json
{
    "status": 200,
    "message": "Operación exitosa.",
    "data": [
        {
            "e74aee1f02a03193b86ea8a0287af75a8f0443373b83e5b7fbbe173fd350da94ebf6f9f8376f78fe67401281d2f129f3": {
                "events": [
                    {
                        "eventNumber:": "030",
                        "eventName:": "Acuse de recibo de la Factura Electrónica de Venta"
                    },
                    {
                        "eventNumber:": "032",
                        "eventName:": "Recibo del bien o prestación del servicio"
                    }
                ],
                "sellerInformation": {
                    "Document": "901596817",
                    "Name": "COLOMBIA PLATAFORM SAS"
                },
                "receiverInformation": {
                    "Document": "800071617",
                    "Name": "CUMMINS DE LOS ANDES S.A"
                },
                "linkGraphicRepresentation": "https://catalogo-vpfe.dian.gov.co/User/SearchDocument/Document/DownloadPDF?trackId=e74aee1f02a03193b86ea8a0287af75a8f0443373b83e5b7fbbe173fd350da94ebf6f9f8376f78fe67401281d2f129f3&token=3659e76d124c1f3ce7600387694925ebed0ac8960e8d701dbe24b0a94157645f"
            }
        }
    ]
}
```

Respuesta de errores:

Data invalida

```json
{
    "status": 400,
    "message": "Verifique los datos de entrada e inténtelo nuevamente.",
    "data": []
}
```

Cufes Invalido

```json
{
    "status": 200,
    "message": "Operación exitosa.",
    "data": [
        {
            "CufeInvalidoIdAshs": "Cufe invalido."
        }
    ]
}
```

Cufes parametro enviado diferente a una lista

```json
{
    "status": 400,
    "message": "El valor 'cufes' debe ser una lista.",
    "data": []
}
```

Adjunto Url de Posmtan y Respositorio github

**URL POSTMAN [https://drive.google.com/drive/folders/1KehDE4oMtxcnvux8KUU0rLoS8_Rnv06G?usp=sharing]**

**URL GITHUB [https://github.com/anthonyeparra/WebScrapingTest]**
