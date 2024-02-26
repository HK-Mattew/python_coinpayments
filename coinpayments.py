from urllib.parse import urlencode
import requests, hmac, hashlib



class CoinPayments():
    def __init__(self, public_key: str, private_key: str, version: int=1):
        self.__PUBLIC_KEY = public_key
        self.__PRIVATE_KEY = private_key
        self.__VERSION = version
        self.__BASE_ENDPOINT = 'https://www.coinpayments.net/api.php'
        self.__SESSION = requests.Session()
        
        self._GEN_HMAC = (
            lambda data: (
                hmac.new(bytearray(self.__PRIVATE_KEY, 'UTF-8'),
                urlencode(data).encode('UTF-8'), hashlib.sha512).hexdigest()
                )
            )


    def __request_api(self, data, method):
        data.update({
            'cmd': data.get('cmd'),
            'key': self.__PUBLIC_KEY,
            'version': self.__VERSION,
            'format': 'json'
            })
        _response_api = getattr(self.__SESSION, method.lower())(
            url=self.__BASE_ENDPOINT,
            data=data,
            headers={'hmac': self._GEN_HMAC(data)}
            )
        return _response_api.json()

    
    def coinpayments(self, data: dict, method: str='POST'):
        return self.__request_api(data, method)
    

        