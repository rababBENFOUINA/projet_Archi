import cv2
import time

# Définir la durée de la capture en secondes
duree_capture = 10

# Ouvrir la webcam (0 correspond à la webcam par défaut)
cap = cv2.VideoCapture(0)

# Vérifier si la webcam est ouverte correctement
if not cap.isOpened():
    print("Erreur: Impossible d'ouvrir la webcam.")
    exit()

# Définir le codec et créer un objet VideoWriter pour enregistrer la vidéo
codec = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('video_capture.avi', codec, 20.0, (640, 480))

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
