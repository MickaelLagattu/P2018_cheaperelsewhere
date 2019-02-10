

#import des codes de scrapp

from threading import Thread
import schedule
from .global_comparator import GlobalComparator
from .Scrapp import scrapp_all_century_21, scrapp_century21
from .scrap_pap import scrapp_all_pap, scrapp_pap


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

    def run(self):
        """Launches the scrapping process regularly. Must be called at server startup"""

        # self.__scrapp_all()

        # schedule.every().day.at("00:00").do(self.__scrapp_all)

        # Tests de scrap d'1 annonce à la fois
        self.__scrap_one_pap("https://www.pap.fr/annonces/appartement-paris-13e-r423901287")
        self._scrap_one_c21("https://www.century21.fr/trouver_logement/detail/1768710414/?came_from=/annonces/achat-maison-appartement/cp-75013/s-0-/st-0-/b-0-/page-1/")

    def __scrapp_all(self):
        """Scrapps all the sites, must be called once a day"""

        self.__scrap_log.write("Launching scrapper\n")

        sites = ["pap.fr", "century21.fr"] # The list of sites to be scrapped

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
                    "surface": str(n_uplet[1]),
                    "rooms": str(n_uplet[5]),
                    "location": str(n_uplet[4]),
                    "price": str(n_uplet[0]),
                    "agency": site,
                    "text": n_uplet[6],
                    "image": n_uplet[8],
                    "similar": [],
                    "site_id": n_uplet[9]
                }

                print()
                print("Database entry before comparison")
                for key, value in database_entry.items():
                    try :
                        print(key, "--->", value)
                    except UnicodeEncodeError:
                        print("error in print")
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


    def _scrap_one_c21(self, link):
        """Fuunction that scraps one ad from given link. Only for testing."""
        n_uplet = scrapp_century21(link)
        site = "century21.fr"

        database_entry = {
            "title": n_uplet[7],
            "link": link,
            "surface": n_uplet[1],
            "rooms": n_uplet[5],
            "location": n_uplet[4],
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
            try:
                print(key, "--->", value)
            except UnicodeEncodeError:
                 print("error in print")
        print()
        print()

        # Comparisons
        similar = GlobalComparator.get_similar(self.__mongo, database_entry)

        database_entry['similar'] = similar
        print("Final similar list : ")
        print(*similar, sep='\n')
        print()

        if self.__mongo.db.ads.find({'site_id': n_uplet[9]}).count() == 0:
            self.__mongo.db.ads.insert_one(database_entry)
        else:
            print("Already in database")
        self.__scrap_log.write("New entry : " + str(database_entry) + "\n")



    def __scrap_one_pap(self, link):
        """Function that scraps one ad from given link. Only for testing."""
        n_uplet = scrapp_pap(link)
        site = "pap.fr"

        database_entry = {
            "title": n_uplet[7],
            "link": link,
            "surface": n_uplet[1],
            "rooms": n_uplet[5],
            "location": n_uplet[4],
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
            try:
                 print(key, "--->", value)
            except UnicodeEncodeError:
                 print("error in print")
        print()
        print()

        # Comparisons
        similar = GlobalComparator.get_similar(self.__mongo, database_entry)

        database_entry['similar'] = similar
        print("Final similar list : ")
        print(*similar, sep='\n')
        print()

        if self.__mongo.db.ads.find({'site_id': n_uplet[9]}).count() == 0:
            self.__mongo.db.ads.insert_one(database_entry)
        else:
            print("Already in database")
        self.__scrap_log.write("New entry : " + str(database_entry) + "\n")