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
from Models.Films import FilmsDB
from Models.Valorations import ValorationsDB
from google.appengine.api import users
from Models.SeenFilms import SeemFilmsDB
class ShowFilmHandler(webapp2.RequestHandler):
    def post(self):
        mensaje="null"
        flag=True
        try:
            id = int(self.request.get("clickado", "fail"))
        except:
            mensaje = "Error: Algo inesperado ha sucedido"
            flag = False
        if flag == True:
            if id <= 0:
                mensaje = "Error: El id introducido es incorrector"
                flag = False
        if flag == True:
            peliculas = FilmsDB.query(FilmsDB.id_pelicula == id)
            valoraciones = ValorationsDB.query(ValorationsDB.id_pelicula == id)
            valMedia=0
            cont=0
            for val in valoraciones:
                valMedia=valMedia+val.valoracion
                cont=cont+1
            if cont > 0:
                valMedia = valMedia / cont
            user = users.get_current_user()
            if user:
                nickname=user.nickname()[0:user.nickname().index("@")]
                id_user=user.user_id()
                url = users.create_logout_url('/')
            else:
                id_user = -1
                nickname="no_logged"
                url = users.create_login_url('/')
            susts={
                "url": url,
                "nickname": nickname,
                "id_user": id_user,
                "peliculas": peliculas,
                 "valoraciones":valoraciones,
                "val_media":valMedia,
                "id_pelicula":id,
                "modalText":"null"
            }
            jinja=jinja2.get_jinja2(app=self.app)
            self.response.write(
                jinja.render_template("showFilmTemplate.html",**susts)
            )
        else:
            ##Si se produce algun error
            if flag == False:
                pelis = FilmsDB.query()
                numPelis = len(list(pelis))
                favs = {}
                user = users.get_current_user()
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
                    "modalText": mensaje
                }
                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(
                    jinja.render_template("listFilmsTemplate.html", **susts)
                )


app = webapp2.WSGIApplication([
    ('/showfilm', ShowFilmHandler)
], debug=True)
