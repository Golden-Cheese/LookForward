class Investment(dict):
    def __init__(self, personID, projectID, amounts, is_mensual, _id=None):
        super().__init__([("personID", personID),
                          ("projectID", projectID),
                          ("values", amounts),
                          ("is_mensual", is_mensual)])
        self._id = _id or id(self)

    @staticmethod
    def from_json(json_object):
        for key in json_object.keys():  # check if json is well formed
            assert key in ["personID", "project", "amounts", "is_mensual", "_id"], str(key) + " not in " + str(["personID", "project", "amounts", "is_mensual", "_id"])
        return Investment(**json_object)


if __name__ == '__main__':
    i = Investment("timothy", "project", 10)
    print(i._id)
    i2 = Investment("timothy", "project", 10)
    print(i2._id)
    i3 = Investment("timothy", "project", 10)
    print(i3._id)
