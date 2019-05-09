from resource_flows import Resource

class Contributor:
    def __init__(self, a_name):
        self.name = a_name
        self.resources = {}

    def add_resource(self, a_resource:Resource):
        self.resources[a_resource.type] = a_resource
