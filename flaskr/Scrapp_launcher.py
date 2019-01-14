

#import des codes de scrapp

from threading import Thread
import schedule

class Scrapper(Thread):
    """Class that launches the scrapping process regularly, with comparisons and database updates"""

    def __init__(self, mongo):
        """Constructor, mongo is the mongodb object"""
        Thread.__init__(self)
        self.__mongo = mongo
        self.__scrap_log = open("log/scrap.log")

    def __del__(self):
        """Destructor"""
        self.__scrap_log.close()

    def start(self):
        """Launches the scrapping process regularly. Must be called at server startup"""

        self.__scrapp_all()

        schedule.every().day.at("00:00").do(self.__scrapp_all)

    def __scrapp_all(self):
        """Scrapps all the sites, must be called once a day"""

        self.__scrap_log.write("Launching scrapper\n")

        sites = ["machin", "truc"] # The list of sites to be scrapped

        for site in sites:
            #n_uplets, liens = la commande pour scrapper ce site. Doit renvoyer une liste de n_uplets et la liste des liens correspondants
            n_uplets, links = [[5000,45,40,"F5",5,1,"Cette annonce est très belle","Une belle annonce","static/TestFrontImages/test_image_1.jpg"]], [["http://www.google.fr"]]

            for k in range(len(n_uplets)):
                n_uplet = n_uplets[k]
                link = links[k]

                #Comparisons
                similar = []
                #Là il faut remplir "similar" avec les annonces similaires à l'annonce en cours de traitement

                database_entry = {
                    "title": n_uplet[7],
                    "link": link,
                    "surface": n_uplet[2],
                    "rooms": n_uplet[4],
                    "location": "Arrondissement : " + str(n_uplet[5]),
                    "price": n_uplet[0],
                    "agency": site,
                    "text": n_uplet[6],
                    "image": n_uplet[8],
                    "similar": similar
                }
                self.__mongo.db.ads.insert_one(database_entry)
                self.__scrap_log.write("New entry : " + str(database_entry) + "\n")

