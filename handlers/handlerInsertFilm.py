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
import time
import webapp2
from webapp2_extras import jinja2
from Models.Films import FilmsDB
from Models.SeenFilms import SeemFilmsDB
from google.appengine.api import users
class InsertDataHandler(webapp2.RequestHandler):
    def post(self):
        flag=True
        peliculas = FilmsDB.query()
        numPelis=len(list(peliculas))
        id=numPelis+1
        numPelis = numPelis + 1
        modalText="Se ha insertado la pelicula correctamente"
        try:
            titulo = self.request.get("titulo", "fail")
            director = self.request.get("director", "fail")
            pais = self.request.get("pais", "fail")
            reparto = self.request.get("reparto", "fail")
            sinopsis = self.request.get("sinopsis", "fail")
            link_imagen = self.request.get("link_portada", "fail")
            link_trailer = self.request.get("link_trailer", "fail")
        except:
            modalText="Error: Algo inesperado ha sucedido"
            flag=False
        if flag == True:
            if titulo == 'fail' or director == 'fail' or pais == 'fail' or reparto == 'fail' or sinopsis == 'fail' or link_imagen == 'fail' or link_trailer == 'fail':
                modalText = "Error: Alguno de los parametros es incorrecto"
                flag=False
            if len(titulo) == 0 or len(director) == 0 or len(pais) == 0 or len(reparto) == 0 or len(sinopsis) <100 or len(link_imagen) == 0 or len(link_trailer) == 0:
                modalText = "Error: Alguno de los parametros es incorrecto"
                flag=False

            if 'http://' in link_imagen or 'https://' in link_imagen or 'www.' in link_imagen:
                if '.png' in link_imagen or '.jpg' in link_imagen or '.jpeg' in link_imagen or '.gif' in link_imagen:
                    pass
                else:
                    modalText = "Error: el link de la imagen de portada es incorrecto"
                    flag = False
            else:
                modalText = "Error: el link de la imagen de portada es incorrecto"
                flag = False

            if 'https://www.youtube.com/' in link_trailer:
                pass
            else:
                modalText = "Error: el link del trailer debe ser de YouTube p.ej https://www.youtube.com/embed/VxJ64hB0G_I"
                flag = False





        if flag == True:
            data = FilmsDB(id_pelicula=id,titulo=titulo, director=director, valoracion=0.0, pais=pais, reparto=reparto,
                           sinopsis=sinopsis,link_imagen=link_imagen,link_trailer=link_trailer)
            data.put()
            time.sleep(1)
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
        peliculas = FilmsDB.query()
        susts = {
            "url": url,
            "nickname": nickname,
            "id_user": id_user,
            "favoritos": favs,
            "peliculas": peliculas,
            "modalText": modalText,
            "admin": admin,
            "numPelis": numPelis
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(
            jinja.render_template("listFilmsTemplate.html", **susts)
        )


app = webapp2.WSGIApplication([
    ('/handlerInsertFilm', InsertDataHandler)
], debug=True)
