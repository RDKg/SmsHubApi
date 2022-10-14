import requests
import json
import os

from .SmsHubExceptions import *

SmsHubDir = os.path.dirname(__file__) + "\\"
SmsHubDir_Source = SmsHubDir + "src\\"

class SmsHubApi():
    url = "https://smshub.org/stubs/handler_api.php?"
    
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def GetNumbersStatus(self, country: int = None, operator: str = None) -> dict:
        """
            Параметры:
            - apiKey - Ваш API-ключ, обеспечивающий доступ к оплаченным услугам. Обязательный параметр;
            - country - Страна номера, если не задано, то будет выбрана страна с прошлого номера. Необязательный параметр;
            - operator - Оператор номера, если не задано, то будет выбран прошлый. Необязательный параметр.
        """

        response = requests.get(url=self.url, params={
            "api_key": self.apiKey,
            "action": "getNumbersStatus",
            "country": country,
            "operator": operator
        })

        SmsHubApi.FindException(response.text)

        return response.json()
    
    def GetBalance(self) -> dict:
        """
            Параметры:
            - apiKey - Ваш API-ключ, обеспечивающий доступ к оплаченным услугам. Обязательный параметр.

            Возможные ошибки:
            - BAD_KEY - Неверный API-ключ;
            - ERROR_SQL - Ошибка SQL-сервера;
            - BAD_ACTION - Общее неправильное формирование запроса.
        """
        response = requests.get(url=self.url, params={
            "api_key": self.apiKey,
            "action": "getBalance"
        })
        responseData = response.text.split(":")

        SmsHubApi.FindException(responseData[0])

        return {
            "status": responseData[0],
            "balance": float(responseData[1])
        }

    def GetNumber(self, service: str, country: int = None, operator: str = None) -> dict:
        """
            Параметры:
            - apiKey - Ваш API-ключ, обеспечивающий доступ к оплаченным услугам. Обязательный параметр;
            - service - Сервис приобретаемого номера. Обязательный параметр;
            - operator - Сотовый оператор номер которого необходимо получить. Необязательный параметр;
            - country - Страна приобретаемого номера. Необязательный параметр.

            Возможные ошибки:
            - BAD_KEY - Неверный API-ключ;
            - ERROR_SQL - Ошибка SQL-сервера;
            - BAD_ACTION - Общее неправильное формирование запроса;
            - BAD_SERVICE - Некорректное нименование сервиса.

            Ответ сервера:
            - NO_NUMBERS - Нет номеров с заданными параметрами;
            - NO_BALANCE - Баланс ниже цены покупаемого номера;
            - WRONG_SERVICE - Не верный идентификатор сервиса;
            - ACCESS_NUMBER:ID:NUMBER - Получили номер, ID активации и сам номер.
        """
        
        response = requests.get(url=self.url, params={
            "api_key": self.apiKey,
            "action": "getNumber",
            "service": service,
            "operator": operator,
            "country": country
        })
        responseData = response.text.split(":")

        SmsHubApi.FindException(responseData[0])

        if len(responseData) == 1:
            for i in range(2):
                responseData.append(None)

        return {
            "status": responseData[0],
            "id": responseData[1],
            "number": responseData[2]
        }

    def SetStatus(self, ID: int, status: int) -> dict:
        """
            Параметры:
            - apiKey - Ваш API-ключ, обеспечивающий доступ к оплаченным услугам. Обязательный параметр;
            - ID - ID активации, полученный при покупке номера. Обязательный параметр;
            - status - Статус активации (1: СМС отправлено, 3: Повторная отправка СМС, 6: Активация завершена, 8: Отменить активацию). Обязательный параметр.

            Возможные ошибки:
            - BAD_KEY - Неверный API-ключ;
            - ERROR_SQL - Ошибка SQL-сервера;
            - BAD_ACTION - Общее неправильное формирование запроса;
            - BAD_SERVICE - Некорректное нименование сервиса;
            - NO_ACTIVATION - ID активации не существует.

            Ответ сервера:
            - ACCESS_READY - Готовность ожидания СМС;
            - ACCESS_RETRY_GET - Ожидаем новое СМС;
            - ACCESS_ACTIVATION - Активация успешно завершена;
            - ACCESS_CANCEL - Активация отменена.
        """

        response = requests.get(url=self.url, params={
            "api_key": self.apiKey,
            "action": "setStatus",
            "status": status,
            "id": ID
        })
        responseData = response.text.split(":")

        SmsHubApi.FindException(responseData[0])

        return {
            "status": responseData[0]
        }

    def GetStatus(self, ID: int) -> dict:
        """
            Параметры:
            - apiKey - Ваш API-ключ, обеспечивающий доступ к оплаченным услугам. Обязательный параметр;
            - ID - ID активации, полученный при покупке номера. Обязательный параметр;

            Возможные ошибки:
            - BAD_KEY - Неверный API-ключ;
            - ERROR_SQL - Ошибка SQL-сервера;
            - BAD_ACTION - Общее неправильное формирование запроса;
            - NO_ACTIVATION - ID активации не существует.

            Ответ сервера:
            - STATUS_WAIT_CODE - Ожидаем прихода смс;
            - STATUS_WAIT_RETRY:LASTCODE - Ожидаем еще одно смс (LASTCODE - последнее полученное смс);
            - STATUS_CANCEL - Активация отменена;
            - STATUS_OK:CODE - Код получен (CODE - код активации).
        """

        response = requests.get(url=self.url, params={
            "api_key": self.apiKey,
            "action": "getStatus",
            "id": ID
        })
        responseData = response.text.split(":")

        SmsHubApi.FindException(responseData[0])

        if len(responseData) == 1:
            responseData.append(None)

        return {
            "status": responseData[0],
            "code": responseData[1]
        }

    def GetPrices(self, service: str = None, country: int = None) -> dict:
        """
            Параметры:
            - apiKey - Ваш API-ключ, обеспечивающий доступ к оплаченным услугам. Обязательный параметр;
            - service - Сервис приобретаемого номера. Необязательный параметр;
            - country - Страна номера. Необязательный параметр;
        """

        response = requests.get(url=self.url, params={
            "api_key": self.apiKey,
            "action": "getPrices",
            "service": service,
            "country": country
        })

        SmsHubApi.FindException(response.text)

        return response.json()

    def SetMaxPrice(self, maxPrice: float, service: str, country: int, random: bool = False) -> int:
        """
            Параметры:
            - apiKey - Ваш API-ключ, обеспечивающий доступ к оплаченным услугам. Обязательный параметр;
            - maxPrice - Максимальная цена для покупки номера;
            - service - Сервис приобретаемого номера. Необязательный параметр;
            - country - Страна номера. Обязательный параметр;
            - random - Выдавать случайный номер в рамках указанной цены (True), или сначала самые дешевые (False).
        """

        response = requests.get(url=self.url, params={
            "api_key": self.apiKey,
            "action": "setMaxPrice",
            "maxPrice": maxPrice,
            "service": service,
            "country": country,
            "random": random
        })

        SmsHubApi.FindException(response.text)

        return response.status_code

    @staticmethod 
    def GetListOfCountriesAndOperators() -> dict:
        with open(f"{SmsHubDir_Source}ListOfCountriesAndOperators.json", "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod 
    def GetCountryIdByName(country: str = "россия") -> str:
        """
            Параметры:
            - country - Название страны на латинице или кириллице;
        """

        listOfCountriesAndOperators = SmsHubApi.GetListOfCountriesAndOperators()
        country = country.lower().replace(" ", "")

        keyFinder = "name"
        if ord(country[0]) >= 97 and ord(country[0]) <= 122:
            keyFinder = "country"

        for key in listOfCountriesAndOperators:
            if listOfCountriesAndOperators[key][keyFinder] == country:
                return key
    
    @staticmethod 
    def GetListOfServices() -> dict:
        with open(f"{SmsHubDir_Source}ListOfServices.json", "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def FindException(value):
        if "BAD_KEY" in value:
            raise BAD_KEY("Неверный API-ключ.")
        elif "ERROR_SQL" in value:
            raise ERROR_SQL("Ошибка SQL-сервера.")
        elif "BAD_ACTION" in value:
            raise BAD_ACTION("Общее неправильное формирование запроса.")
        elif "BAD_SERVICE" in value:
            raise BAD_SERVICE("Некорректное наименование сервиса.")
        elif "NO_ACTIVATION" in value:
            raise NO_ACTIVATION("ID активации не существует.")
