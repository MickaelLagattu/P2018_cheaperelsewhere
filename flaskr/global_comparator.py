from ce_text_processing.ce_text_scoring import TextScoring
from imageComparator import histogram,SSIM

class GlobalComparator:
    """Class for comparisons of ads"""

    weight_text = 0.05
    weight_image = 0.4
    weight_surface = 0.25
    weight_rooms = 0.2
    weigh_price = 0.1
    
    def __compare_(n1, n2):
        if n1 == n2 == 0 :
            return 0
        return 1-abs(n1-n2)/max(n1,n2)
    @staticmethod
    def get_similar(mongo, ad):
        """Get the ads similar to this n_uplet"""
        place = ad['location']
        surface = ad['surface']
        site_id = ad['site_id']
        if type(surface) == int and place != 'NC':
            surface_min, surface_max = surface*0.8, surface*1.2
            potential_similar = mongo.db.ads.find(
                {'location': place, 'surface': {"$gt": surface_min, "$lt": surface_max}})
        elif place != "NC":
            potential_similar = mongo.db.ads.find({'location': place})
        elif type(surface) == int:
            surface_min, surface_max = surface * 0.8, surface * 1.2
            potential_similar = mongo.db.ads.find(
                {'surface': {"$gt": surface_min, "$lt": surface_max}})
        else:
            potential_similar = mongo.db.ads.find()

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
        score_text = weight_text * TextScoring.get_score(ad1['text'],ad2["text"])
        max_score_image = 0
        for image1 in ad1["image"] :
            for image2 in ad2["image"] :
                image_ssim = SSIM(image1,image2)
                image_score_ssim = image_ssim.compare_images()[1]
                if max_score_image < image_score_ssim :
                    max_score_image = image_score_ssim

                image_hist = histogram(ad1["image"],ad2["image"])
                image_score_hist = image_hist.correlation()
                if max_score_image < image_score_hist :
                    max_score_image = image_score_hist
        score_image = weight_image*max_score_image
        if ad1["price"] != "NC" and ad2["price"] != "NC" :
            score_price = weigh_price * __compare_(ad1["price"],ad2["price"])
        else :
            score_price = 0

        if ad1["rooms"] != "NC" and ad2["rooms"] != "NC" :
            score_rooms = weigh_rooms * __compare_(ad1["rooms"],ad2["rooms"])
        else :
            score_rooms = 0

        if ad1["surface"] != "NC" and ad2["surface"] != "NC" :
            score_surface = weigh_surface * __compare_(ad1["surface"],ad2["surface"])
        else :
            score_surface = 0

        return score_rooms + score_text + score_price + score_surface + score_image
