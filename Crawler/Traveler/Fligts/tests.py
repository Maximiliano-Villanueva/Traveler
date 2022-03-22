#simpletestcase avoids creating a test database while testcase does
from django.test import TestCase, SimpleTestCase
from Common.Proxy_broker import PBroker
from Common.table_parser import AirportParse

# Create your tests here.
# python manage.py test
class PBrokerTest(SimpleTestCase):

    def setUp(self):
        pass
    
    def atest_get_proxies(self):
        self.proxies = False
        async def store_proxies(proxies):
            
            proxy = await proxies.get()
            self.proxies = dict()
            while proxy is not None:
                
                proxy = await proxies.get()
                print(proxy)

                if proxy is None:
                    continue
                country_code = proxy.geo.code

                if country_code not in self.proxies.keys():
                    self.proxies[country_code] = []
                
                self.proxies[country_code].append(proxy.as_json())


        PBroker.main(countries=['IN'], types = ['SOCKS5'], limit=3, callback = store_proxies)

        max_sec = 60
        while not self.proxies and max_sec > 0:
            sleep(1)
            max_sec -= 1
        
        self.assertGreater(len(self.proxies),0)


class CommonTests(SimpleTestCase):

    def setUp(self):
        self.parser = AirportParse()
        pass

    def test_url_parse(self):
        """
        test passing a regular url
        """

        url = 'https://www.flightconnections.com/airports-in-aruba-aw'

        air_list = self.parser.parseUrl(url = url, method = 'get')

        self.assertGreater(len(air_list), 0)

    def test_url_parse_wrong_url(self):
        """
        test parsing a wrong url
        """
        url = 'https://www.flightconnections.com/airports-in-aruba-aw2'

        self.assertRaises(Exception, self.parser.parseUrl, url = url, method = 'get')
    

        