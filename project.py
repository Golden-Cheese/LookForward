import collections
from typing import Optional


class Project(dict):
    def __init__(self, name, description: Optional[str] = None, constituents: Optional['Project'] = None,
                 cost: Optional[dict] = None, _id=None):
        """
        A Project object which is built on Python's dictionary object with some additional project-related
        methods (see ´cost´, ´ time_to_completion´)

        :param name: The name of the project
        :type name: str
        :param description: a short description of the project
        :type description: Optional[str]
        :param constituents: sub-projects contained in this project
        :type constituents: Optional['Project']
        :param cost: total cost of this project, including sub-project costs
        :type cost: Optional[dict]
        """
        # assert all(elem in ["name", "description", "cost"] for elem in kwargs.keys() )
        super(Project, self).__init__([("name", name),
                                       ("description", description),
                                       ("constituents", constituents or list()),
                                       ("cost", cost or dict())])
        self["_id"] = _id or id(self)

    def add_subproject(self, sub_project):
        self["constituents"].append(sub_project)

    @property
    def cost(self):
        counter = collections.Counter()
        counter.update(self["cost"])
        for c in self["constituents"]:
            counter.update(c.cost)
        return counter

    def time_to_completion(self, investments: []):  # todo investment timeline ?
        c = self.cost
        d = {}
        if not investments:
            for k, v in c.items():
                d[k] = None
            return d
        else:
            monthly = [i for i in investments if i.is_mensual]
            once = [i for i in investments if not i.is_mensual]

            c.subtract(o["amounts"] for o in once)
            monthly_amount = collections.Counter()
            for m in monthly:
                monthly_amount.update(m["amounts"])

            for k, v in c.items():
                if v > 0:
                    if monthly_amount[k] == 0:
                        d[k] = None
                    else:
                        d[k] = v / monthly_amount[k]
                else:
                    d[k] = 0
            return d

    @staticmethod
    def from_json(json_object):
        for key in json_object.keys():  # check if json is well formed
            assert key in ["name", "description", "constituents", "cost", "_id"], str(key) + " not in " + str(["name", "description", "constituents", "cost", "_id"])
        return Project(**json_object)
