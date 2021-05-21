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
class InsertDataHandler(webapp2.RequestHandler):
    def get(self):
        data = FilmsDB(id_pelicula=1,titulo="La daronne", director="Christopher Nolan", valoracion=0.0, pais="Francia", reparto="Isabelle Huppert, Hippolyte Girardot",
                       sinopsis="Patience Portefeux es una traductora especializada en escuchas telefonicas para la brigada de estupefacientes de Paris. Es un trabajo precario y mal pagado. Un dia, Patience se dispone a hacer un favor al problematico hijo de una mujer y acaba involucrada en un trapicheo de drogas fallido, lo que le deja con una pila de cannabis en su posesion. Mientras mantiene su trabajo en la brigada anti-droga, Patience cruza al otro lado y se convierte en camello.",
                       link_imagen="https://i.imgur.com/p6MD8n4.jpg",link_trailer="https://www.youtube.com/embed/VxJ64hB0G_I")
        data.put()
        data = FilmsDB(id_pelicula=2,titulo="Train to busan", director="Manolito Perez", valoracion=0.0, pais="Corea del Sur",
                       reparto="Isabelle Huppert, Hippolyte Girardot",
                       sinopsis="Cuatro meses despues de la epidemia zombi, Corea sigue infestada de monstruos y el soldado Jung-seok, que escapo del pais, se ve obligado a regresar a Seul para recuperar un objeto valioso. Alli descubre que hay, todavia, personas sanas en la ciudad.",
                       link_imagen="https://i.imgur.com/qFOEPXO.jpg",link_trailer="https://www.youtube.com/embed/roKEPJJRqVk")
        data.put()
        data = FilmsDB(id_pelicula=3,titulo="Nobody", director="Pedro Invento", valoracion=0.0, pais="Estados Unidos",
                      reparto="Isabelle Huppert, Hippolyte Girardot",
                      sinopsis="Hutcg Mansel es un hombre de familia corriente pero un inesperado robo hara que su vida cambie para siempre, tendra que demostrarle a su familia lo valiente y buen heroe americano que es",
                       link_imagen="https://i.imgur.com/A8HqQDv.jpg",link_trailer="https://www.youtube.com/embed/SNFcflvJ90M")
        data.put()
        data = FilmsDB(id_pelicula=4, titulo="Chaos Walking", director="Doug Liman", valoracion=0.0, pais="Estados Unidos",
                       reparto="Daisy Ridley, Tom Holland, Mads Mikkelsen, Demian Bichir, David Oyelowo, Kurt Sutter, Nick Jonas, Oscar Jaenada",
                       sinopsis="En Prentisstown,Tod ha crecido creyendo que la Masila fue la responsable de liberar un germen que asesino a todas las mujeres y contagio con el ruido al resto de los hombres. Tras descubrir un remanso de silencio en un pantano, sus padres adoptivos le obligan a huir lo mas rapido que pueda, dejando todo atras salvo un mapa del Nuevo Mundo y un mensaje, asi como un sinfin de preguntas sin responder.",
                       link_imagen="https://i.imgur.com/seqkP1a.jpg",link_trailer="https://www.youtube.com/embed/KJOd3poTq_I")
        data.put()
        data = FilmsDB(id_pelicula=5, titulo="Great White", director="Martin Wilson", valoracion=0.0,
                       pais="Estados Unidos",
                       reparto="Katrina Bowden, Aaron Jakubenko, Tim Kano, Kimie Tsukakoshi, Te Kohe Tuhaka, Tatjana Alexis, Jason Wilder, Patrick Atchison",
                       sinopsis="Una escapada en hidroavion a la Gran Barrera de Coral australiana se convierte en una pesadilla para un grupo de jovenes cuando son atacados por un gigantesco tiburon blanco. Varado en alta mar sobre un fragil bote salvavidas, el grupo tendra que usar todo su ingenio para resistir a la monstruosa amenaza que les acecha bajo el agua.",
                       link_imagen="https://i.imgur.com/0eS5HQK.jpg",link_trailer="https://www.youtube.com/embed/aknWfAczkZA")
        data.put()
        data = FilmsDB(id_pelicula=6, titulo="Things Heard & Seen", director="Shari Springer Berman, Robert Pulcini", valoracion=0.0,
                       pais="Estados Unidos",
                       reparto="Amanda Seyfried, James Norton, Karen Allen, F. Murray Abraham, Natalia Dyer, Rhea Seehorn, Alex Neustaedter, Jack Gore, Olivia Boreham-Wing, Kelcy Griffin, Emily Dorsch",
                       sinopsis="Una pareja de Manhattan se muda a una aldea historica en el valle del Hudson y acaba descubriendo que su matrimonio oculta una siniestra oscuridad que rivaliza con la historia de su nuevo hogar.",
                       link_imagen="https://i.imgur.com/VKn7sWI.jpg",link_trailer="https://www.youtube.com/embed/HCAaonjgDEA")
        data.put()
        data = FilmsDB(id_pelicula=7, titulo="Star Wars Batch", director="Steward Lee", valoracion=0.0,
                       pais="Estados Unidos",
                       reparto="Personajes de animacion 3D",
                       sinopsis="Los clones de La Remesa Mala se encuentran en una galaxia cambiante tras las Guerras Clon. En este episodio el imperio intentara relanzar su ataque",
                       link_imagen="https://i.imgur.com/2OIHq6y.jpg",link_trailer="https://www.youtube.com/embed/BsOmYpP4UDU")
        data.put()
        time.sleep(1)
        self.redirect('/')



app = webapp2.WSGIApplication([
    ('/insertDataDB', InsertDataHandler)
], debug=True)
