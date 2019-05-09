import json

from investment import Investment
from project import Project
import pymongo


class Model:
    def __init__(self, mongo_client_adress=None):
        self.people = {}
        self.projects = {}
        self.investments= {}
        self.mgdb = pymongo.MongoClient(mongo_client_adress or "mongodb://localhost:27017/")["lookforward"]

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

if __name__ == '__main__':
    model = Model.from_mongoDB("mongodb://localhost:27017/lookforward")

    print(model.projects)