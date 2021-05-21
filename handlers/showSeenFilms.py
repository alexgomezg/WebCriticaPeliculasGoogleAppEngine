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
from Models.SeenFilms import SeemFilmsDB
from google.appengine.api import users
class showSeenFilmsHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        favs = {}
        if user:
            nickname=user.nickname()[0:user.nickname().index("@")]
            id_user=user.user_id()
            url = users.create_logout_url('/')
            favoritos = SeemFilmsDB.query(SeemFilmsDB.id_usuario == float(id_user))
            for fav in favoritos:
                favs[fav.id_pelicula] = "yes"
        else:
            id_user = -1
            nickname="no_logged"
            url = users.create_login_url('/')
        peliculas = FilmsDB.query()
        pelis_pasar=[]
        numPelis=0
        for peli in peliculas:
            if peli.id_pelicula in favs:
                numPelis = numPelis + 1
                pelis_pasar.append(peli)
        susts={
            "url":url,
            "nickname":nickname,
            "id_user":id_user,
            "favoritos":favs,
            "peliculas":pelis_pasar,
            "numPelis":numPelis
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(
            jinja.render_template("listSeenFilmsTemplate.html", **susts)
        )


app = webapp2.WSGIApplication([
    ('/showSeenFilms', showSeenFilmsHandler)
], debug=True)
