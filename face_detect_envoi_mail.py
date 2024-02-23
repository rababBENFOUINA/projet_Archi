from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import face_recognition
import pickle
import os
import cv2
import numpy as np
import time
import yagmail

# Connexion à la base de données MongoDB
# Remplacez 'mon_uri_de_connexion' par l'URI de connexion de votre base de données MongoDB
#client = pymongo.MongoClient("mongodb://localhost:27017")
connection_string = "mongodb+srv://rabab:rabab2002@archiapp.k4ms9yu.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

# Sélectionnez la base de données à utiliser (dans votre cas, "PrjArchi")
db = client["PrjArchi"]
personne = db["personne"]

def recuperer_email_par_id(utilisateur_id):
    utilisateur = personne.find_one({"_id": utilisateur_id})
    if utilisateur:
        return utilisateur.get("email")
    else:
        return None

def envoyer_email(destinataire, sujet, corps_message):
    smtp_username = "rababbenfina@gmail.com"
    smtp_password = "ovrt ixvt hptt ukjv"

    yag = yagmail.SMTP(smtp_username, smtp_password)
    yag.send(destinataire, sujet, corps_message)
    yag.close()



# Utilisation
################################################################################
output_dir_without_helmet = "C:\\Users\\HP\\Documents\\MIT\\Archi\\projet\\captures_ecran"

# Charger les encodages depuis le fichier
with open("encodings.pkl", "rb") as f:
    encodeListKnown = pickle.load(f)

# Liste pour stocker les IDs sans redondance
unique_ids = set()

# Parcourir les fichiers dans le dossier source
for filename in os.listdir(output_dir_without_helmet):
    img_path = os.path.join(output_dir_without_helmet, filename)

    # Lire une image
    img = cv2.imread(img_path)

    # Vérifier si l'image a été lue correctement
    if img is not None:
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurentFrame = face_recognition.face_locations(imgS)
        encodeCurentFrame = face_recognition.face_encodings(imgS, faceCurentFrame)

        for encodeface, faceLoc in zip(encodeCurentFrame, faceCurentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeface)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeface)

            if True in matches:
                matchIndex = np.argmin(faceDis)
                classNames = ['P1', 'P2', 'P3', 'p4', 'P5', 'P6', 'P7', 'P8', 'P9']
                id = classNames[matchIndex].upper()

                # Ajouter l'ID à la liste des IDs uniques
                unique_ids.add(id)

# Ouvrir le fichier texte en mode écriture
output_file_path = "resultats_detection.txt"
with open(output_file_path, "w") as output_file:
    # Parcourir la liste des IDs uniques et écrire dans le fichier texte
    for id in unique_ids:
        output_file.write(f"Personne sans casque détectée : {id}\n")
        
        # Sélectionnez la collection à utiliser (dans votre cas, "personnes_sans_casque")
        collection = db["personnes_sans_casque"]
        # Enregistrer dans la base de données MongoDB
        collection.insert_one({
            "id": id,
            "chemin_image": img_path,
            "timestamp": time.time()  # Vous pouvez utiliser une horodatage réelle ici
        })
        
###############################################################################
        print(id)
        utilisateur_id = id  # Remplacez par l'ID de l'utilisateur que vous souhaitez
        email_destinataire = recuperer_email_par_id(utilisateur_id)

        personne = db["personne"]
        utilisateur = personne.find_one({"_id": utilisateur_id})
        
        if email_destinataire:
            sujet_email = "Alerte : Détection d'une personne sans casque de sécurité"
            corps_email = """
                        Cher(e) {} {},

                        Nous avons détecté que vous avez été capturé(e) par notre système de surveillance sans porter de casque de sécurité.

                        Détails de la détection :
                        - Identifiant de la personne : [ID de la personne]
                        - Date et heure de la détection : [Date et heure]
                        - Emplacement : [Emplacement]

                        Veuillez prendre les mesures nécessaires pour assurer votre sécurité et vous conformer aux règles de protection en portant un casque approprié dans la zone surveillée.

                        Cordialement
                        """.format(utilisateur.get("nom"),utilisateur.get("prenom"))


            envoyer_email(email_destinataire, sujet_email, corps_email)
            print(f"L'e-mail a été envoyé à {email_destinataire}")
        else:
            print(f"Aucun utilisateur trouvé avec l'ID {utilisateur_id}")
