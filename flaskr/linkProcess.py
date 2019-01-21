

class LinkProcess:
    """Class that will be used to receive the link sent by the user and return the results from the DB"""

    @staticmethod
    def process(link, mongo):
        """Search for similar announces in the DB and returns the results"""

        #Find this ad in our db
        ad_in_db = mongo.db.ads.find({'link': link})
        if ad_in_db.count() == 0:
            return {}
        else:
            ad = ad_in_db[0]

            #Get similar ads
            similar = ad['similar']

            results = mongo.db.ads.find({'_id': {"$in" : similar}})



            return list(results)

    @staticmethod
    def process_test(link, mongo):
        """Same but with fake results to test front"""

        result1 = {
            "id": 123,
            "title": "Jolie annonce",
            "link": "http://www.google.fr",
            "surface": 12,
            "rooms": 2,
            "location": "Paris 16e",
            "price" : 9999999,
            "agency": "Century 42",
            "text": "Ceci est une annonce de type attractive.",
            "image": "/static/TestFrontImages/test_image_1.jpg"

        }
        result2 = {
            "id": 128,
            "title": "Annonce pas ouf",
            "link": "http://www.centralesupelec.fr",
            "surface": 12,
            "rooms": 2,
            "location": "Gif-sur-Yvette",
            "price": 9999999,
            "agency": "P.u.P",
            "text": "Ceci est une annonce de type attractive mais pas top.",
            "image": "/static/TestFrontImages/test_image_2.jpg"
        }


        return [result1, result2]