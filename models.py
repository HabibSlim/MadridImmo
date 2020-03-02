""" Scraping models for multiple real estate websites """

from bs4 import BeautifulSoup, SoupStrainer

from shared import ScraperModel
from shared import make_entry, read_addr, gen_headers, list_pages, read_html


class PisosScraper(ScraperModel):
    def __init__(self):
        super().__init__()

        self._name = "pisos"

        self._url = "https://pisos.com"
        self._url_flats = self._url + "/en/venta/piso-madrid_capital/%d/"
        self._url_houses = self._url + "/en/venta/casas-madrid_capital/%d/"

        self._min_page_flats = 0
        self._max_page_flats = 99

        self._min_page_houses = 0
        self._max_page_houses = 21


    def parse_page(self, job):
        """Parse a page's HTML contents.
        Generate a list of entries from it.
        """

        # Unwrapping job
        url = job[0]
        proptype = job[1]

        # Reading HTML
        page = read_html(url, self._req)

        # Parsing content
        entries = []
        soup = BeautifulSoup(page, 'lxml',
                             parse_only=SoupStrainer('div', class_='row-to-hide'))

        # Iterating over all rows
        for row in soup.find_all(recursive=False):
            entry = make_entry(proptype)

            # Price
            price = row.select_one('div.price')
            price = price.text.strip().replace('.', '')
            if (price):
                entry['price'] = price[:-2]

            # Surface
            surf = row.select_one('div.characteristics')
            surf = surf.find_all(recursive=False)
            if (surf):
                entry['m2'] = surf[0].text.strip()[:-3]

            # URL
            url = row.find('meta', attrs={'itemprop':'url'})
            entry['url'] = self._url+url['content']

            # Localization
            loc = row.find('div', class_='location')
            loc = loc.text.strip().split(' (')
            entry['loc'] = loc[0]

            # Address
            addr = row.find('meta', attrs={'itemprop':'description'})
            entry['address'] = read_addr(addr['content'])

            entries += [entry]

        return entries


class HabitacliaScraper(ScraperModel):
    def __init__(self):
        super().__init__()

        self._name = "habitaclia"

        self._url = "https://english.habitaclia.com"
        self._url_flats = self._url + "/homes-madrid-%d.htm?ordenar=mas_recientes&st=1,4,9,11,13"
        self._url_houses = self._url + "/homes-madrid-%d.htm?ordenar=mas_recientes&st=3,6,8,10,12,15"

        self._min_page_flats = 0
        self._max_page_flats = 882

        self._min_page_houses = 0
        self._max_page_houses = 73

    def parse_page(self, job):
        """Parse a page's HTML contents.
        Generate a list of entries from it.
        """

        # Unwrapping job
        url = job[0]
        proptype = job[1]

        # Reading HTML
        page = read_html(url, self._req)

        # Parsing content
        entries = []
        soup = BeautifulSoup(page, 'lxml',
                             parse_only=SoupStrainer('article'))

        # Iterating over all rows
        it = iter(soup.find_all('article'))
        pairs = list(zip(it, it))
        for row,price in pairs[:-1]:
            entry = make_entry(proptype)

            # Price
            price = price.find('span')
            if (price):
                entry['price'] = price.text[:-2].replace('.', '')
            
            # Surface
            surf = row.select_one('p.list-item-feature')
            if (surf):
                entry['m2'] = surf.text.split('m2')[0][2:]

            # URL
            entry['url'] = "http:"+row['data-href'].split('?')[0]

            # Localization
            loc = row.select_one('p.list-item-location')
            entry['loc'] = loc.text[10:].split('\n')[0]

            entries += [entry]

        return entries


class TucasaScraper(ScraperModel):
    def __init__(self):
        super().__init__()

        self._name = "tucasa"

        self._url = "https://www.tucasa.com"
        self._url_flats = self._url + "/compra-venta/pisos-y-apartamentos/madrid/madrid-capital/?r=&idz=0028.0001.9999.0001&ord=&pgn=%d"
        self._url_houses = self._url + "/compra-venta/casas-y-chalets/madrid/madrid-capital/?r=&idz=0028.0001.9999.0001&ord=&pgn=%d"

        self._min_page_flats = 1
        self._max_page_flats = 1

        self._min_page_houses = 1
        self._max_page_houses = 1

    def parse_page(self, job):
        """Parse a page's HTML contents.
        Generate a list of entries from it.
        """

        # Unwrapping job
        url = job[0]
        proptype = job[1]

        # Reading HTML
        page = read_html(url, self._req)

        # Parsing content
        entries = []
        strainer = SoupStrainer('div', class_='contenedor-descripcion-inmueble')
        soup = BeautifulSoup(page, 'lxml', parse_only=strainer)

        # Iterating over all rows
        for row in soup.find_all(recursive=False):
            entry = make_entry(proptype)

            # Price
            price = row.select_one('span.precio-card')
            price = price.text.strip()
            if (price):
                entry['price'] = price[:-2].replace('.', '')

            # Surface
            surf = row.select_one('li.metros-cuadrados')
            if (surf):
                entry['m2'] = surf.text[:-3]

            # Localization
            loc = row.find('span', class_='titulo-inmueble')
            loc = loc.text.strip().split("Palacio, ")
            entry['loc'] = loc[-1]

            # Address
            addr = row.find('span', class_='calle-inmueble')
            if (len(addr)):
                entry['address'] = addr.text.lower()

            # URL
            # Since tucasa.com works as an aggregator,
            # we can only provide the page URL for this field.
            entry['url'] = job[0]

            entries += [entry]

        return entries
