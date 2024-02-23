import RPi.GPIO as GPIO
import time
import threading

# Importer le module pour exécuter le code en parallèle
from concurrent.futures import ThreadPoolExecutor

# Définir les broches GPIO pour les feux de signalisation
RED_PIN = 17
YELLOW_PIN = 27
GREEN_PIN = 22

# Initialiser la bibliothèque GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

# Fonction pour exécuter le code en parallèle
def run_parallel_code():
    subprocess.run(["python", "autre_code.py"])

def all_lights_off():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)

def traffic_light_cycle():
    try:
        while True:
            # Feu rouge
            GPIO.output(RED_PIN, GPIO.HIGH)
            time.sleep(5)

            # Feu rouge clignotant (transition)
            GPIO.output(RED_PIN, GPIO.LOW)
            time.sleep(1)

            # Feu vert
            GPIO.output(GREEN_PIN, GPIO.HIGH)
            time.sleep(5)

            # Feu vert clignotant (transition)
            GPIO.output(GREEN_PIN, GPIO.LOW)
            time.sleep(1)

            # Feu jaune
            GPIO.output(YELLOW_PIN, GPIO.HIGH)
            time.sleep(3)
            
            # Exécuter le code en parallèle pendant que le feu jaune est allumé
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.submit(run_parallel_code)

            # Feu jaune clignotant (transition)
            GPIO.output(YELLOW_PIN, GPIO.LOW)
            time.sleep(1)

            # Réinitialiser tous les feux
            all_lights_off()

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    traffic_light_cycle()
