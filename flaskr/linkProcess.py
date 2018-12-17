

class LinkProcess:
    """Class that will be used to receive the link sent by the user and return the results from the DB"""

    @staticmethod
    def process(link):
        """Search for similar announces in the DB and returns the results"""
        results = {}


        return results

    @staticmethod
    def process_test(link):
        """Same but with fake results to test front"""

        result1 = {
            "id": 123,
            "title": "Jolie annonce",
            "link": "www.google.fr",
            "surface": 12,
            "rooms": 2,
            "location": "Paris 16e",
            "price" : 9999999,
            "agency": "Century 42",
            "text": "Ceci est une annonce de type attractive.",
            "images": [
                {"link": "/static/TestFrontImages/test_image_1.jpg"}
            ]
        }
        result2 = {
            "id": 128,
            "title": "Annonce pas ouf",
            "link": "www.centralesupelec.fr",
            "surface": 12,
            "rooms": 2,
            "location": "Gif-sur-Yvette",
            "price": 9999999,
            "agency": "P.u.P",
            "text": "Ceci est une annonce de type attractive mais pas top.",
            "images": [
                {"link": "/static/TestFrontImages/test_image_2.jpg"}
            ]
        }


        return [result1, result2]