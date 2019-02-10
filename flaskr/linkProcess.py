
class LinkProcess:
    """Class that will be used to receive the link sent by the user and return the results from the DB"""

    @staticmethod
    def process(link, mongo):
        """Search for similar announces in the DB and returns the results"""

        print("Lien :", link)

        #Find the website
        splitted_link = link.split('.')
        site = None
        try:
            nom_site = splitted_link[-2]
            terminaison = ''
            i = 0
            while i < len(splitted_link[-1]):
                if splitted_link[-1][i] not in "abcdefghijklmnopqrstuvwxyz":
                    break
                terminaison += splitted_link[-1][i]
                i += 1

            site = nom_site + '.' + terminaison

            #find the reference depending on the site
            if site == "century21.fr":
                link_without_arguments = link.split('?')[0]
                splitted = link_without_arguments.split('/')
                site_id = splitted[-2]
            elif site == "pap.fr":
                link_without_arguments = link.split('?')[0]
                splitted = link_without_arguments.split('-')
                site_id = splitted[-1]
            else:
                return []
        except:
            return []

        final_site_id = site.split(".")[0] + " " + site_id

        print("Site id : ", final_site_id)

        #Find this ad in our db
        ad_in_db = mongo.db.ads.find({'site_id': final_site_id})
        if ad_in_db.count() == 0:
            print("Not in DB")
            return []
        else:
            ad = ad_in_db[0]

            #Get similar ads
            similar = ad['similar']

            results = mongo.db.ads.find({'site_id': {"$in" : similar}})

            ads_found = [x["site_id"] for x in results]
            print(ads_found)



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
            "image": ["/static/TestFrontImages/test_image_1.jpg"]

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
            "image": ["/static/TestFrontImages/test_image_2.jpg"]
        }


        return [result1, result2]