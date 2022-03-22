"""Gather proxies from the providers without
   checking and save them to a file."""

import asyncio
from proxybroker import Broker

import requests
import random

import aiohttp
from proxybroker.resolver import Resolver
from proxybroker.utils import log


class ResolverCustom(Resolver):
    _temp_host = []

    def _pop_random_ip_host(self):

        host = random.choice(self._temp_host)
        self._temp_host.remove(host)
        return host

    async def get_real_ext_ip(self):
        self._temp_host = self._ip_hosts.copy()
        while self._temp_host:
            try:
                timeout = aiohttp.ClientTimeout(total=self._timeout)
                async with aiohttp.ClientSession(
                        timeout=timeout, loop=self._loop
                ) as session, session.get(self._pop_random_ip_host()) as resp:
                    ip = await resp.text()
            except asyncio.TimeoutError:
                pass
            else:
                ip = ip.strip()
                if self.host_is_ip(ip):
                    log.debug('Real external IP: %s', ip)
                    break
        else:
            raise RuntimeError('Could not get the external IP')
        return ip





class PBroker:

    def __init__(self):
        pass

    @staticmethod
    async def save(proxies):
        """Save proxies to a file."""

        #proxy_list = kargs['proxy_list']

        while True:
            proxy = await proxies.get()
            if proxy is None:
                break

            country_code = proxy.geo.code

            """
            if country_code not in proxy_list.keys():
                proxy_list[country_code] = []
            
            proxy_list[country_code].append(proxy.as_json())
            """
            print(proxy.as_json())

    @staticmethod
    def main(countries=['US'], types = ['SOCKS5'], limit=3, callback = save.__func__):
        """
        find n number of proxies
        
        Parameters:
            countries -> list of cuntry codes
            types -> list of web protocols : [HTTP, HTTPS, SOCKS4, SOCKS5, CONNECT:80, CONNECT:25]
            limit -> max number of proxies per country
            callback -> async function to call to this function receives proxies as first parameter and the others must be passed as **kargs
        """
        #define variables
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        

        tasks = asyncio.gather(
            broker.find(countries=countries, types = types, limit= limit),
            callback(proxies),
        )
        loop = asyncio.get_event_loop()
        broker._resolver = ResolverCustom(loop=loop)
        loop.run_until_complete(tasks)


if __name__ == '__main__':
    PBroker.main()

