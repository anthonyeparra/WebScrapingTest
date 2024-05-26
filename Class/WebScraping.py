from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from Helpers.basic_helper import dict_data
from os import environ
from Models.ProcessSQL import ProcessSQL 

SELLER_INFORMATION = "DATOS DEL EMISOR"
RECEIVER_INFORMATION = "DATOS DEL RECEPTOR"
MESSAGE_INVALIDATE = "Ingrese el código CUFE o UUID"
CUFE_INVALIDATE = {"InputValue": "Cufe invalido."}
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
CONTENT_TYPE = "application/x-www-form-urlencoded"
HEADERS = {"User-Agent": AGENT, "Content-Type": CONTENT_TYPE}

class WebScraping():
    def __init__(self):
        self.url_dian = environ.get('URL_DIAN')
        self.script_path = environ.get('SCRIPT_PATH')
        self.recaptcha_site_key = environ.get('RECAPTCHA_SITE_KEY')

    def get_information_cufe(self, data: dict):
        """
        Retrieves information about a list of CUFE codes using a
        web scraping technique.

        Args:
            data (dict): A dictionary containing a list of CUFE codes under
            the key 'cufes'.

        Returns:
            list: A list of dictionaries,
            each containing the extracted information for a CUFE code.
    
        Raises:
            Warning: If there is an error obtaining the reCAPTCHA token or the form token.
        """
        
        driver = webdriver.Chrome(ChromeDriverManager().install())
        try:
            if not isinstance(data['cufes'], list):
                raise Warning(
                    "El valor 'cufes' debe ser una lista."
                )
            array_data = [] 
            for dato_ in data['cufes']:

                driver.get(self.url_dian)
                
                recaptcha_token = self.get_recaptcha_token(driver)

                form_token = self.get_token_forms(driver)
                
                if not recaptcha_token or not form_token:
                    raise Warning(
                        "No se pudieron obtener todos los tokens necesarios."
                    )

                data = dict_data(form_token, recaptcha_token, dato_)
                array_data.append(self.request_get_informations(data, driver))
            return array_data
        except TimeoutError as te:
            raise Warning(te)
        except Exception as e:
            raise Warning(e)
        finally:
            driver.quit()
    def extract_data(self, html):
        """
        Extracts data from an HTML document using BeautifulSoup.

        Args:
            html (str): The HTML document to extract data from.

        Returns:
            dict: A dictionary containing the extracted data. 
            The dictionary has the following structure:
                {
                    'cufe_value': {
                        'events': [
                            {
                                'eventNumber:': code,
                                'eventName:': description
                            },
                            ...
                        ],
                        'sellerInformation': {
                            'Document': seller_nit,
                            'Name': seller_name
                        },
                        'receiverInformation': {
                            'Document': receiver_nit,
                            'Name': receiver_name
                        },
                        'linkGraphicRepresentation': pdf_link
                    }
                }
        """
        soup = BeautifulSoup(html, 'html.parser')

        input_element = soup.find('input', {'id': 'DocumentKey'})
        events = []
     
        # Cuando event sea vacio
        if not input_element :
            pass
        elif (input_element.get('placeholder') == MESSAGE_INVALIDATE):
            events.append(CUFE_INVALIDATE)

        # Extrae el valor de CUFE
        cufe_value = soup.find('span', class_='cufe-text').text.strip().split('\n')[-1].strip()

        seller_nit, seller_name = self.generic_data_extraction(
            SELLER_INFORMATION, soup
        )
        receiver_nit, receiver_name = self.generic_data_extraction(
            RECEIVER_INFORMATION, soup
        )
        # enlace del PDF
        pdf_link = soup.find('a', class_='downloadPDFUrl')['href']
        pdf_link = self.url_dian + pdf_link

        # Div especifico para recorrer los eventos
        container = soup.find('div', id='container1')
        tbody = container.find('tbody')

        # Extrar las filas de la tabla
        if tbody:
            for tr in tbody.find_all('tr'):
                code = tr.find_all('td')[0].text.strip()
                description = tr.find_all('td')[1].text.strip()
                events.append(
                    {
                        'eventNumber:': code,
                        'eventName:': description
                    }
                )
        # retorno estructura solicitada
        structure_data = {
            f'{cufe_value}': {
                'events': events,
                'sellerInformation': {
                    'Document': seller_nit,
                    'Name': seller_name
                },
                'receiverInformation': {
                    'Document': receiver_nit,
                    'Name': receiver_name
                },
                'linkGraphicRepresentation': pdf_link
                }
        }
        process_sql = ProcessSQL()
        process_sql.create_informations_cufes(cufe_value, structure_data)
        return structure_data

    def get_recaptcha_token(self, driver):
        """
        Retrieves the reCAPTCHA token from the specified driver.

        Args:
            driver (WebDriver): The driver object used to interact 
            with the web page.

        Returns:
            str or None: The reCAPTCHA token, or None if it cannot be obtained.

        Raises:
            Warning: If there is an error obtaining the reCAPTCHA token.
        """
        recaptcha_token = None
        try:
            script = self.get_recaptcha_script()
            recaptcha_token = driver.execute_script(script)

        except Exception as e:
            raise Warning("Error al obtener el token de reCAPTCHA:",e)
        return recaptcha_token

    def get_token_forms(self, driver):
        """
        Retrieves the value of the form token from the specified driver.

        Args:
            driver (WebDriver): The driver object used to interact with
            the web page.

        Returns:
            str: The value of the form token, or None if it cannot be found.

        Raises:
            Warning: If there is an error obtaining the form token.
        """
        form_token = None
        try:
            form_token_element = driver.find_element(
                By.NAME, "__RequestVerificationToken"
            )
            form_token = form_token_element.get_attribute("value")
        except Exception as e:
            raise Warning("Error al obtener el token del formulario:", e)
        return form_token
    
    def request_get_informations(self, data: dict, driver):
        """
        Sends a POST request to the specified URL with the given data and 
        cookies from the driver.
        If the response status code is 200, it extracts the data using 
        the `extract_data` method.
        If the extraction is successful, it returns the extracted data.
        Otherwise, it returns a dictionary with the value of `InputValue` 
        from `CUFE_INVALIDATE` for the key `DocumentKey` from the input data.
        
        Args:
            data (dict): A dictionary containing the data to be sent 
            in the request.
            driver (WebDriver): The driver object used to get the cookies.
        
        Returns:
            Union[list, dict]: The extracted data if successful,
            or a dictionary with the value of `InputValue`
            for the key `DocumentKey` from the input data.
        
        Raises:
            Warning: If there is an error obtaining the data.
        """
        try:
            # Convierte el diccionario en una cadena de consulta
            data_str = '&'.join([f"{key}={value}" for key, value in data.items()])

            session = requests.Session()
            cookies = driver.get_cookies()
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])

            response = session.post(self.url_dian, headers=HEADERS, data=data_str)
            if response.status_code == 200:
                datos_extraidos = []
                try:
                    datos_extraidos = self.extract_data(response.text)
                    return datos_extraidos
                except AttributeError as e:
                    return {data['DocumentKey']: CUFE_INVALIDATE['InputValue']}
            else:
                    return {data['DocumentKey']: CUFE_INVALIDATE['InputValue']}

        except Exception as e:
            raise Warning("Error al obtener los datos:", e)
            
    def generic_data_extraction(self, name_class, soup):
        """
        Extracts the NIT and name of the emitter from a given HTML soup object.

        Parameters:
            name_class (str): The name class to search for in the HTML soup.
            soup (BeautifulSoup): The HTML soup object to extract data from.

        Returns:
            tuple: A tuple containing the NIT (National Identification Number) 
            and name of the emitter.
        """
        generic_div = soup.find(
            'span', class_='datos-receptor',
            string=name_class
        ).find_parent('div', class_='col-md-4')

        # Extraer el texto dentro del div del emisor y dividirlo por líneas
        generic_text = generic_div.text.strip().split('\n')
        
        # Encontrar línea que contiene el NIT del emisor y extraer su valor
        nit_line = [linea for linea in generic_text if 'NIT' in linea][0]
        generic_nit = nit_line.split(':')[1].strip()

        # Encontrar línea que contiene el nombre del emisor y extraer su valor
        name_line = [linea for linea in generic_text if 'Nombre' in linea][0]
        generic_name = name_line.split(':')[1].strip()

        return generic_nit, generic_name
    
    def get_recaptcha_script(self):
        with open(self.script_path, 'r') as file:
            script = file.read()
        return script.replace('{{RECAPTCHA_SITE_KEY}}', self.recaptcha_site_key)