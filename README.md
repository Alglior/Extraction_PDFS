# Kit d'extraction PDF2Data

Ce dépôt contient une boîte à outils complète pour extraire et traiter des données à partir de documents PDF, particulièrement orientée vers la gestion de documents contenant des images et du texte qui doivent être séparés et traités individuellement.

## Aperçu

PDF2Data est une boîte à outils Python modulaire qui permet :
- L'extraction de pages PDF sous forme d'images
- La conversion de formats d'image
- La détection et la division des pages contenant plusieurs images
- L'extraction de texte à partir d'images vers Excel
- L'extraction propre du contenu des images (sans texte)

La boîte à outils comprend 667 lignes de code réparties sur plusieurs modules Python, chacun gérant une partie spécifique du pipeline d'extraction.

## Modules

### `main.py`
- **Classe principale** : `FastPDFExtractor`
- **Fonction principale** : `batch_process_pdfs()`
- **Objectif** : Extraire les pages des fichiers PDF et les convertir au format PNG

### `convertPNGtoJPG.py`
- **Fonction principale** : `convert_png_to_jpg()`
- **Objectif** : Convertir les images PNG extraites au format JPEG pour un traitement ultérieur

### `extract_double_image_jpg.py`
- **Classe principale** : `ImageSplitter`
- **Fonctions clés** : 
  - `find_doubles_images_folders()`
  - `process_folder()`
  - `batch_process_directories()`
- **Objectif** : Traiter les pages contenant deux images et les diviser en fichiers séparés

### `image.py`
- **Classe principale** : `jpgImageSplitter`
- **Objectif** : Traiter les pages contenant une seule image

### `extract_text_from_img_to_xls.py`
- **Fonctions principales** : 
  - `create_excel_file()`
  - `process_image()`
  - `extract_text_from_images()`
- **Objectif** : Extraire le contenu textuel des images et l'enregistrer dans des fichiers Excel

### `extract_images_completly.py`
- **Classe principale** : `ImageContentExtractor`
- **Méthodes clés** :
  - `find_image_folders()`
  - `find_jpg_files()`
  - `create_extraction_subfolder()`
  - `extract_image_content()`
- **Objectif** : Extraire le contenu visuel des images en supprimant les éléments textuels

## Flux de travail

1. Exécuter `main.py` pour extraire les pages PDF sous forme d'images PNG
2. Trier manuellement les images dans des dossiers :
   - `doubles_images` : Pages avec plusieurs images
   - `simple_images` : Pages avec une seule image
   - `plans` : Pages avec des diagrammes ou des dessins
3. Exécuter `convertPNGtoJPG.py` pour convertir tous les fichiers PNG au format JPG
4. Exécuter `extract_double_image_jpg.py` pour traiter et diviser les pages contenant plusieurs images
5. Exécuter `image.py` pour traiter les pages avec une seule image
6. Exécuter `extract_text_from_img_to_xls.py` pour extraire le contenu textuel dans des fichiers Excel
7. Exécuter `extract_images_completly.py` pour créer un dossier d'images sans texte

## Prérequis

- Python 3.x
- Diverses bibliothèques de traitement d'images (voir `requirements.txt`)
- Capacités OCR pour l'extraction de texte
