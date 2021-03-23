import requests
import logging
import json
import logging
from   random import choice

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

IMAGE_URL    = "https://image.webmotors.com.br/_fotos/AnuncioUsados/gigante/"
USERS_AGENTS = [
    'Mozilla/5.0 (Linux; Android 5.0.2; VK810 4G Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.76.4 (KHTML, like Gecko) Version/7.0.4 Safari/537.76.4',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; SMJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MDDCJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; BOIE9;ENUS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/6.0.51363 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2503.0 Safari/537.36',
]

class Webmotors(object):
    def __init__(self,proxy=None,vehiclePerPage=100):
        self.__proxy          = proxy
        self.__carsPageNum    = 1
        self.__bikePageNum    = 1
        self.__vehiclePerPage = vehiclePerPage
        self.__session        = requests.Session()

    @property
    def proxy(self):
        return self.__proxy

    @proxy.setter
    def proxy(self,value):
        try:
            ip    = requests.get("https://ifconfig.me/ip")
            proxy = {
                "http":value,
                "https":value
            }        
            newIp = requests.get("https://ifconfig.me/ip",proxies=proxy)
            if ip != newIp:
                self.__proxy           = value
                self.__session.proxies = proxy
                logger.info(f"Proxy configurado: {ip}")
            else:
                logger.warn(f"Nao foi possivel configurar o proxy")
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")

    def getCars(self):
        try:
            url      = f"https://www.webmotors.com.br:443/api/search/car?url=https://www.webmotors.com.br/carros%2Festoque%3F&actualPage={self.__carsPageNum}&displayPerPage={self.__vehiclePerPage}&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false"
            cookies  = {"AMCV_3ADD33055666F1A47F000101%40AdobeOrg": "-1124106680%7CMCIDTS%7C18705%7CMCMID%7C08361442210490129111811084005471184982%7CMCOPTOUT-1616107905s%7CNONE%7CvVersion%7C5.2.0", "mbox": "session#778ba20bffd6441b84a07f970ef4bfdb#1616102564", "at_check": "true", "WebMotorsVisitor": "1", "AMCVS_3ADD33055666F1A47F000101%40AdobeOrg": "1", "WMLastFilterSearch": "%7B%22car%22%3A%22carros%2Festoque%3Fidcmpint%3Dt1%3Ac17%3Am07%3Awebmotors%3Abusca%3A%3Averofertas%22%2C%22bike%22%3A%22motos%2Festoque%22%2C%22estadocidade%22%3A%22estoque%22%2C%22lastType%22%3A%22car%22%2C%22cookie%22%3A%22v3%22%2C%22ano%22%3A%7B%7D%2C%22preco%22%3A%7B%7D%2C%22marca%22%3A%22%22%2C%22modelo%22%3A%22%22%7D", "WebMotorsSearchDataLayer": f"%7B%22search%22%3A%7B%22location%22%3A%7B%7D%2C%22ordination%22%3A%7B%22name%22%3A%22Mais%20relevantes%22%2C%22id%22%3A1%7D%2C%22pageNumber%2{self.__carsPageNum}%3A2%2C%22totalResults%22%3A262926%2C%22vehicle%22%3A%7B%22type%22%3A%7B%22id%22%3A1%2C%22name%22%3A%22carro%22%7D%7D%2C%22cardExhibition%22%3A%7B%22id%22%3A%221%22%2C%22name%22%3A%22Cards%20Grid%22%7D%2C%22eventType%22%3A%22paginacaoRealizada%22%7D%7D", "WebMotorsTrackingFrom": "paginacaoRealizada"}
            headers  = {"GET /api/search/car?url=https": f"/www.webmotors.com.br/carros%2Festoque%3F&actualPage={self.__carsPageNum}&displayPerPage={self.__vehiclePerPage}&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false HTTP/1.1", "User-Agent": choice(USERS_AGENTS), "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Sec-GPC": "1"}
            response = self.__session.get(url,headers=headers,cookies=cookies)
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return []

        if response.status_code == 200:
            results = json.loads(response.text)
            if len(results["SearchResults"]) == 0:
                self.__carsPageNum = 1
                return []
            else:
                self.__carsPageNum += 1
                return results["SearchResults"]

    def getBikes(self):
        try:
            url      = f"https://www.webmotors.com.br:443/api/search/bike?url=https://www.webmotors.com.br/motos%2Festoque%3Ftipoveiculo%3Dmotos&actualPage={self.__bikePageNum}&displayPerPage={self.__vehiclePerPage}&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false"
            cookies  = {"AMCV_3ADD33055666F1A47F000101%40AdobeOrg": "359503849%7CMCIDTS%7C18602%7CMCMID%7C56241706435647372388498402368390428709%7CMCOPTOUT-1607182934s%7CNONE%7CvVersion%7C5.0.1", "AMCV_3ADD33055666F1A47F000101%40AdobeOrg": "-1124106680%7CMCIDTS%7C18704%7CMCMID%7C56241706435647372388498402368390428709%7CMCOPTOUT-1615992864s%7CNONE%7CvVersion%7C5.2.0", "WebMotorsLastSearches": "%5B%7B%22route%22%3A%22carros%2Festoque%2Fvolkswagen%2Fjetta%22%2C%22query%22%3A%22%22%7D%5D", "mbox": "session#95f94e1177ac42908ac4fb1aaac3a342#1615986642", "at_check": "true", "AMCVS_3ADD33055666F1A47F000101%40AdobeOrg": "1", "WebMotorsVisitor": "1", "WMLastFilterSearch": "%7B%22car%22%3A%22carros%2Festoque%3Fidcmpint%3Dt1%3Ac17%3Am07%3Awebmotors%3Abusca%3A%3Averofertas%22%2C%22bike%22%3A%22motos%2Festoque%22%2C%22estadocidade%22%3A%22estoque%22%2C%22lastType%22%3A%22car%22%2C%22cookie%22%3A%22v3%22%2C%22ano%22%3A%7B%7D%2C%22preco%22%3A%7B%7D%2C%22marca%22%3A%22%22%2C%22modelo%22%3A%22%22%7D", "WebMotorsSearchDataLayer": "%7B%22search%22%3A%7B%22location%22%3A%7B%7D%2C%22ordination%22%3A%7B%22name%22%3A%22Mais%20relevantes%22%2C%22id%22%3A1%7D%2C%22pageNumber%22%3A1%2C%22totalResults%22%3A258704%2C%22vehicle%22%3A%7B%22type%22%3A%7B%22id%22%3A1%2C%22name%22%3A%22carro%22%7D%7D%2C%22cardExhibition%22%3A%7B%22id%22%3A%221%22%2C%22name%22%3A%22Cards%20Grid%22%7D%2C%22eventType%22%3A%22buscaRealizada%22%7D%7D", "WebMotorsTrackingFrom": "filtroRealizado"}
            headers  = {"GET /api/search/bike?url=https": f"/www.webmotors.com.br/motos%2Festoque%3Ftipoveiculo%3Dmotos&actualPage={self.__bikePageNum}&displayPerPage={self.__vehiclePerPage}&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false HTTP/1.1", "User-Agent": choice(USERS_AGENTS), "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Sec-GPC": "1"}
            response = self.__session.get(url,headers=headers,cookies=cookies)
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return []
            
        if response.status_code == 200:
            results = json.loads(response.text)
            if len(results["SearchResults"]) == 0:
                self.__bikePageNum = 1
                return []
            else:
                self.__bikePageNum += 1
                return results["SearchResults"]
