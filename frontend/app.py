import streamlit as st

st.set_page_config(
    page_title="Job Intelligent App",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Job Intelligent App")
st.subheader("Trouvez les offres d'emploi qui correspondent à votre profil")

st.markdown("---")
st.info("📄 Uploadez votre CV et laissez l'IA trouver les meilleures offres pour vous.")

# Zone d'upload du CV (à compléter)
uploaded_file = st.file_uploader(
    "Déposez votre CV ici",
    type=["pdf", "docx"],
    help="Formats acceptés : PDF, DOCX"
)

if uploaded_file is not None:
    st.success(f"✅ Fichier '{uploaded_file.name}' uploadé avec succès !")
    st.write("🔄 Analyse en cours... (fonctionnalité à venir)")
else:
    st.write("👆 En attente de votre CV...")
