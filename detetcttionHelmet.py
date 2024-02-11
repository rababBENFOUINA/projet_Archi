from ultralytics import YOLO


# Modèle YOLO pour détecter les objets
model = YOLO("C:\\Users\\HP\\Documents\\MIT\\Archi\\tstCodes\\code_projet_complet\\runs\\detect\\train\\weights\\best.pt")

# Capture des résultats
results = model(source="0", show=True, conf=0.4, save=True)  # Modifier les paramètres selon vos besoins
