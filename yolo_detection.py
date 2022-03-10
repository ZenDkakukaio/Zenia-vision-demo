import cv2
import numpy as np



class My_Yolo_Detection(object):
    def __init__(self):
        pass

    def detect_(self, path_file):

        # charger les donnees de yolo4
        net = cv2.dnn.readNetFromDarknet('yolo_detection/yolov4.cfg', 'yolo_detection/yolov4.weights')

        # charger les noms des differentes couches
        ln = net.getLayerNames()

        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

        print("chargement...\n")

        DEFAULT_CONFIDANCE = .5  # niveau de confiance(probalite de confiance)
        TRHESOLD = .4  # seuil de detection des mauvaises zones

        # chargement des noms de labels contenu dans le fichier coco.name avec lesquels Yolov4 a ete entrainé
        with open('yolo_detection/coco.names', 'r') as f:
            LABELS = f.read().splitlines()



        image = cv2.imread(path_file)
        name_app = 'Detection objet ZENIA...'

        while True:



            height, width, _ = image.shape  # recuperation des cordonnees de l'image(hauteur et largeur)

            # traitement de l'image
            blob = cv2.dnn.blobFromImage(image, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

            """
                echelle de traitement, on divise notre image en pixel de 1 par 255
                on utilise une taille normalisee de 416 par 416
                application d'aucune moyenne au image (0,0,0)
                convertion des images en rgb swapRB =True
                defiinir la coupure des images a false crop = False
        
        
            """

            # passage des flux d'image au reseaux
            net.setInput(blob)

            # passage des noms des couches prepaprees plus haut
            layerOutputs = net.forward(ln)

            boxes = []  # parametre qui contiendra les differents zones detectees sur l'image
            confidences = []  # parametre qui contiendra les niveau de confiance pour chacune des zones detectées
            classIDs = []  # parametre qui contiendra les labels predits pour l'ensemble des zones detectee

            # on parcoure chacune des couches ayant ete detectees
            for output in layerOutputs:
                for detection in output:  # et pour chacune des couches detectee on recupere les objets detectee
                    scores = detection[5:]
                    classID = np.argmax(scores)  # on recupere l'ID de l'objet ayant ete detecté
                    confidence = scores[classID]  # on recupere la probabilite avec laquelle cet objet a ete detecte

                    if confidence > DEFAULT_CONFIDANCE:  # si la probabilite est superieure au niveau de confiance
                        # on peut effectuer le traitement

                        """
                            on recupere les cordonnees de l'objet detecte
                        """
                        box = detection[0:4] * np.array([width, height, width, height])
                        (centerX, centerY, W, H) = box.astype("int")

                        """
                            en fonction des cordonnees calculees on recupere la position des bordures de la zone detectee
                        """
                        x = int(centerX - (W / 2))
                        y = int(centerX - (H / 2))

                        """
                            on rajoute ces donnees retrouvee dans les objets detectes : boxes
                        """

                        boxes.append([x, y, int(W), int(H)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)

            # on supprime les mauvaises detections detectees plus haut grace a la methode NMSBoxes
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, DEFAULT_CONFIDANCE, TRHESOLD)

            # on definit une liste de couleur utilisee pour definir nos boxes
            COLORS = np.random.uniform(0, 255, size=(len(boxes), 3))

            # on se rassure avoir detecte aumoins un objet
            if len(indexes) > 0:
                for i in indexes.flatten():  # parcour de tous les elements detectes dans nos indexes
                    (x, y, w, h) = boxes[i]  # on extrait les cordonnees de la zone
                    color = COLORS[i]

                    # on renvoie un text au dessus du rectangle constitue du label ou obet detecte et de la probabilite
                    # de detection de cette objet

                    text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])

                    # ensuite on dessine un rectangle de detection
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(image, text, (x, y + 20), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

            # on affiche l'image
            cv2.imshow(name_app, image)

            # pour quitter l'execution du code l'utilisateur devra entrer q sur son clavier

            cv2.waitKey(0)

            # ensuite on libere les ressources
            # image.release()
            cv2.destroyAllWindows()
