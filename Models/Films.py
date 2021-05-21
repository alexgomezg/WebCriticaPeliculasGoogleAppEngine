from google.appengine.ext import ndb

class FilmsDB(ndb.Model):
    id_pelicula=ndb.IntegerProperty(required=True)
    titulo=ndb.StringProperty(required=True)
    director = ndb.StringProperty(required=True)
    valoracion = ndb.FloatProperty(required=True)
    pais= ndb.StringProperty(required=True)
    reparto =ndb.TextProperty(required=True)
    sinopsis = ndb.TextProperty(required=True)
    link_imagen = ndb.StringProperty(required=True)
    link_trailer = ndb.StringProperty(required=True)
