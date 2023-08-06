import os
from basePhantom import _BasePhantom


class _PhantomRoles(_BasePhantom):
    def __init__(self, host, username, password):
        _BasePhantom.__init__(self, host, username, password)
        self.endpoint_url = os.path.join(self.host, "role")

    def query(self, query=None):
        """
        Query the phantom roles
        :param query: Optional query to filter the roles down
        :return: json response from the phantom endpoint
        """
        url = self.endpoint_url
        if query is not None:
            url += "?%s" % query

        return self.__make_rest_request__(url, "GET")

    def get(self, id):
        """
        Get a phantom role by it's id
        :param id: The id of the role
        :return: json response from the phantom endpoint
        """
        if id is None:
            raise ValueError("id is required")

        url = os.path.join(self.endpoint_url, str(id))
        return self.__make_rest_request__(url, "GET")

    def create(self, obj):
        """
        Create a new phantom role
        :param obj: a dictionary object containing the role information.
        :return: json response from the phantom endpoint
        """
        if "name" not in obj or "description" not in obj:
            raise KeyError("required key missing")

        return self.__make_rest_request__(self.endpoint_url, "POST", data=obj)

    def add_users(self, id, user_ids):
        url = os.path.join(self.endpoint_url, str(id))

        if not isinstance(user_ids, list):
            user_ids = [user_ids]

        data = {
            "add_users": user_ids
        }

        return self.__make_rest_request__(url, "POST", data=data)