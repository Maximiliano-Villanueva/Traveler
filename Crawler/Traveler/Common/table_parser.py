from bs4 import BeautifulSoup
from typing import List
import requests
import lxml

class AirportParse:

    def __init__(self):
        pass

    def _getUrlHtml(self, url : str, method : str, post_data = []) -> str:
        """
        get data from url and return the html content
        """
        html_data = None

        if method.lower() == 'post':
            html_data = requests.post(url = url, data = post_data)

        else:
            html_data = requests.post(url = url)

        return html_data

    def parseUrl(self, url : str, method : str = 'get' , post_data = []) -> List[str]:
        """
        parse tables in url and return a list of airports
        """
        if url is None or not isinstance(url,str) or len(url)<1:
            raise Exception('url : {] is not valid'.format(url))

        data = self._getUrlHtml(url, method).text

        #if data.status_code 
        table_content = []

        #make sure data is not empty
        if data is not None:
            
            content = data

            try:
                #avoid unexpected errors trying to parse the html data
                soup = BeautifulSoup(data, 'lxml')

                #find the tables
                airports = soup.select("ul.airport-list.country-airports")

                if len(airports) < 1 :
                    raise Exception("No airports found in url {}".format(url))

                #parse airports
                for air in airports:

                    name = air.getText()
                    table_content.append(name)
                        
                #check url for airports
                #https://www.flightconnections.com/airports-by-country
            except Exception as e:
                raise Exception('error parsing content from url {0} with error: {1}'.format(url, str(e)))

        return table_content

            


            
        


        