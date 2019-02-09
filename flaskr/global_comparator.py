
import imageComparator
print("import text scoring")
from .ce_text_processing.ce_text_scoring import TextScoring
print("text scoring imported ")

class GlobalComparator:
    """Class for comparisons of ads"""





    @staticmethod
    def get_similar(mongo, ad):
        """Get the ads similar to this n_uplet"""
        place = ad['location']
        surface = ad['surface']
        site_id = ad['site_id']
        print("Comparaison de l'annonce ", site_id)
        threshold = 0.9
        if type(surface) == int and place != 'NC':
            surface_min, surface_max = surface*0.8, surface*1.2
            potential_similar = mongo.db.ads.find(
                {'location': place, 'surface': {"$gt": surface_min, "$lt": surface_max}, 'agency': {'$ne': ad['agency']}})
        elif place != "NC":
            potential_similar = mongo.db.ads.find({'location': place, 'agency': {'$ne': ad['agency']}})
        elif type(surface) == int:
            surface_min, surface_max = surface * 0.8, surface * 1.2
            potential_similar = mongo.db.ads.find(
                {'surface': {"$gt": surface_min, "$lt": surface_max}, 'agency': {'$ne': ad['agency']}})
        else:
            # Not enough info
            potential_similar = []
            # potential_similar = mongo.db.ads.find({'agency': {'$ne': ad['agency']}})

        similar = []
        potential_similar = list(potential_similar)
        print("avec les annonces", potential_similar)
        for ad2 in potential_similar:
            if GlobalComparator.__compare(ad, ad2) >= threshold:
                similar.append(ad2["site_id"])

        #We have to append the new ad to its similar ads's lists

        for site_id_similar in similar:
            mongo.db.ads.update({"site_id": site_id_similar}, {"$addToSet":{"similar": site_id}})

        return similar




    @staticmethod
    def __compare(ad1, ad2):

        weight_text = 0.05
        weight_image = 0.4
        weight_surface = 0.25
        weight_rooms = 0.2
        weigh_price = 0.1

        #If a coeff is NC, the booleans will be false
        surface = True
        rooms = True
        price = True

        score_text = weight_text * TextScoring.get_score(ad1['text'],ad2["text"])
        max_score_image = 0
        for image1 in ad1["image"] :
            for image2 in ad2["image"] :
                print("Comparaison d'image : ", image1)
                print("avec", image2)
                if imageComparator.global_score(image1, image2) > max_score_image:
                    max_score_image = imageComparator.global_score(image1, image2)
        score_image = weight_image*max_score_image
        if ad1["price"] != "NC" and ad2["price"] != "NC" :
            score_price = weigh_price * GlobalComparator.__relative_diff(ad1["price"], ad2["price"])
        else :
            score_price = 0
            price = False

        if ad1["rooms"] != "NC" and ad2["rooms"] != "NC" :
            score_rooms = weight_rooms * GlobalComparator.__relative_diff(ad1["rooms"], ad2["rooms"])
        else :
            score_rooms = 0
            rooms = False

        if ad1["surface"] != "NC" and ad2["surface"] != "NC" :
            score_surface = weight_surface * GlobalComparator.__relative_diff(ad1["surface"], ad2["surface"])
        else :
            score_surface = 0
            surface = False

        # Rebalance of weights:
        denominator = weight_text + weight_image + weight_surface*surface + weight_rooms*rooms + weigh_price*price

        score = (score_rooms + score_text + score_price + score_surface + score_image) / denominator

        print("Comparaison", ad1['site_id'], "avec", ad2['site_id'], "score :", score)

        return score


    @staticmethod
    def __relative_diff(v1, v2):
        """Computes the relative difference between 2 values"""
        try:
            value = 1 - (v1 - v2)/v1
        except TypeError:
            value = 0
        return value
