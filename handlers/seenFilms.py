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
from Models.SeenFilms import SeemFilmsDB
from Models.Films import FilmsDB
from google.appengine.api import users
class seenFilmsHandler(webapp2.RequestHandler):
    def post(self):
        flag=True
        try:
            id_pelicula = int(self.request.get("id_pelicula", "fail"))
            id_user = float(self.request.get("id_user", "fail"))
            action = self.request.get("toDo", "fail")
        except:
            mensaje = "Error: Algo inesperado ha sucedido"
            flag = False
        if flag == True:
            if (action != 'add' and action != 'delete') or id_pelicula <= 0 and id_user <= 0.0:
                mensaje = "Error: Alguno de los parametros es incorrecto"
                flag = False
        if flag == True:
            if action != 'fail':
                if action == 'add':
                    data = SeemFilmsDB(id_pelicula=id_pelicula, id_usuario=id_user)
                    data.put()
                    mensaje="Tu pelicula se ha guardado en peliculas vistas correctamente"
                else:
                    query = SeemFilmsDB.query(SeemFilmsDB.id_pelicula == id_pelicula)
                    next_entity = query.fetch()
                    next_entity[0].key.delete()
                    mensaje = "Tu pelicula se ha borrado de peliculas vistas correctamente"
            time.sleep(1)
        pelis = FilmsDB.query()
        numPelis=len(list(pelis))
        if numPelis > 0:
            user = users.get_current_user()
            favs = {}
            admin = "no_admin"
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
                "modalText": mensaje,
                "admin": admin,
                "numPelis": numPelis
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(
                jinja.render_template("listFilmsTemplate.html", **susts)
            )


app = webapp2.WSGIApplication([
    ('/seenFilms', seenFilmsHandler)
], debug=True)
