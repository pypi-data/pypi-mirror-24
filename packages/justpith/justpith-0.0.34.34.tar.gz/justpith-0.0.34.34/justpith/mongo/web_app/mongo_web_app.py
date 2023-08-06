from ..mongo import Mongo

class MongoWebApp(Mongo):
    def __init__(self,host, port, db):
        super(MongoWebApp,self).__init__(host, port, db)


    def get_news_reccomandations(self, user_id):
        selected_collection = self.connection["Users"]
        result = selected_collection.find_one({"_id": str(user_id)},{"raccomandations":1})
        selected_collection = self.connection["News"]
        racc_list = []
        for id_news, weight in result["raccomandations"].iteritems():
            racc_news = {}
            news = selected_collection.find_one({"_id": int(id_news)})
            racc_news["_id"] = id_news
            racc_news["weight"] = weight
            #print(str(news)+" id:"+id_news+" weight:"+str(weight))
            racc_news["category_title"] = news["category_title"]
            racc_news["news_source"] = news["news_source"]
            racc_news["url"] = news["url"]
            racc_news["article"] = news["article"]
            racc_news["title"] = news["title"]
            racc_list.append(racc_news)

        return racc_list