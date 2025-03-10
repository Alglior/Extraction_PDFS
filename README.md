Structure des fichiers Python 667 lignes de code

main.py

Classe principale: FastPDFExtractor
Fonction principale: batch_process_pdfs
Objectif: Extraire les pages des PDFs et les convertir en images PNG


convertPNGtoJPG.py

Fonction principale: convert_png_to_jpg
Objectif: Convertir les images PNG extraites en format JPEG


extract_double_image_jpg.py

Classes principales: ImageSplitter
Fonctions: find_doubles_images_folders, process_folder, batch_process_directories
Objectif: Traiter les pages contenant deux images et les diviser


image.py

Classe principale: jpgImageSplitter
Objectif: Traiter les pages avec une seule image


extract_text_from_img_to_xls.py

Fonctions principales: create_excel_file, process_image, extract_text_from_images
Objectif: Extraire le texte des images et l'enregistrer dans un fichier Excel


extract_images_completly.py

Classe principale: ImageContentExtractor
Méthodes: find_image_folders, find_jpg_files, create_extraction_subfolder, extract_image_content
Objectif: Extraire le contenu des images sans le texte


Exécuter main.py pour extraire les pages PDF en PNG
Trier manuellement les images en dossiers: doubles_images, simple_images, plans
Exécuter convertPNGtoJPG.py pour convertir les PNG en JPG
Exécuter extract_double_image_jpg.py pour traiter les images doubles
Exécuter image.py pour les pages avec une seule image
Exécuter extract_text_from_img_to_xls.py pour extraire le texte en Excel
Exécuter extract_images_completly.py pour créer un dossier d'images sans texte