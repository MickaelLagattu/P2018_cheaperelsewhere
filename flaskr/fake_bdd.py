
class FakeBDD:
    """Class thet helps creating a fake BDD for testing purpose"""

    @staticmethod
    def create_fake_bdd(mongo):
        """Creates the fake bdd"""
        database_entry = {
            "title": "Une annonce intéressante",
            "link": "google.com",
            "surface": 25,
            "rooms": 6,
            "location": "Arrondissement : " + '9',
            "price": 6000000,
            "agency": "Century 21",
            "text": "Ceci est une annonce intéressante pour une maison attractive et très bien entretenue",
            "image": "static/TestFrontImages/test_image_1.jpg",
            "similar": []
        }
        mongo.db.ads.insert_one(database_entry)



        database_entry = {
            "title": "Une annonce intéressante 2",
            "link": "wikipedia.org",
            "surface": 25,
            "rooms": 6,
            "location": "Arrondissement : " + '9',
            "price": 6000000,
            "agency": "Century 21",
            "text": "Ceci est une annonce intéressante pour une maison attractive et très bien entretenue",
            "image": "static/TestFrontImages/test_image_1.jpg",
            "similar": []
        }

        mongo.db.ads.insert_one(database_entry)

        database_entry = {
            "title": "Une annonce intéressante 3",
            "link": "centralesupelec.com",
            "surface": 25,
            "rooms": 6,
            "location": "Arrondissement : " + '9',
            "price": 6000000,
            "agency": "Century 21",
            "text": "Ceci est une annonce intéressante pour une maison attractive et très bien entretenue",
            "image": "static/TestFrontImages/test_image_1.jpg",
            "similar": []
        }

        mongo.db.ads.insert_one(database_entry)

        database_entry = {
            "title": "Une annonce intéressante 4",
            "link": "youtube.com",
            "surface": 25,
            "rooms": 6,
            "location": "Arrondissement : " + '9',
            "price": 6000000,
            "agency": "Century 21",
            "text": "Ceci est une annonce intéressante pour une maison attractive et très bien entretenue",
            "image": "static/TestFrontImages/test_image_1.jpg",
            "similar": []
        }

        mongo.db.ads.insert_one(database_entry)

        database_entry = {
            "title": "Une annonce intéressante 5",
            "link": "twitch.tv",
            "surface": 25,
            "rooms": 6,
            "location": "Arrondissement : " + '9',
            "price": 6000000,
            "agency": "Century 21",
            "text": "Ceci est une annonce intéressante pour une maison attractive et très bien entretenue",
            "image": "static/TestFrontImages/test_image_1.jpg",
            "similar": []
        }
        mongo.db.ads.insert_one(database_entry)


        ids = [x['_id'] for x in mongo.db.ads.find({}, {'_id' : 1})]

        mongo.db.ads.update({'_id': ids[0]}, {'$push': {'similar': ids[1]}})
        mongo.db.ads.update({'_id': ids[1]}, {'$push': {'similar': ids[0]}})
        mongo.db.ads.update({'_id': ids[0]}, {'$push': {'similar': ids[2]}})
        mongo.db.ads.update({'_id': ids[2]}, {'$push': {'similar': ids[0]}})
        mongo.db.ads.update({'_id': ids[1]}, {'$push': {'similar': ids[2]}})
        mongo.db.ads.update({'_id': ids[2]}, {'$push': {'similar': ids[1]}})
        mongo.db.ads.update({'_id': ids[3]}, {'$push': {'similar': ids[4]}})
        mongo.db.ads.update({'_id': ids[4]}, {'$push': {'similar': ids[3]}})