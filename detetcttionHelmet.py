from ultralytics import YOLO
from ultralytics.engine.results import Results

import os
import shutil

# Modèle YOLO pour détecter les objets
model = YOLO("C:\\Users\\HP\\Documents\\MIT\\Archi\\tstCodes\\code_projet_complet\\runs\\detect\\train\\weights\\best.pt")

# Dossiers de sortie
output_dir_with_helmet = "C:\\Users\\HP\\Documents\\MIT\\Archi\\projet\\images_avec_casque"
output_dir_without_helmet = "C:\\Users\\HP\\Documents\\MIT\\Archi\\projet\\images_sans_casque"

# Création des répertoires s'ils n'existent pas
os.makedirs(output_dir_with_helmet, exist_ok=True)
os.makedirs(output_dir_without_helmet, exist_ok=True)

# Dossier source
source_dir = "C:\\Users\\HP\\Documents\\MIT\\Archi\\projet\\captures_ecran"

# Parcourir les images dans le dossier source
for filename in os.listdir(source_dir):
    img_path = os.path.join(source_dir, filename)

    # Détecter les objets dans l'image
    results_list = model(img_path, conf=0.4)
    
    # Supposez que 'results' est votre objet Results

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
            else:
                # Si 'Helmet' est détecté, copier l'image dans le répertoire avec casque
                shutil.copy(img_path, output_dir_with_helmet)
        else:
            print("Aucune boîte détectée pour l'image :", img_path)
