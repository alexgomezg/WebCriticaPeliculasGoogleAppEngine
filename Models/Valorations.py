from google.appengine.ext import ndb

class ValorationsDB(ndb.Model):
    id_critica = ndb.IntegerProperty(required=True)
    id_pelicula=ndb.IntegerProperty(required=True)
    autor=ndb.TextProperty(required=True)
    comentario = ndb.TextProperty(required=True)
    valoracion = ndb.FloatProperty(required=True)
    id_usuario = ndb.FloatProperty(required=True)

