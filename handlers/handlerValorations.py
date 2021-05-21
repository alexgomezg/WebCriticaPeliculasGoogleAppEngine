#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from webapp2_extras import jinja2
import time
from Models.Valorations import ValorationsDB
from Models.Films import FilmsDB
from google.appengine.api import users
from Models.SeenFilms import SeemFilmsDB
import random
class valorationsHandler(webapp2.RequestHandler):
    def post(self):
        flag = True
        try:
            action = self.request.get("toDo", "fail")
        except:
            flag=False
            modalText = "Error: Algo inesperado ha sucedido"
        if flag == True:
            if action != 'add' and action !='delete':
                flag = False
                modalText = "Error: El parametro accion es incorrecto"
        #Gestion de usuarios
        user = users.get_current_user()
        if user:
            nickname = user.nickname()[0:user.nickname().index("@")]
            id_user = user.user_id()
            url = users.create_logout_url('/')
        else:
            id_user = -1
            nickname = "no_logged"
            url = users.create_login_url('/')
        if action != 'fail':
            if action == 'add': ##En caso de de se este creando la pelicula
                salir=False
                ##Se crea de forma aleatoria el id de la nueva critica
                while salir == False:
                    id= random.random()*1000000
                    id_critica=int(id)
                    cont=0
                    values = ValorationsDB.query(ValorationsDB.id_critica == id_critica)
                    for value in values:
                        cont=cont+1
                    if cont == 0:
                        salir = True
                try:
                    id_pelicula = int(self.request.get("id_pelicula", "fail"))
                    autor = self.request.get("nombre", "fail")
                    comentario = self.request.get("critica", "fail")
                    rate = float(self.request.get("rate", "fail"))
                    id_usuario = float(self.request.get("id_usuario", "fail"))
                except:
                    modalText = "Error: Algo inesperado ha sucedido"
                    flag = False
                if flag == True:
                    if id_pelicula == 'fail' or autor == 'fail' or comentario == 'fail' or id_usuario == 'fail':
                        modalText = "Error: Alguno de los parametros es incorrecto"
                        flag = False
                    if id_pelicula <= 0 or len(autor)==0 or len(comentario)<50 or id_pelicula <= 0:
                        modalText = "Error: Alguno de los parametros es incorrecto"
                        flag = False
                if flag == True:
                    data = ValorationsDB(id_critica=id_critica,id_pelicula=id_pelicula, autor=autor,comentario=comentario, valoracion=rate, id_usuario=id_usuario)
                    data.put()
                    time.sleep(1)
                    peliculas = FilmsDB.query(FilmsDB.id_pelicula == id_pelicula)
                    list_peliculas=peliculas
                    query = FilmsDB.query(FilmsDB.id_pelicula == id_pelicula)
                    next_entity = query.fetch()
                    for peli in list_peliculas:
                        pelicula_actual = peli
                    next_entity[0].key.delete()
                    valoraciones = ValorationsDB.query(ValorationsDB.id_pelicula == id_pelicula)
                    valMedia = 0
                    cont = 0
                    for val in valoraciones:
                        valMedia = valMedia + val.valoracion
                        cont = cont + 1
                    if cont >0 :
                        valMedia=valMedia/cont

                    data = FilmsDB(id_pelicula=pelicula_actual.id_pelicula, titulo=pelicula_actual.titulo, director=pelicula_actual.director, valoracion=valMedia,
                                   pais=pelicula_actual.pais,
                                   reparto=pelicula_actual.reparto,
                                   sinopsis=pelicula_actual.sinopsis,
                                   link_imagen=pelicula_actual.link_imagen, link_trailer=pelicula_actual.link_trailer)
                    data.put()
                    time.sleep(1)
                    susts = {
                        "url": url,
                        "nickname": nickname,
                        "peliculas": peliculas,
                        "id_user": id_user,
                        "valoraciones": valoraciones,
                        "val_media": valMedia,
                        "id_pelicula": id_pelicula,
                        "modalText":"Tu critica se ha guardado correctamente"
                    }
                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(
                        jinja.render_template("showFilmTemplate.html", **susts)
                    )
            else: ##En caso de de se este borrando la pelicula
                try:
                    id_critica = self.request.get("id", "fail")
                    id_pelicula = int(self.request.get("id_pelicula", "fail"))
                except:
                    modalText = "Error: Algo inesperado ha sucedido"
                    flag = False
                if flag == True:
                    if id_pelicula == 'fail' or id_critica == 'fail':
                        modalText = "Error: Alguno de los parametros es incorrecto"
                        flag = False
                if flag == True:
                    query = ValorationsDB.query(ValorationsDB.id_critica== int(id_critica))
                    next_entity = query.fetch()
                    next_entity[0].key.delete()
                    peliculas = FilmsDB.query(FilmsDB.id_pelicula == id_pelicula)
                    list_peliculas=peliculas
                    for peli in list_peliculas:
                        pelicula_actual = peli
                    valoraciones = ValorationsDB.query(ValorationsDB.id_pelicula == id_pelicula)
                    valMedia = 0
                    cont = 0
                    query = FilmsDB.query(FilmsDB.id_pelicula == id_pelicula)
                    next_entity = query.fetch()
                    next_entity[0].key.delete()
                    for val in valoraciones:
                        valMedia = valMedia + val.valoracion
                        cont = cont + 1
                    if cont > 0:
                        valMedia = valMedia / cont
                    data = FilmsDB(id_pelicula=pelicula_actual.id_pelicula, titulo=pelicula_actual.titulo,
                                   director=pelicula_actual.director, valoracion=valMedia,
                                   pais=pelicula_actual.pais,
                                   reparto=pelicula_actual.reparto,
                                   sinopsis=pelicula_actual.sinopsis,
                                   link_imagen=pelicula_actual.link_imagen, link_trailer=pelicula_actual.link_trailer)
                    data.put()
                    time.sleep(1)
                    pelis = FilmsDB.query()
                    pelis_list = {}
                    for peli in pelis:
                        pelis_list[peli.id_pelicula] = peli.titulo
                    valoraciones = ValorationsDB.query(ValorationsDB.id_usuario == float(user.user_id()))
                    susts = {
                        "valoraciones": valoraciones,
                        "url": url,
                        "nickname": nickname,
                        "pelis": pelis_list,
                        "modalText":"Tu critica se ha borrado correctamente"
                    }
                    jinja = jinja2.get_jinja2(app=self.app)
                    self.response.write(
                        jinja.render_template("showCriticsTemplate.html", **susts)
                    )
            ##Si se produce algun error
            if flag == False:
                pelis = FilmsDB.query()
                numPelis = len(list(pelis))
                favs = {}
                if user:
                    if users.is_current_user_admin():
                        admin = "admin"
                    nickname = user.nickname()[0:user.nickname().index("@")]
                    id_user = user.user_id()
                    url = users.create_logout_url('/')
                    favoritos = SeemFilmsDB.query(SeemFilmsDB.id_usuario == float(id_user))
                    for fav in favoritos:
                        favs[fav.id_pelicula] = "yes"
                else:
                    id_user = -1
                    nickname = "no_logged"
                    url = users.create_login_url('/')
                susts = {
                    "url": url,
                    "nickname": nickname,
                    "id_user": id_user,
                    "favoritos": favs,
                    "peliculas": pelis,
                    "admin": admin,
                    "numPelis": numPelis,
                    "modalText": modalText
                }
                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(
                    jinja.render_template("listFilmsTemplate.html", **susts)
                )


app = webapp2.WSGIApplication([
    ('/handlerValorations', valorationsHandler)
], debug=True)
