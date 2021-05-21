from google.appengine.ext import ndb

class SeemFilmsDB(ndb.Model):
    id_usuario=ndb.FloatProperty(required=True)
    id_pelicula=ndb.IntegerProperty(required=True)


