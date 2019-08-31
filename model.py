import json

from bson import ObjectId

from investment import Investment
from project import Project
import pymongo


class Model:
    def __init__(self, mongo_client_address=None):
        self.people = {}
        self.projects = {}
        self.investments = {}
        self.mgdb = pymongo.MongoClient(mongo_client_address or "mongodb://localhost:27017/")["lookforward"]

    def investment_from_json_obj(self, js_obj):
        inv = Investment.from_json(json_object=js_obj)
        assert inv['_id'] not in self.investments, "tried to load more than one investment with same id"
        self.investments[inv['_id']] = inv

    def investment_from_json_file(self, j_f_path):
        with open(j_f_path) as f:
            js_obj = json.load(f)
            self.investment_from_json_obj(js_obj)

    def investments_from_json_files(self, json_file_paths):
        for j_f_path in json_file_paths:
            self.investment_from_json_file(j_f_path)

    def project_from_json_obj(self, js_obj):
        pro = Project.from_json(json_object=js_obj)
        assert pro['_id'] not in self.projects, "tried to load more than one project with same id"
        self.projects[pro['_id']] = pro

    def project_from_json_file(self, j_f_path):
        with open(j_f_path) as f:
            js_obj = json.load(f)
            self.project_from_json_obj(js_obj)

    def projects_from_json_files(self, json_file_paths):
        for j_f_path in json_file_paths:
            self.project_from_json_file(j_f_path)

    # def person_from_json_obj(self, js_obj):
    #     per = Person.from_json(json_object=js_obj)
    #         assert per['_id'] not in self.people, "tried to load more than one person with same id"
    #         self.people[per['_id']] = per

    # def person_from_json_file(self, j_f_path):
    #     with open(j_f_path) as f:
    #         js_obj = json.load(f)
    #         self.person_from_json_obj(js_obj)
    #
    # def investments_from_json_files(self, json_file_paths):
    #     for j_f_path in json_file_paths:
    #         self.person_from_json_file(j_f_path)

    @staticmethod
    def from_mongoDB(mongo_client_adress):
        model = Model(mongo_client_adress)
        for pro in model.mgdb["projects"].find():
            model.project_from_json_obj(pro)
        for inv in model.mgdb["investments"].find():
            model.investment_from_json_obj(inv)
        # for per in Model.mgdb["people"].find():
        #     Model.project_from_json_obj(per)
        return model


class Model_Lazy:
    def __init__(self, mongo_client_adress:str=None):
        """
        This version of the model does not keep a buffered version of the database, it is 'lazy loading' (see
        `https://en.wikipedia.org/wiki/Lazy_loading`), it feches the data only when asked to provide the data.

        :param mongo_client_adress: the string address of the MongoDB database containing the data
        """
        self.people = {}
        self.mgdb = pymongo.MongoClient(mongo_client_adress or "mongodb://localhost:27017/")["lookforward"]
        print(list(i for i in self.mgdb["projects"].find()))

    @property
    def projects(self):
        for pro in self.mgdb["projects"].find():
            yield Model_Lazy.project_from_json_obj(pro)

    @property
    def investments(self):
        for inv in self.mgdb["investments"].find():
            yield Model_Lazy.investment_from_json_obj(inv)

    def save_project(self, project):
        self.mgdb["projects"].update_one(filter={'_id':project['_id']}, update={"$set":project},upsert=True)

    def save_investment(self, investment):
        self.mgdb["investments"].update_one(filter={'_id':investment['_id']}, update={"$set":investment},upsert=True)

    @staticmethod
    def investment_from_json_obj(js_obj):
        return Investment.from_json(json_object=js_obj)

    def investment_from_json_file(self, j_f_path):
        with open(j_f_path) as f:
            js_obj = json.load(f)
            return self.investment_from_json_obj(js_obj)

    def investments_from_json_files(self, json_file_paths):
        for j_f_path in json_file_paths:
            yield self.investment_from_json_file(j_f_path)

    @staticmethod
    def project_from_json_obj(js_obj):
        return Project.from_json(json_object=js_obj)

    def project_from_json_file(self, j_f_path):
        with open(j_f_path) as f:
            js_obj = json.load(f)
            return self.project_from_json_obj(js_obj)

    def projects_from_json_files(self, json_file_paths):
        for j_f_path in json_file_paths:
            yield self.project_from_json_file(j_f_path)

    # def person_from_json_obj(self, js_obj):
    #     per = Person.from_json(json_object=js_obj)
    #         assert per['_id'] not in self.people, "tried to load more than one person with same id"
    #         self.people[per['_id']] = per

    # def person_from_json_file(self, j_f_path):
    #     with open(j_f_path) as f:
    #         js_obj = json.load(f)
    #         self.person_from_json_obj(js_obj)
    #
    # def investments_from_json_files(self, json_file_paths):
    #     for j_f_path in json_file_paths:
    #         self.person_from_json_file(j_f_path)

    @staticmethod
    def from_mongoDB(mongo_client_adress):
        model = Model_Lazy(mongo_client_adress)
        for pro in model.mgdb["projects"].find():
            print(pro)
            model.project_from_json_obj(pro)
        for inv in model.mgdb["investments"].find():
            print(inv)
            model.investment_from_json_obj(inv)
        # for per in Model.mgdb["people"].find():
        #     Model.project_from_json_obj(per)
        return model


if __name__ == '__main__':
    # Uncomment the three line that follow to reset/empty the MongoDB database.
    # mgdb = pymongo.MongoClient("mongodb://localhost:27017/")["lookforward"]
    # mgdb["projects"].delete_many({})
    # mgdb["investments"].delete_many({})

    model = Model_Lazy.from_mongoDB("mongodb://localhost:27017/lookforward")

    print(list(model.investments))
    print('5d6aae1fdff6b4ff473a86a5')
    i = Investment("timothy", "project2", 10, is_mensual=False, _id='5d6aae1fdff6b4ff473a86a5')
    print(i)
    model.save_investment(i)
    print(list(model.investments))
