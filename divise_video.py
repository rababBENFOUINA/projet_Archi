"""import cv2
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
"""
"""
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

# Charger le classificateur de visage Haarcascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détection des visages dans l'image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    
    # Enregistrer une capture d'écran chaque seconde avec les visages encadrés et une marge
    if frame_count % int(fps) == 0:
        for (x, y, w, h) in faces:
            # Ajouter une marge (par exemple, 10 pixels) autour du visage
            margin = 50
            x_margin = max(0, x - margin)
            y_margin = max(0, y - margin)
            w_margin = w + 2 * margin
            h_margin = h + 2 * margin

            # Extraire l'image du visage avec la marge
            face_image = frame[y_margin:y_margin + h_margin, x_margin:x_margin + w_margin]

            # Enregistrer l'image avec la marge
            output_path = os.path.join(output_folder, f"capture_{frame_count // int(fps)}_face.png")
            cv2.imwrite(output_path, face_image)

    frame_count += 1





# Fermer la vidéo
cap.release()


"""
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

# Charger le classificateur de visage Haarcascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détection des visages dans l'image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    
    # Enregistrer une capture d'écran chaque seconde avec les visages encadrés
    if frame_count % int(fps) == 0:
        for i, (x, y, w, h) in enumerate(faces):
            # Ajouter une marge (par exemple, 10 pixels) autour du visage
            margin = 50
            x_margin = max(0, x - margin)
            y_margin = max(0, y - margin)
            w_margin = w + 2 * margin
            h_margin = h + 2 * margin

            # Extraire l'image du visage avec la marge
            face_image = frame[y_margin:y_margin + h_margin, x_margin:x_margin + w_margin]

            # Enregistrer l'image avec le visage, sans compression
            output_path = os.path.join(output_folder, f"capture_{frame_count // int(fps)}_face_{i}.png")
            cv2.imwrite(output_path, face_image, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

    frame_count += 1

# Fermer la vidéo
cap.release()
