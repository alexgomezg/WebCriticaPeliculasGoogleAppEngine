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
import webapp2
from webapp2_extras import jinja2
from Models.Valorations import ValorationsDB
from google.appengine.api import users
from Models.Films import FilmsDB
class ShowCriticsHandler(webapp2.RequestHandler):
    def get(self):
        pelis = FilmsDB.query()
        pelis_list={}
        for peli in pelis:
            pelis_list[peli.id_pelicula]=peli.titulo
        user = users.get_current_user()
        valoraciones = ValorationsDB.query(ValorationsDB.id_usuario == float(user.user_id()))
        nickname = user.nickname()[0:user.nickname().index("@")]
        url = users.create_logout_url('/')
        susts = {
            "valoraciones": valoraciones,
            "url": url,
            "nickname": nickname,
            "pelis": pelis_list,
            "modalText":"null"
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(
            jinja.render_template("showCriticsTemplate.html", **susts)
        )


app = webapp2.WSGIApplication([
    ('/showCritics', ShowCriticsHandler)
], debug=True)
