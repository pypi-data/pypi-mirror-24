import os
from basePhantom import _BasePhantom


class _PhantomUsers(_BasePhantom):
    def __init__(self, host, username, password):
        _BasePhantom.__init__(self, host, username, password)
        self.endpoint_url = os.path.join(self.host, "ph_user")

    def query(self, query=None):
        url = self.endpoint_url
        if query is not None:
            url += "?%s" % query

        return self.__make_rest_request__(url, "GET")

    def get(self, id):
        if id is None:
            raise ValueError("id is required")

        url = os.path.join(self.endpoint_url, str(id))
        return self.__make_rest_request__(url, "GET")

    def create(self, obj):
        """
        Create a new phantom user
        :param obj: a dictionary object containing the user information.
        :return: json response from the phantom endpoint
        """
        if "username" not in obj:
            raise KeyError("required key missing")

        return self.__make_rest_request__(self.endpoint_url, "POST", data=obj)

    def add_roles(self, id, role_ids):
        url = os.path.join(self.endpoint_url, id)

        if not isinstance(role_ids, list):
            role_ids = [role_ids]

        data = { "add_roles": role_ids }
        return self.__make_rest_request__(url, "POST", data=data)