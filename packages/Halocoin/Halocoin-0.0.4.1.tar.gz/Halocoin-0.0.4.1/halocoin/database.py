import json
import leveldb
import os

from service import Service, sync


class DatabaseService(Service):
    def __init__(self, engine):
        Service.__init__(self, name='database')
        self.engine = engine
        self.database_name = self.engine.config['database.name']
        self.DB = None
        self.salt = None
        self.set_state(Service.INIT)

    def on_register(self):
        self.DB = leveldb.LevelDB(self.database_name)
        try:
            self.salt = self.DB.Get('salt')
        except KeyError:
            self.salt = os.urandom(5)
            self.DB.Put('salt', self.salt)
        return True

    @sync
    def get(self, key):
        """Gets the key in args[0] using the salt"""
        try:
            return json.loads(self.DB.Get(self.salt + str(key)))
        except KeyError:
            return None

    @sync
    def put(self, key, value):
        """
        Puts the val in args[1] under the key in args[0] with the salt
        prepended to the key.
        """
        try:
            self.DB.Put(self.salt + str(key), json.dumps(value))
            return True
        except:
            return False

    @sync
    def exists(self, key):
        """
        Checks if the key in args[0] with the salt prepended is
        in the database.
        """
        try:
            self.DB.Get(self.salt + str(key))
        except KeyError:
            return False
        else:
            return True

    @sync
    def delete(self, key):
        """
        Removes the entry in the database under the the key in args[0]
        with the salt prepended.
        """
        try:
            self.DB.Delete(self.salt + str(key))
            return True
        except:
            return False