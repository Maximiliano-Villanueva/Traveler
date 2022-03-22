import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Traveler.settings")
#os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "Traveler.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from Fligts.models import Country, Airport, ProxyServer
import pycountry
from asgiref.sync import sync_to_async
from Common.Proxy_broker import PBroker
from Common.table_parser import AirportParse
import logging
import time

class DataLoader():
    """
    populate static tables
    """

    def __init__(self):
        """
        basic constructor
        params
            proxies : list<Proxy> -> list of found proxies
            running : bool-> indicates if thread is running so the main thread can await to bulk load the data in the database
        """
        self.proxies = []
        self.running = False
    
    def loadProxies(self, country : str, types = ['SOCKS5'], limit : int=3):
        """
        load proxies matching the specified characteristics
        params:
            country : str -> country to find proxy for
            types -> List<str> -> list of protocols to retrieve
            limit : int -> max number of proxies to retrieve
        """

        if not isinstance(types, list):
            raise Exception('types parameter is invalid')
        if limit < 1:
            raise Exception('limit parameter must be >= 0')

        #define function to handle async queues
        async def store_proxies(proxies):
            """
            store proxies in self.proxies
            """
            self.running = True

            #iterate each found proxy                        
            proxy = await proxies.get()

            #populate self.proxies list with found proxies
            while proxy is not None:
                #print(proxy)    
                proxy = await proxies.get()

                #ignore empty cases
                if proxy is None:
                    continue
            
                try:
                    self.proxies.append(proxy)
                    logging.info('adding proxy : {} to list of proxies'.format(str(proxy)))

                except Exception as e:
                    #make sure to avoid unwanted waitings
                    self.running = False
                    logging.error(str(e))

            self.running = False

        logging.info('calling proxy borker for cuntry {}'.format(country))

        PBroker.main(countries=[country], types = types, limit= limit, callback = store_proxies)

        elapsed_seconds = 0

        logging.info('about to enter waiting loop')
        #wait for thread to finish with a 30 secs timeout
        while self.running and elapsed_seconds < 30:
            logging.info('waiting 1 second')
            time.sleep(1)
            elapsed_seconds+=1

        logging.info('thread finished, starting to manage the list of proxies. number of elements : %d'.format(len(self.proxies)))
        #insert each proxy in db
        while len(self.proxies) > 0:
            proxy = self.proxies.pop()
            print(proxy)
            #get relevant info from proxy
            country_code = proxy.geo.code
            host = proxy.host
            port = proxy.port
            
            #create objects
            countr = Country.objects.get(code=country_code)
            logging.info('trying to get code from {}'.format(country_code))
            
            logging.info('retrieved {}'.format(str(countr)))
            created_object, created = ProxyServer.objects.get_or_create(host=str(host), port=int(port), country = countr)
                    
    def loadCountries(self, load_proxies : bool): 
        """
        load countries to database

        params:
            load_proxies : bool -> indicates if proxy loading should be done simultaneously
        """
        countries = list(pycountry.countries)

        for country in countries:
            
            created_object, created = Country.objects.get_or_create(name = country.name, code = country.alpha_2, code_2 = country.alpha_3)
            print('object : {obj}, created : {created}'.format(**{'obj' : str(country.alpha_2), 'created' : str(created)}))

            if created and load_proxies:
                self.loadProxies(country = country.alpha_2, types = ['SOCKS5'], limit = 3)
                logging.info('inserted country {}'.format(country.name))

            else:
                logging.info('ignoring country {}'.format(country.name))

    def loadAirports(self):
        #https://www.flightconnections.com/airports-in-aruba-aw
        
        #define common variables
        BASE_URL = 'https://www.flightconnections.com/airports-in-{name}-{code}'
        parser = AirportParse()

        #load all country objects
        countries = Country.objects.all()

        #use iterator for memory optimization
        for country in countries:

            #format the url to be parsed
            url = BASE_URL.format(**{'name' : country.name, 'code' : country.code})

            try:
                #invoke parser
                airports = parser.parseUrl(url = url, method = 'get')

                for air in airports:
                    created_object, created = Airport.objects.get_or_create(name = air, country = country)

            except Exception as e:
                pass



            

if __name__ == '__main__':

    dl = DataLoader()
    #dl.loadCountries(load_proxies=True)
    dl.loadAirports()
    

    #dl.loadProxies(country = 'US', types = ['SOCKS5'], limit = 3)
    #dl.loadProxies(country = 'IN', types = ['SOCKS5'], limit = 3)
    #dl.loadProxies(country = 'GB', types = ['SOCKS5'], limit = 3)
