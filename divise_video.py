import cv2
import os
import shutil

# Chemin vers la vidéo
video_path = "C:\\Users\\HP\\Documents\\MIT\\Archi\\projet\\video_capture.avi"

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

    # Enregistrer une capture d'écran chaque seconde (ajustez selon vos besoins)
    if frame_count % int(fps) == 0:
        output_path = os.path.join(output_folder, f"capture_{frame_count // int(fps)}.png")
        cv2.imwrite(output_path, frame)

    frame_count += 1

# Fermer la vidéo
cap.release()
