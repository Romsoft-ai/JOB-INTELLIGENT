import streamlit as st
from PIL import Image
import os
import requests

st.set_page_config(
    page_title="Job Intelligent App",
    page_icon="🎯",
    layout="wide"
)

# Affichage du logo
logo_path = os.path.join(os.path.dirname(__file__), '../logo/logo1.png')
logo = Image.open(logo_path)
st.image(logo, width=180)

st.title("🎯 Job Intelligent App")

# Description de l'application
st.markdown("""
<div style='font-size:1.1em; margin-bottom: 1.5em;'>
    <b>Job Intelligent App</b> est une application intelligente de matching CV / Offres d'emploi en France.<br>
    <ul>
        <li><b>Upload</b> : Déposez votre CV sur la plateforme</li>
        <li><b>Analyse intelligente</b> : Extraction et compréhension de vos compétences, expériences et formations</li>
        <li><b>Matching en temps réel</b> : Recherche et classement des offres d'emploi les plus pertinentes</li>
        <li><b>Résultats personnalisés</b> : Visualisez les offres qui correspondent à votre profil</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.info("📄 Uploadez votre CV et laissez l'IA trouver les meilleures offres pour vous.")

# Zone principale divisée en deux colonnes sans cadre
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    uploaded_file = st.file_uploader(
        "Déposez votre CV ici",
        type=["pdf", "docx"],
        help="Formats acceptés : PDF, DOCX",
        label_visibility="visible"
    )
    # Champ de saisie des mots-clés
    user_keywords = st.text_input(
        "Entrez vos mots-clés pour la recherche d'offres (ex: data analyst, développeur python, chef de projet)",
        value="",
        help="Vous pouvez entrer un ou plusieurs mots-clés séparés par des virgules."
    )
    if uploaded_file is not None:
        st.success(f"✅ Fichier '{uploaded_file.name}' uploadé avec succès !")
        st.markdown(f"<div style='margin:18px 0;'><b>CV sélectionné :</b><br><span style='display:inline-block; margin-top:8px;'><img src='https://img.icons8.com/ios-filled/50/2b4162/document--v1.png' width='32' style='vertical-align:middle; margin-right:8px;'/> {uploaded_file.name}</span></div>", unsafe_allow_html=True)
        # Envoi du fichier à FastAPI
        with st.spinner('Envoi du CV au serveur...'):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            try:
                response = requests.post("http://127.0.0.1:8001/upload-cv", files=files)
                if response.status_code == 200:
                    st.success("Fichier transmis au backend et sauvegardé avec succès !")
                    st.json(response.json())
                else:
                    st.error(f"Erreur lors de l'envoi au backend : {response.status_code}")
            except Exception as e:
                st.error(f"Erreur de connexion au backend : {e}")
        # Affichage du PDF si c'est un PDF
        if uploaded_file.name.lower().endswith('.pdf'):
            import base64
            pdf_bytes = uploaded_file.read()
            b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f"""
            <iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="350" type="application/pdf"></iframe>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.info("Aperçu disponible uniquement pour les fichiers PDF.")
        st.write("🔄 Analyse en cours... (fonctionnalité à venir)")
    else:
        st.write("👆 En attente de votre CV...")

    # Bouton pour lancer la recherche d'offres avec les mots-clés
    if uploaded_file is not None and user_keywords:
        if st.button("Rechercher des offres avec ces mots-clés"):
            with st.spinner('Recherche des offres en cours...'):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                data = {"keywords": user_keywords}
                try:
                    response = requests.post(
                        "http://127.0.0.1:8001/upload-cv-and-search",
                        files=files,
                        data=data
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.success("Offres récupérées avec succès !")
                        st.write("Mots-clés extraits du CV :", result.get("cv_keywords"))
                        st.write("Mots-clés utilisateur :", result.get("user_keywords"))
                        offres = result.get("offers", [])
                        if offres:
                            st.subheader("Offres trouvées :")
                            for offre in offres:
                                st.write(offre)
                        else:
                            st.info("Aucune offre trouvée avec ces mots-clés.")
                    else:
                        st.error(f"Erreur lors de la recherche d'offres : {response.status_code}")
                except Exception as e:
                    st.error(f"Erreur de connexion au backend : {e}")
    elif user_keywords and not uploaded_file:
        st.warning("Veuillez d'abord uploader un CV avant de lancer la recherche.")
    elif uploaded_file and not user_keywords:
        st.warning("Veuillez entrer des mots-clés pour lancer la recherche.")

with col2:
    st.subheader("Classement des offres d'emploi")
    offres = [
        {"titre": "Développeur Python", "pourcentage": 92},
        {"titre": "Data Scientist", "pourcentage": 85},
        {"titre": "Ingénieur Logiciel", "pourcentage": 78},
        {"titre": "Chef de projet IT", "pourcentage": 65},
    ]
    if uploaded_file is not None:
        for offre in offres:
            st.markdown(f"<div style='margin-bottom:18px;'><b>{offre['titre']}</b> <span style='float:right; color:#2b4162; font-weight:bold;'>{offre['pourcentage']}%</span><div style='background:#e0e7ef; border-radius:6px; height:12px; width:100%;'><div style='background:#2b4162; width:{offre['pourcentage']}%; height:12px; border-radius:6px;'></div></div></div>", unsafe_allow_html=True)
    else:
        st.info("Le classement des offres apparaîtra ici après l'upload de votre CV.")
