import tkinter

from kivy.uix.screenmanager import ScreenManager, FallOutTransition, SlideTransition
from kivymd.uix.boxlayout import MDBoxLayout
import json as js

from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, FallOutTransition, SlideTransition
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.screen import MDScreen
#from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextFieldRound
from kivy.metrics import dp
from kivy.uix.image import Image as Image_kivy
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner
#from kivy.core.camera import CameraBase
from kivy.core.audio import SoundLoader




import cv2
import sqlite3
import  base64
import webbrowser
import os
from PIL import Image as Image_PIL
from tkinter import *
from tkinter import filedialog
import pyttsx3
import sys

#integration de l'algorithme de detection des objets
from yolo_detection import My_Yolo_Detection

#creation de l'instance de detection d'objet
obj_detect = My_Yolo_Detection()




obj = MDApp()

with open("media/file json/file.json") as f:
    data = js.load(f)



#categorie animal
with open("media/file json/file_test_animal.json") as a:
    data_animal = js.load(a)





#categorie sport
with open("media/file json/file_test_sport.json") as s:
    data_sport = js.load(s)






#categorie others
with open("media/file json/file_test_others.json") as o:
    data_others = js.load(o)

sm = ScreenManager()
obj.icon = data["icon"]["avatar6"]


class MyLayout1(ScreenManager):

    # gestion des models via json

    data_model1 = data["model1"]["model_face_detection"]  # model smile

    theme = obj.theme_cls.primary_color
    # accent_theme = obj.theme_cls.accent_color

    # font d'ecran du 2e screen

    data_bg1 = data["bg"]["bg1"]

    data1 = {
        'Accueil': 'human-greeting'
    }

    title_1 = "Instructions"
    title_2 = "ETAPE 1"
    title_3 = "ETAPE 2"

    instructions = """Bienvenue sur Zenia\npour la vision par ordinateur\nchoisisser la prochaine étape\npour la traduction par ordinateur choisisser la 2e étape."""

    etape_1 = """La vision par ordinateur nous permettra de communiquer avec le systeme par flux vidéos\npour débuter, valider le boutton Computer traduction du sous menu."""

    etape_2 = """La traduction par ordinateur nous permettra de communiquer avec le systeme par écrit\npour débuter, valider le boutton Computer vision du sous menu."""

    data_target = data["image"]["avatar1"]
    data_target4 = data["image3"]["avatar4"]
    data_target3 = data["image4"]["avatar5"]
    data_target5 = data["image2"]["avatar3"]
    data_target6 = data["image6"]["avatar8"]
    data_target7 = data["image5"]["avatar7"]
    data_target8 = data["image7"]["avatar9"]
    # data_target9 = data["image8"]["avatar10"]
    data_target10 = data["image9"]["avatar11"]
    data_target11 = data["image10"]["avatar12"]



    myListname = []
    mylistfile = []





    def __init__(self, **Kwargs):
        super(MyLayout1, self).__init__(**Kwargs)


        self.dialog1 = None
        self.dialog2 = None
        self.dialog3 = None
        self.dialog_alert = None
        self.camera_obj = None
        self.a = ["Vision par ordinateur", "Traduction par ordinateur",
                  "Récuperer les données", "Fermer la Webcam", "Quitter l'application", ]
        self.capture = cv2.VideoCapture(0)


    def process_load_image(self, id_spinner, id_load_db):
        sound_intro = SoundLoader.load('media/sound/zenia voice analyse.wav')
        if sound_intro:
            sound_intro.play()
        id_spinner.active = False
        state_loader = True
        
        while state_loader:



            self.load_image()
            state_loader = False




        id_load_db.icon = "check-bold"
        toast("Chargement terminé")

            






    def load_image(self):
        default_name_animal = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11"]
        default_name_sport = ["s1", "s2", "s3", "s4", "s5", "s6", "s7"]
        default_name_other = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8",
                              "o9", "o10", "o11", "o12", "o13", "o14", "o15",
                              "o16", "o17", "o18", "o19", "o20", "o21",
                              "o22", "o23", "o24", "o25", "o26", "o27"]

        # insertion des images test de categorie animal

        for i in range(0, 10):
            self.insert_file_image_animal(default_name_animal[i],
                                            data_animal["file_test" + str(i)]["file" + str(i)])

        # insertion des images test de categorie others

        for j in range(0, 6):
            self.insert_file_image_sport(default_name_sport[j], data_sport["sport" + str(j)]["s" + str(j)])

        # insertion des images test de categorie sport

        for k in range(0, 26):
            self.insert_file_image_others(default_name_other[k], data_others["other" + str(k)]["o" + str(k)])






    def insert_file_image_others(self, name, file):
        try:
            entity_db = sqlite3.connect("media/ZENIA_VISION.db")
            entity_cursor = entity_db.cursor()
            entity_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS Image_others(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,    
                    name TEXT,
                    file BLOB NOT NULL
                    )



                """
            )
            entity_db.commit()
            sql1 = "INSERT INTO Image_others(name, file) VALUES(?, ?)"

            # convertir le fichier au format binaire
            with open(file, 'rb') as myfile:
                blobfile = myfile.read()

            value = (name, blobfile)
            entity_cursor.execute(sql1, value)
            entity_db.commit()


        except Exception as E:
            print(f"erreur de type-->{E}")
            entity_db.rollback()

        finally:
            entity_db.close()








    def insert_file_image_sport(self, name, file):
        try:
            entity_db = sqlite3.connect("media/ZENIA_VISION.db")
            entity_cursor = entity_db.cursor()
            entity_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS Image_sport(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,    
                    name TEXT,
                    file BLOB NOT NULL
                    )



                """
            )
            entity_db.commit()
            sql1 = "INSERT INTO Image_sport(name, file) VALUES(?, ?)"

            # convertir le fichier au format binaire
            with open(file, 'rb') as myfile:
                blobfile = myfile.read()

            value = (name, blobfile)
            entity_cursor.execute(sql1, value)
            entity_db.commit()


        except Exception as E:
            print(f"erreur de type-->{E}")
            entity_db.rollback()

        finally:
            entity_db.close()











    def insert_file_image_animal(self, name, file):
        try:
            entity_db = sqlite3.connect("media/ZENIA_VISION.db")
            entity_cursor = entity_db.cursor()
            entity_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS Image_animal(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,    
                    name TEXT,
                    file BLOB NOT NULL
                    )



                """
            )
            entity_db.commit()
            sql1 =  "INSERT INTO Image_animal(name, file) VALUES(?, ?)"


            #convertir le fichier au format binaire
            with open(file, 'rb') as myfile:
                blobfile = myfile.read()

            value = (name, blobfile)
            entity_cursor.execute(sql1, value)
            entity_db.commit()


        except Exception as E:
            print(f"erreur de type-->{E}")
            entity_db.rollback()

        finally:
            entity_db.close()





    def speak(self, text_write):
        engine_voice = pyttsx3.init('sapi5')
        list_service = ["Vous avez validé les services youtube, vous serez redirigé vers le site youtube.com",
                             "Vous avez validé les services de messagerie vous serez renvoyé vers le support google",
                             "vous avez validé les services facebook, vous serez renvoyer vers le site facebook.com",
                             "vous avez validé les services twitter, vous serez renvoyé vers le site twitter.com",
                             "vous voulez ouvrir un fichier pour le traiter, vous serez renvoyé vers l'explorateur de fichier"]
        if "youtube" in text_write:
            engine_voice.say(list_service[0])
            engine_voice.runAndWait()
            toast("Lancement de la plateforme youtube")
            path_youtube = "https://www.youtube.com"
            webbrowser.open_new(path_youtube)


        elif "mail" in text_write:
            engine_voice.say(list_service[1])
            engine_voice.runAndWait()
            toast("Lancement de la plateforme de message électronique")
            path_mail = "https://mail.google.com"
            webbrowser.open_new(path_mail)

        elif "facebook" in text_write:
            engine_voice.say(list_service[2])
            engine_voice.runAndWait()
            toast("Lancement de la plateforme facebook")
            path_facebook = "https://facebook.com"
            webbrowser.open_new(path_facebook)

        elif "twitter" in text_write:
            engine_voice.say(list_service[3])
            engine_voice.runAndWait()
            toast("Lancement de la plateforme twitter")
            path_twitter = "https://twitter.com"
            webbrowser.open_new(path_twitter)

        elif "pdf" or "word" or "excel" or "classeur" or "text" or "fichier" in text_write:
            engine_voice.say(list_service[4])
            engine_voice.runAndWait()
            toast("Ouverture de l'explorateur de fichier...")
            fen = Tk()
            fen.title("Recherche de documents...")
            fen.geometry("500x1+50+100")
            fen.resizable(width=False, height=False)
            i1 = tkinter.PhotoImage(file="media/img/new zenia logo.png")
            fen.iconphoto(False, i1)

            file = filedialog.askopenfilename(initialdir="/",
                                                         title="Sélectionner le fichier",
                                                         filetypes=(("Fichier Texte", "*.txt"),
                                                                    ("Fichier pdf", "*.pdf"),
                                                                    ("Fichier Word", "*.docx"),
                                                                    ("Fichier Excel", "*.xlsx"),
                                                                    ("Tous les fichiers", "*.*")
                                                                    ))
            toast(file)
            os.popen(file)
            fen.mainloop()
            sys.exit(0)

        else:
            engine_voice.say("désolé nous ne gérons pas ce type de service pour le moment")
            engine_voice.runAndWait()








    def open_form(self, id_float_speech, id_float_img_speech):
        toast("Initiation du formulaire...")
        sound_intro = SoundLoader.load('media/sound/zenia voice analyse.wav')
        if sound_intro:
            sound_intro.play()

        anim_layout_speech = Animation(duration=.2, opacity=0, pos_hint={"center_x": .1, "center_y": .1}, size=(dp(1), dp(1)))

        anim_layout_speech.start(id_float_img_speech)


        anim_layout_speech = Animation(duration=.2, opacity=1)
        anim_layout_speech += Animation(duration=.5, opacity=1,
                                          size=(dp(2 * 300), dp(2 * 200)), pos_hint={"center_x": .5, "center_y": .5})
        anim_layout_speech.start(id_float_speech)


    def open_list_animal(self):
        sound_intro = SoundLoader.load('media/sound/zenia_animaux-mc..wav')
        if sound_intro:
            sound_intro.play()
        fen = Tk()
        fen.title("ZENIA EXPLORATION DE FICHIER CATEGORIE ANIMAL")
        fen.geometry("500x1+50+100")
        fen.resizable(width=False, height=False)
        i1 = tkinter.PhotoImage(file="media/img/new zenia logo.png")
        fen.iconphoto(False, i1)

        filename_animal = filedialog.askopenfilename(initialdir = "media/recovery_data/animal",
                                                     title = "Categorie animal",
                                                     filetypes = (("Image files", "*.png"),
                                                                  ))
        print(filename_animal)
        obj_detect.detect_(filename_animal)

        fen.mainloop()
        sys.exit(0)







    def open_list_sport(self):
        sound_intro = SoundLoader.load('media/sound/zenia_sport-mc..wav')
        if sound_intro:
            sound_intro.play()
        fen = Tk()
        fen.title("ZENIA EXPLORATION DE FICHIER CATEGORIE SPORT")
        fen.geometry("500x1+50+100")
        fen.resizable(width=False, height=False)
        i1 = tkinter.PhotoImage(file="media/img/new zenia logo.png")
        fen.iconphoto(False, i1)

        filename_sport = filedialog.askopenfilename(initialdir = "media/recovery_data/sport",
                                                     title = "Categorie sport",
                                                     filetypes = (("Image files", "*.png"),
                                                                  ))
        print(filename_sport)
        obj_detect.detect_(filename_sport)
        fen.mainloop()
        sys.exit(0)




    def open_list_others(self):

        fen = Tk()
        fen.title("ZENIA EXPLORATION DE FICHIER CATEGORIE OTHERS")
        fen.geometry("500x1+50+100")
        fen.resizable(width=False, height=False)
        i1 = tkinter.PhotoImage(file="media/img/new zenia logo.png")
        fen.iconphoto(False, i1)

        filename_other = filedialog.askopenfilename(initialdir = "media/recovery_data/other",
                                                     title = "Categorie other",
                                                     filetypes = (("Image files", "*.png"),
                                                                  ))
        print(filename_other)
        obj_detect.detect_(filename_other)
        fen.mainloop()
        sys.exit(0)









    def on_start_camera_race(self):

        Clock.schedule_once(self.load_time_camera1, 5)


    def load_time_camera1(self, dt):
        sound_intro = SoundLoader.load('media/sound/zenia voice valider.wav')
        if sound_intro:
            sound_intro.play()
        self.ids.sm2.transition = SlideTransition(duration=.8, direction='right')
        self.ids.sm2.current = self.ids.id_screen_screen_load_time_camera.name


        id_screen_camera = self.ids.id_screen_camera


        self.open_camera_race(id_screen_camera)





    def open_camera_race(self, id_screen_camera):
        sound_intro = SoundLoader.load('media/sound/zenia voice fin registred.wav')
        if sound_intro:
            sound_intro.play()

        self.ids.sm2.transition = SlideTransition(duration=.8, direction='left')
        self.ids.sm2.current = self.ids.id_screen_camera.name


        anim_screen_camera = Animation(opacity=0, duration=1, size=(1, 1), pos_hint={"center_x": .5, "center_y": .4})
        anim_screen_camera += Animation(opacity=1, duration=1, size=(10, 10), pos_hint={"center_x": .5, "center_y": .4})
        anim_screen_camera += Animation(opacity=1, duration=1, size=(20, 20),
                                        pos_hint={"center_x": .99, "center_y": .4})
        anim_screen_camera += Animation(opacity=1, duration=1, size=(30, 30),
                                        pos_hint={"center_x": .05, "center_y": .4})
        anim_screen_camera += Animation(opacity=1, duration=1, size=(40, 40), pos_hint={"center_x": .5, "center_y": .4})
        anim_screen_camera += Animation(opacity=1, duration=1, size=(500, 250 * 2),
                                        pos_hint={"center_x": .5, "center_y": .3})
        anim_screen_camera.start(id_screen_camera)
        layout_camera1 = self.ids.id_boxlayout_camera1




        self.image = Image_kivy(
            pos_hint = {"center_x": .8, "center_y": .5},
            size_hint = (None, None),
            size = (500, 500)
        )
        self.label = MDLabel(text = "Detection faciale",
                             theme_text_color = "Custom",
                             halign = "center",
                             text_color = [0, 162/255, 232/255, .67])

        layout_camera1.add_widget(self.image)
        layout_camera1.add_widget(self.label)






        self.face_smile = cv2.CascadeClassifier(self.data_model1)

        self.count = 0


        Clock.schedule_interval(self.load_video_for_race, 1.0/60.0)








    def load_video_for_race(self, dt):

            ret, frame = self.capture.read()

            #initialisation du frame

            self.image_frame = frame
            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            smile = self.face_smile.detectMultiScale(color_frame, 1.1, 4)
            text = "Detection Faciale-ZENIA"

            #initialisation du rectangle
            for (x, y, w,h) in smile:
                cv2.rectangle(color_frame, (x, y), (x+w, y+h), ( 255, 0, 0), 2)
                cv2.putText(color_frame,text, (x, y + 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 1, 0), 2)
            buffer = cv2.flip(color_frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='luminance')
            texture.blit_buffer(buffer, colorfmt='luminance', bufferfmt='ubyte')
            self.image.texture = texture
            cv2.waitKey(0)




    def exit_webcam(self):
        sound_intro = SoundLoader.load('media/sound/zenia voice clic.wav')
        if sound_intro:
            sound_intro.play()
        layout_camera1 = self.ids.id_boxlayout_camera1
        layout_camera1.remove_widget(self.image)
        layout_camera1.remove_widget(self.label)

        layout_camera1.opacity = 0
        sys.quit(0)











    def finish_callback(self):
        sound_intro = SoundLoader.load('media/sound/zenia voice clic.wav')
        if sound_intro:
            sound_intro.play()
        self.open_instruction()



    def call_activities(self):
        sound_intro = SoundLoader.load('media/sound/zenia voice clic.wav')
        if sound_intro:
            sound_intro.play()

        i = 0
        activities = "ouverture des activités"

        menu_items = [
            {

                "text": f"{self.a[i]}",
                "viewclass": "OneLineListItem",
                "height": 60,
                "on_release": lambda x=f"{i}": self.menu_callback(x),

            } for i in range(len(self.a))

        ]

        self.menu = MDDropdownMenu(
            # header_cls = Menu_header(),
            caller=self.ids.id_button_call_activities,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

        return toast(activities)

    def menu_callback(self, text_item):
        n1 = self.ids.number1
        n2 = self.ids.number2

        if text_item == str(0):
            self.open_number1(n1, n2)

        elif text_item == str(1):
            self.open_number2(n1, n2)

        elif text_item == str(2):
            self.recovery_data()

        elif text_item == str(3):
            self.exit_webcam()

        elif text_item == str(4):
            obj.stop()


        else:
            toast("erreur lors de la selection des activités")


    def callback(self, instance):
        sound_intro = SoundLoader.load('media/sound/zenia voice intro.wav')
        if sound_intro:
            sound_intro.play()
        self.transition = FallOutTransition(duration=1)
        self.current = "second"


    def recovery_data(self):
        sound_intro = SoundLoader.load('media/sound/zenia voice recovery data.wav')
        if sound_intro:
            sound_intro.play()
        toast(" traitement et récupération des données chargées dans la base de données...")
        self.get_data_animal()
        self.get_data_sport()
        self.get_data_others()





    def get_data_animal(self):
        try:
            entity_db = sqlite3.connect("media/ZENIA_VISION.db")
            entity_cursor = entity_db.cursor()

            sql = "SELECT * from Image_animal"
            entity_cursor.execute(sql)
            entity_db.commit()
            result_list_animal = entity_cursor.fetchall()

            for colon_animal in result_list_animal:

                name = colon_animal[1]
                file = colon_animal[2]


                path_animal = "media/recovery_data/animal\\" + name + ".png"
                path_folder = "media/recovery_data/animal"

                #conversion du fichier binaire en fichier png
                with open(path_animal, 'wb') as file_animal:
                    file_animal.write(file)


                #redimensionnement des images de type animal avec la même echelle
                f = path_folder
                new_dimension_width = 500 #largeur de notre nouvelle image
                new_dimension_height = 300 #hauteur de notre nouvelle image

                for f_ile in os.listdir(f):
                    f_image = f+'/'+f_ile
                    try:
                        img = Image_PIL.open(f_image)
                        img = img.resize((new_dimension_width, new_dimension_height))
                        img.save(f_image)
                    except IOError as IOE:
                        print(f"erreur de type: '{IOE}")





        except Exception as E:
            print(f"Erreur de type:{E}")

        finally:
            entity_db.close()






    def get_data_others(self):
        try:
            entity_db = sqlite3.connect("media/ZENIA_VISION.db")
            entity_cursor = entity_db.cursor()

            sql = "SELECT * from Image_others"
            entity_cursor.execute(sql)
            entity_db.commit()
            result_list_others = entity_cursor.fetchall()

            for colon_others in result_list_others:

                name = colon_others[1]
                file = colon_others[2]

                path_others = "media/recovery_data/other\\" + name + ".png"
                path_folder = "media/recovery_data/other"

                #conversion du fichier binaire en fichier png
                with open(path_others, 'wb') as file_others:
                    file_others.write(file)

                # redimensionnement des images de type others avec la même echelle
                f = path_folder
                new_dimension_width = 500  # largeur de notre nouvelle image
                new_dimension_height = 300  # hauteur de notre nouvelle image
                for f_ile in os.listdir(f):
                    f_image = f + '/' + f_ile
                    try:
                        img = Image_PIL.open(f_image)
                        img = img.resize((new_dimension_width, new_dimension_height))
                        img.save(f_image)
                    except IOError as IOE:
                        print(f"erreur de type: '{IOE}")


        except Exception as E:
            print(f"Erreur de type:{E}")

        finally:
            entity_db.close()







    def get_data_sport(self):
        try:
            entity_db = sqlite3.connect("media/ZENIA_VISION.db")
            entity_cursor = entity_db.cursor()

            sql = "SELECT * from Image_sport"
            entity_cursor.execute(sql)
            entity_db.commit()
            result_list_sport = entity_cursor.fetchall()

            for colon_sport in result_list_sport:

                name = colon_sport[1]
                file = colon_sport[2]

                path_sport = "media/recovery_data/sport\\" + name + ".png"
                path_folder = "media/recovery_data/sport"

                #conversion du fichier binaire en fichier png
                with open(path_sport, 'wb') as file_sport:
                    file_sport.write(file)

                # redimensionnement des images de type sport avec la même echelle
                f = path_folder
                new_dimension_width = 500  # largeur de notre nouvelle image
                new_dimension_height = 300  # hauteur de notre nouvelle image
                for f_ile in os.listdir(f):
                    f_image = f + '/' + f_ile
                    try:
                        img = Image_PIL.open(f_image)
                        img = img.resize((new_dimension_width, new_dimension_height))
                        img.save(f_image)
                    except IOError as IOE:
                        print(f"erreur de type: '{IOE}")

        except Exception as E:
            print(f"Erreur de type:{E}")

        finally:
            entity_db.close()









    def open_number1(self, number1, number2):
        sound_intro = SoundLoader.load('media/sound/zenia voice clic.wav')
        if sound_intro:
            sound_intro.play()

        self.ids.sm2.transition = SlideTransition(duration=.8, direction='left')
        self.ids.sm2.current = self.ids.number1.name
        t1 = self.a[0]

        anim_number1 = Animation(opacity=0, duration=1, size=(10, 10), pos_hint={"center_x": .5, "center_y": .4})
        anim_number1 += Animation(opacity=1, duration=1, size=(10, 10), pos_hint={"center_x": .5, "center_y": .4})
        anim_number1 += Animation(opacity=1, duration=1, size=(10, 10), pos_hint={"center_x": .99, "center_y": .4})
        anim_number1 += Animation(opacity=1, duration=1, size=(10, 10), pos_hint={"center_x": .05, "center_y": .4})
        anim_number1 += Animation(opacity=1, duration=1, size=(10, 10), pos_hint={"center_x": .5, "center_y": .4})
        anim_number1 += Animation(opacity=1, duration=1, size=(150 * 2, 70 * 3),
                                  pos_hint={"center_x": .5, "center_y": .3})
        anim_number1.start(number1)

        anim_number2 = Animation(opacity=0)
        anim_number2.start(number2)

        return toast(t1)

    def open_instruction(self, id_layout_register_user, id_float_speech):
        sound_intro = SoundLoader.load('media/sound/zenia voice clic.wav')
        if sound_intro:
            sound_intro.play()
        anim_layout_register = Animation(duration=.2, opacity=1)
        anim_layout_register += Animation(duration=.5, opacity=0,
                                          size=(dp(1), dp(1)), pos_hint={"center_x": .5, "center_y": .35})
        anim_layout_register.start(id_layout_register_user)

        anim_layout_register = Animation(duration=.2, opacity=1)
        anim_layout_register += Animation(duration=.5, opacity=0,
                                          size=(dp(1), dp(1)), pos_hint={"center_x": .5, "center_y": .35})
        anim_layout_register.start(id_float_speech)

        self.ids.sm2.transition = SlideTransition(duration=.8, direction='up')
        self.ids.sm2.current = "instruction"


    def open_number2(self, number1, number2, id_float_img_speech):
        sound_intro = SoundLoader.load('media/sound/zenia voice clic.wav')
        if sound_intro:
            sound_intro.play()

        self.ids.sm2.transition = SlideTransition(duration=.8, direction='right')
        self.ids.sm2.current = self.ids.number2.name
        t2 = self.a[1]

        anim_number2 = Animation(opacity=1, duration=1)
        anim_number2.start(id_float_img_speech)

        anim_number2 = Animation(opacity=0, duration=1, size=(10, 10), pos_hint={"center_x": .5, "center_y": .4})
        anim_number2 += Animation(opacity=1, duration=1, size=(10, 10), pos_hint={"center_x": .5, "center_y": .4})
        anim_number2 += Animation(opacity=1, duration=1, size=(10, 10), pos_hint={"center_x": .99, "center_y": .4})
        anim_number2 += Animation(opacity=1, duration=1, size=(10, 10), pos_hint={"center_x": .05, "center_y": .4})
        anim_number2 += Animation(opacity=1, duration=1, size=(10, 10), pos_hint={"center_x": .5, "center_y": .4})
        anim_number2 += Animation(opacity=1, duration=1, size=(150 * 2, 150 * 2),
                                  pos_hint={"center_x": .5, "center_y": .3})
        anim_number2.start(number2)

        anim_number1 = Animation(opacity=0)
        anim_number1.start(number1)

        return toast(t2)

    def call_screen_onboarding(self):
        self.ids.sm2.transition = SlideTransition(duration=.8, direction="up")
        self.ids.sm2.current = "screen_onboarding"


    def call_name_user(self, id_layout_register_user):
        sound_intro = SoundLoader.load('media/sound/zenia voice analyse.wav')
        if sound_intro:
            sound_intro.play()
        anim_layout_register = Animation(duration = .2, opacity = 1)
        anim_layout_register += Animation(duration = .5, opacity = 1,
                                          size = (dp(2*300), dp(2*200)), pos_hint = {"center_x": .5, "center_y": .35})
        anim_layout_register.start(id_layout_register_user)





    def print_name_user(self, user):
        sound_intro = SoundLoader.load('media/sound/zenia voice fin registred.wav')
        if sound_intro:
            sound_intro.play()
        if user == "":
            if not self.dialog_alert:
                self.dialog_alert = MDDialog(
                    title="Aucune Donnée enregistrée, veuillez remplir le champs",
                    buttons=[
                        MDIconButton(
                            icon="alert",
                            theme_text_color="Custom",
                            text_color=(1, 201/255, 14/255, .8),
                            user_font_size="90sp",
                            pos_hint={"center_x": .5, "center_y": .5}
                        ),
                        MDFlatButton(
                            text="                                                  ",

                        ),
                    ],
                )

            self.dialog_alert.open()

        else:
            mysnackbar = Snackbar(
                text= \
                    f"[color=#ddbb23] Validation D'accès!!!,   [/color], [color=#ffffff]{user.upper()}[/color]",

                snackbar_y="10dp",
                snackbar_x="100dp",

            )
            mysnackbar.size_hint_x = (
                                             Window.width - (mysnackbar.snackbar_x * 2)
                                     ) / Window.width
            mysnackbar.buttons = [
                MDIconButton(
                    icon="checkbox-marked",
                    theme_text_color="Custom",
                    text_color=(34 / 255, 177 / 255, 76 / 255, .8),
                    on_release=mysnackbar.dismiss,
                ),
            ]
            mysnackbar.open()

            #encryptage des données d'utilisateurs
            E = My_encrypt_data()
            user_encrypt = E.encrypt(user)


            if not self.dialog_alert:
                self.dialog_alert = MDDialog(
                    title="                      processus d'encryptage des données...",
                    buttons=[
                        MDIconButton(
                            icon="briefcase-upload",
                            theme_text_color="Custom",
                            text_color=(34 / 255, 177 / 255, 76 / 255, .8),
                            user_font_size="90sp",
                            pos_hint={"center_x": .5, "center_y": .5}
                        ),
                        MDFlatButton(
                            text="                                                    ",

                        ),
                ],
                )
                self.dialog_alert.open()


            self.insert_name_user(user_encrypt)






    def insert_name_user(self, user=""):
        try:
            entity_db = sqlite3.connect("media/ZENIA_VISION.db")
            entity_cursor = entity_db.cursor()
            entity_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS User_table(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,    
                    user TEXT)

                    

                """
            )
            entity_db.commit()

            table_db1 = (user,)

            entity_cursor.execute("""
                        INSERT INTO User_table(user) VALUES(?)""", table_db1

                                  )
            entity_db.commit()


        except Exception as E:
            print(f"erreur de type-->{E}")
            entity_db.rollback()

        finally:
            entity_db.close()


class ContentNavigationDrawer(MDBoxLayout):
    data_target1 = data["image1"]["avatar2"]
    data_target = data["image"]["avatar1"]
    data_target3 = data["image4"]["avatar5"]

    def open_dialog_star(self):
        pass


class Windows_menu(MDScreen):
    dialog_info = None

    def save_star_and_nameUser(self):
        star_valide = "Etoile(s) validee(s)"
        star_test = self.ids.id_akrating_star.get_rate()

        toast(str(star_test) + " " + star_valide)
        self.save_database_(str(star_test))



    def save_database_(self,star=""):
        sound_intro = SoundLoader.load('media/sound/zenia voice fin registred.wav')
        if sound_intro:
            sound_intro.play()
        try:
            entity_db = sqlite3.connect("media/ZENIA_VISION.db")
            entity_cursor = entity_db.cursor()
            entity_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS Star_table(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,    
                    star TEXT)
                   
                    
                    
                """
            )
            entity_db.commit()

            table_db2 = (star)

            entity_cursor.execute("""
                        INSERT INTO Star_table(star) VALUES(?)""", table_db2

            

                                )
            entity_db.commit()


        except Exception as E:
            print(f"erreur de type-->{E}")
            entity_db.rollback()

        finally:
            entity_db.close()




    def show_theme(self):
        sound_intro = SoundLoader.load('media/sound/zenia voice clic.wav')
        if sound_intro:
            sound_intro.play()
        theme = MDThemePicker()
        theme.open()



    def call_share_page(self):
        sound_intro = SoundLoader.load('media/sound/zenia voice clic.wav')
        if sound_intro:
            sound_intro.play()
        bs = MDGridBottomSheet()
        data = {
            "Github": "github",
            "Youtube": "youtube",
            "Cloud": "apple-icloud"

        }
        for item in data.items():
            bs.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1]


            )
            bs.open()
        return toast("Partage de l'application")



    def callback_for_menu_items(self, y):
        if y == "Github":
            self.get_url_github()

        elif y == "Youtube":
            self.get_url_youtube_channel()


        elif y == "Cloud":
            self.get_url_gmail_cloud()




    def get_url_github(self):
        path_1 = "https://github.com/ZenDkakukaio/Zenia-vision-demo/"
        webbrowser.open_new(path_1)


    def get_url_youtube_channel(self):
        path_2 = "https://www.youtube.com/channel/UCeB2pGU0eG77iEhqKSqgkkg"
        webbrowser.open_new(path_2)


    def get_url_twitter(self):
        path_3 = "https://twitter.com/home"
        webbrowser.open_new(path_3)







    def call_info_app(self):
        sound_intro = SoundLoader.load('media/sound/zenia voice clic.wav')
        if sound_intro:
            sound_intro.play()
        t_info1 = """ZENIA est une application qui implémente: ¤la communication par vision, ¤la communication par écrit.
                                                    
                                                                 
                                                                  
                       
                                                    Version: Beta\n
                                         contact: Daryl21emani07@gmail.com
            
        """
        t_infos2 = "                                           A propos"

        if not self.dialog_info:
            self.dialog_info = MDDialog(
                title=t_infos2,
                text=t_info1,

            )
        self.dialog_info.open()




#classe d'encryptage des données
class My_encrypt_data(object):
    DIE = 128
    KEY = (7, 3, 55)

    def __init__(self):
        pass

    def encryptChar(self, char):
        k1, k2, kI = self.KEY
        return chr((k1 * ord(char) + k2) % self.DIE)


    def encrypt(self, string):
        return "".join(map(self.encryptChar, string))


    def decryotchar(self, char):
        k1, k2, kI = self.KEY
        return chr(kI * (ord(char) - k2) % self.DIE)


    def decrypt(self, string):
        return "".join(map(self.decryotchar, string))





class Myspinner(MDSpinner):
    pass



