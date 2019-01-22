

class GlobalComparator:
    """Class for comparisons of ads"""


    @staticmethod
    def get_similar(mongo, ad):
        """Get the ads similar to this n_uplet"""
        place = ad['location']
        surface = ad['surface']
        site_id = ad['site_id']
        surface_min, surface_max = surface*0.8, surface*1.2

        potential_similar = mongo.db.ads.find({'location': place, 'surface': {"$gt" : surface_min, "$lt": surface_max}})

        similar = []
        for ad2 in potential_similar:
            if GlobalComparator.__compare(ad, ad2):
                similar.append(ad2["site_id"])

        #We have to append the new ad to its similar ads's lists

        for site_id_similar in similar:
            mongo.db.ads.update({"site_id": site_id_similar}, {"$addToSet":{"similar": site_id}})

        return similar





    @staticmethod
    def __compare(ad1, ad2):
