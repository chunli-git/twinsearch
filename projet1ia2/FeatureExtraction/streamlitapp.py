import streamlit as st
from distances import retrieve_similar_images
from descriptor import glcm, bitdesc
import numpy as np
import os
import cv2

# ici je charge les signatures
signatures_glcm = np.load('signatures.npy')
signatures_bit = np.load('signaturesBit.npy')

# extraction des caractéristiques en fonction du descripteur que je choisis 
def extract_features(image_path, descriptor):
    if descriptor == 'GLCM':
        return glcm(image_path)
    elif descriptor == 'BiT':
        return bitdesc(image_path)
    else:
        raise ValueError("Descripteur inconnu")


st.title("Alyssia CBIR")

# televerser image
uploaded_file = st.file_uploader("Téléverser une image", type=["jpg", "jpeg", "png"])

# ici je selectionne le nombre d'images similaires à afficher
num_results = st.slider("Nombre d'images similaires à afficher", 1, 20, 10)

# choisir la distance voulue
distance_metric = st.selectbox("Choisir la mesure de distance", ['euclidean', 'manhattan', 'chebyshev', 'canberra'])

# choisi descripteur voulu
descriptor = st.selectbox("Choisir le descripteur", ['GLCM', 'BiT'])

if uploaded_file is not None:
    # sauvegrder l'image télechargée tenporairement
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ici c'est pour extraire les caractéristiques de l'image téléchargée
    try:
        query_features = extract_features("temp_image.jpg", descriptor)
    except Exception as e:
        st.error(f"Erreur lors de l'extraction des caractéristiques de l'image téléchargée: {e}")
        st.stop()

    # selectionner les signatures en fonction du descripteur choisi
    if descriptor == 'GLCM':
        signatures = signatures_glcm
    else:
        signatures = signatures_bit

    # récuperer les images similaires
    try:
        results = retrieve_similar_images(signatures, query_features, distance_metric, num_results)
        paths = [x[0] for x in results]
        labels = [x[2] for x in results]

        # ici je les affiche sinon j'affiche des erreurs
        st.write(f"Images similaires trouvées ({len(paths)} résultats) :")
        for i, img_path in enumerate(paths):
            if os.path.exists(img_path):
                st.image(img_path, caption=f"{labels[i]} - {results[i][1]:.4f}", use_column_width=False)
            else:
                st.warning(f"Fichier non trouvé: {img_path}")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des images similaires: {e}")
