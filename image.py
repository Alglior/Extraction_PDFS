import cv2
import numpy as np
import os
from pathlib import Path
import logging

class jpgImageSplitter:
    def __init__(self, output_dir: str = "split_images"):
        """
        Initialise le séparateur d'images
        """
        self.output_dir = output_dir
        
        # Configuration du logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('image_splitting.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Paramètres pour la détection
        self.min_area = 5000      # Aire minimale pour une image
        self.padding = 10         # Padding autour des images détectées

    def setup_directory(self):
        """
        Crée le dossier de sortie si nécessaire
        """
        os.makedirs(self.output_dir, exist_ok=True)
        self.logger.info(f"Dossier de sortie: {self.output_dir}")

    def detect_and_split_images(self, image_path: str):
        """
        Détecte et extrait les images individuelles d'un fichier jpg
        """
        try:
            # Lecture de l'image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Impossible de lire l'image: {image_path}")

            # Conversion en niveaux de gris
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Application d'un flou pour réduire le bruit
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Détection des bords
            edges = cv2.Canny(blurred, 30, 150)
            
            # Dilatation pour connecter les bords
            kernel = np.ones((5,5), np.uint8)
            dilated = cv2.dilate(edges, kernel, iterations=2)
            
            # Trouver les contours
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filtrer et trier les régions par position verticale
            regions = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > self.min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    # Ajouter du padding
                    x = max(0, x - self.padding)
                    y = max(0, y - self.padding)
                    w = min(img.shape[1] - x, w + 2 * self.padding)
                    h = min(img.shape[0] - y, h + 2 * self.padding)
                    regions.append((y, x, w, h))
            
            # Trier par position verticale
            regions.sort()
            
            # Extraire et sauvegarder chaque région
            base_name = Path(image_path).stem
            for i, (y, x, w, h) in enumerate(regions, 1):
                # Extraire la région
                region = img[y:y+h, x:x+w]
                
                # Sauvegarder l'image
                output_path = os.path.join(self.output_dir, f"{base_name}_image{i}.jpg")
                cv2.imwrite(output_path, region)
                self.logger.info(f"Image extraite: {output_path}")
            
            return len(regions)
            
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement de {image_path}: {e}")
            raise

def main():
    try:
        # Configuration
        input_dir = "jpg_files"  # Dossier contenant les jpg
        output_dir = "split_images"  # Dossier pour les images extraites
        
        # Création du splitter
        splitter = jpgImageSplitter(output_dir)
        splitter.setup_directory()
        
        # Traitement de tous les jpg dans le dossier
        jpg_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.jpg')]
        total_files = len(jpg_files)
        
        print(f"Traitement de {total_files} fichiers jpg...")
        
        for i, jpg_file in enumerate(jpg_files, 1):
            jpg_path = os.path.join(input_dir, jpg_file)
            print(f"Traitement de {jpg_file} ({i}/{total_files})...")
            num_images = splitter.detect_and_split_images(jpg_path)
            print(f"  → {num_images} images extraites")
        
        print("Traitement terminé. Consultez image_splitting.log pour les détails.")
        
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()