# Importation des librairies standards
import scrapy


# Création d'une classe donnant les méthodes et attributs de notre webscrapping
class VintedScraper(scrapy.Spider):
    url: str
    name = 'vintedgame'
    # On précise le lien à scrapper
    base_url = "https://www.vinted.fr/vetements?search_text=nike&time=1676444406&page={offset}"

    def start_requests(self):
        # On installe un user-agent pour essayer de pouvoir scrapper librement
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.82 Safari/537.36'}
        # Gestion des erreurs de redirections
        meta = {'dont_redirect': True, 'handle_httpstatus_list': [302], 'exception': False}

        # On itère sur chaque page de notre url
        for offset in range(1, 1, 25):
            url = self.base_url.format(offset=offset)
            yield scrapy.Request(url=url, headers=headers, meta=meta, callback=self.parse)

    # Création de la fonction parse qui va aller extraire des elements du site booking.com de la page de resultat
    def parse(self, response):
        annonces = response.xpath(".//div[@class='web_ui__ItemBox__box']")
        # Création d'un dictionnaire qui va contenir les informations de chaque hotel
        vinted_data = {}
        # On recupere les informations relatives à chaque hôtel present sur la page principale
        for annonce in annonces:
            vinted_data['id_product'] = annonce.xpath("")
            #vinted_data['nom'] = annonce.xpath(
            #    ".//div[@class='web_ui__Text__text web_ui__Text__caption web_ui__Text__left'][@data-testid='product-item-id-{}}--owner-name']/text()".format(vinted_data['id_product'])).get()
            #vinted_data['type_hebergement'] = annonce.xpath(".//span[@class='df597226dd']/text()").get()
            #vinted_data['emplacement'] = annonce.xpath(
                #".//span[@class='f4bd0794db b4273d69aa'][@data-testid='address']/text()").get()
            #vinted_data['accessibilite'] = annonce.xpath(
                #".//span[@class='f4bd0794db']/span/span[@data-testid='distance']/text()").get()
            #vinted_data['nb_etoiles'] = annonce.xpath(".//div[@class='e4755bbd60']/@aria-label").get()
            #vinted_data['note'] = annonce.xpath(".//div[@class='b5cd09854e d10a6220b4']/text()").get()
            #vinted_data['prix'] = annonce.xpath(".//span[@class='fcab3ed991 fbd1d3018c e729ed5ab6']/text()").get()
            #vinted_data['breakfast_inclus'] = annonce.xpath(".//span[@class='e05969d63d']/text()").get()
            #vinted_data['annulation_gratuite'] = annonce.xpath(".//div[@class='d506630cf3']//text()").get()
            #vinted_data['lien'] = annonce.xpath(".//a[@class='e13098a59f']/@href").get()

            # On récupère les liens de chaque hôtels afin de les parcourir et y extraire des informations
            #current_hotel_page = annonce.xpath(".//a[@class='e13098a59f']/@href").get()
            #yield scrapy.Request(current_hotel_page, self.parse_hotel, meta={'hotel_data': dict(hotel_data)})

    # # On va récupérer des éléments spécifiques à chaque hôtel sur leurs pages respectives
    def parse_annonce(self, response):
        hotel_data = response.meta.get('hotel_data')
        hotel_data['adresse'] = response.xpath('.//*[@id="showMap2"]/span[1]/text()').get()
        hotel_data['description'] = response.xpath('.//*[@id="property_description_content"]').get()
        hotel_data['long_lat'] = response.xpath('.//*[@id="hotel_address"]').get()
        # On récupère l'ensemble des informations de chaque hôtel dans le dictionnaire hotel_data
        yield hotel_data