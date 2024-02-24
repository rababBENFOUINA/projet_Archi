# Importation des bibliothèques nécessaires
import cv2  # Bibliothèque OpenCV pour la vision par ordinateur
import time  # Module pour gérer le temps dans le script
import os  # Module pour interagir avec le système d'exploitation
import shutil  # Module pour manipuler des fichiers et des répertoires
from ultralytics import YOLO  # Importation du modèle YOLO pour la détection d'objets
import numpy as np  # Bibliothèque pour les opérations mathématiques et numériques
import face_recognition  # Bibliothèque de reconnaissance faciale
import pickle  # Module pour sérialiser et désérialiser des objets Python
from pymongo import MongoClient  # Importation du client MongoDB pour la base de données
import yagmail  # Bibliothèque pour l'envoi de courriels

# Connexion à la base de données MongoDB
#client = pymongo.MongoClient("mongodb://localhost:27017")
connection_string = "mongodb+srv://rabab:rabab2002@archiapp.k4ms9yu.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

# Sélectionnez la base de données à utiliser
db = client["PrjArchi"]


# Définir la durée de la capture en secondes
duree_capture = 10

# Ouvrir la webcam (0 correspond à la webcam par défaut)
cap = cv2.VideoCapture(0)

# Vérifier si la webcam est ouverte correctement
if not cap.isOpened():
    print("Erreur: Impossible d'ouvrir la webcam.")
    exit()

# Spécifier le chemin  du fichier vidéo
nom_video = 'video_capture.avi'
chemin_video = nom_video

# Définir le codec et créer un objet VideoWriter pour enregistrer la vidéo
codec = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter(chemin_video, codec, 20.0, (640, 480))

# Capture de la vidéo pendant la durée spécifiée
debut_capture = time.time()
while time.time() - debut_capture < duree_capture:
    # Lire une image de la webcam
    ret, frame = cap.read()

    # Vérifier si la lecture de l'image a réussi
    if not ret:
        print("Erreur: Impossible de lire l'image de la webcam.")
        break

    # Afficher l'image en direct (facultatif)
    cv2.imshow('Video Capture', frame)

    # Écrire l'image dans la vidéo de sortie
    output.write(frame)

    # Attendre 1 milliseconde et vérifier si l'utilisateur a appuyé sur la touche 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
output.release()
cv2.destroyAllWindows()


#################################################################################
##########################    division video   ##################################
# Chemin vers la vidéo
video_path = "video_capture.avi"

# Créer un dossier pour enregistrer les captures d'écran
output_folder = 'captures_ecran'
os.makedirs(output_folder, exist_ok=True)

# Vider le contenu du répertoire "captures_ecran" s'il n'est pas vide
if os.listdir(output_folder):
    shutil.rmtree(output_folder)
    os.makedirs(output_folder)

# Ouvrir la vidéo
cap = cv2.VideoCapture(video_path)

# Obtenir la fréquence d'images par seconde (FPS) de la vidéo
fps = cap.get(cv2.CAP_PROP_FPS)

# Lire les images une par une
frame_count = 0
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Enregistrer une capture d'écran chaque seconde 
    if frame_count % int(fps) == 0:
        output_path = os.path.join(output_folder, f"capture_{frame_count // int(fps)}.png")
        cv2.imwrite(output_path, frame)

    frame_count += 1

# Fermer la vidéo
cap.release()


#################################################################################
##########################  detection helemt   ##################################

# Modèle YOLO pour détecter les objets
model = YOLO("best.pt")

# Dossiers de sortie
output_dir_with_helmet = "images_avec_casque"
output_dir_without_helmet = "images_sans_casque"

# Nettoyer le répertoire 'images_avec_casque'
shutil.rmtree(output_dir_with_helmet, ignore_errors=True)
os.makedirs(output_dir_with_helmet, exist_ok=True)

# Nettoyer le répertoire 'images_sans_casque'
shutil.rmtree(output_dir_without_helmet, ignore_errors=True)
os.makedirs(output_dir_without_helmet, exist_ok=True)


# Dossier source
source_dir = "captures_ecran"

# Parcourir les images dans le dossier source
for filename in os.listdir(source_dir):
    img_path = os.path.join(source_dir, filename)

    # Détecter les objets dans l'image
    results_list = model(img_path, conf=0.4)
    

    # Parcourir la liste des résultats pour chaque image
    for results in results_list:
        # Assurez-vous que la liste des boîtes est présente dans les résultats
        if hasattr(results, 'boxes'):
            # Récupérer les noms des classes
            class_names = results.names

            # Obtenez les indices des classes détectées dans l'image
            indices_classes_detectees = results.boxes.cls
            indices_classes_detectees = indices_classes_detectees.numpy()
            print(indices_classes_detectees)
            
            # Initialiser class_name en dehors de la condition
            class_name = None
            
            if len(indices_classes_detectees) > 0:
                # Obtenez le nom de la classe à partir de l'indice
                class_index = int(indices_classes_detectees[0])
                class_name = class_names[class_index]

                # Utilisez le nom de la classe selon vos besoins
                print("Nom de la classe :", class_name)
            else:
                print("Aucune classe détectée dans cette image.")


            # Vérifier si la classe 'Helmet' est présente dans les résultats
            if 'NoHelmet' == class_name:
                # Si 'Helmet' n'est pas détecté, copier l'image dans le répertoire sans casque
                shutil.copy(img_path, output_dir_without_helmet)
            elif 'Helmet' == class_name:
                # Si 'Helmet' est détecté, copier l'image dans le répertoire avec casque
                shutil.copy(img_path, output_dir_with_helmet)
        else:
            print("Aucune boîte détectée pour l'image :", img_path)

################################################################################################
##########################  identifier personne sans casque   ##################################
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



################################################################################

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
