from ..resource import Resource


class UserKeyTermResource(Resource):
    def __init__(self, client):
        Resource.__init__(self, client, base_path='/user-key-terms')
        self.resource_name = 'UserKeyTerm'

    def list(self, user_id=None, term=None):
        return self._list(user_id=user_id, term=term)

    def create(self, user_id=None, term=None):
        return self._create(user_id=user_id, term=term)

    def get(self, id):
        return self._get(id)

    def delete(self, id):
        return self._delete(id)
