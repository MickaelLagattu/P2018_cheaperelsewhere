

#import des codes de scrapp

from threading import Thread
import schedule
from .global_comparator import GlobalComparator
from .Scrapp import scrapp_all_century_21
from .scrap_pap import scrapp_all_pap


class Scrapper(Thread):
    """Class that launches the scrapping process regularly, with comparisons and database updates"""

    def __init__(self, mongo):
        """Constructor, mongo is the mongodb object"""
        Thread.__init__(self)
        self.__mongo = mongo
        self.__scrap_log = open("scrap.log", "w")

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

        sites = ["century21.fr", "pap.fr"] # The list of sites to be scrapped

        for site in sites:
            #n_uplets, liens = la commande pour scrapper ce site. Doit renvoyer une liste de n_uplets et la liste des liens correspondants
            #n_uplets, links = [[5000,45,40,"F5",5,75001,"Cette annonce est très belle","Une belle annonce",["static/TestFrontImages/test_image_1.jpg"], "pap.fr123456789"]], [["http://www.google.fr"]]

            if site == "century21.fr":
                my_generator = scrapp_all_century_21
            elif site == "pap.fr":
                my_generator = scrapp_all_pap

            for n_uplet, link in my_generator():

                database_entry = {
                    "title": n_uplet[7],
                    "link": link,
                    "surface": n_uplet[1],
                    "rooms": n_uplet[4],
                    "location": n_uplet[5],
                    "price": n_uplet[0],
                    "agency": site,
                    "text": n_uplet[6],
                    "image": n_uplet[8],
                    "similar": [],
                    "site_id": n_uplet[9]
                }

                print()
                print("Database entry before comparison")
                for key, value in database_entry.items():
                    print(key, "--->", value)
                print()
                print()


                #Comparisons
                similar = GlobalComparator.get_similar(self.__mongo, database_entry)



                database_entry['similar'] = similar
                print("Final similar list : ")
                print(*similar, sep='\n')
                print()

                if self.__mongo.db.ads.find({'site_id': n_uplet[9]}).count() == 0:
                    self.__mongo.db.ads.insert_one(database_entry)
                self.__scrap_log.write("New entry : " + str(database_entry) + "\n")

