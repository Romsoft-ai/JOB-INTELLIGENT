document.getElementById('upload-btn').addEventListener('click', async function() {
    const fileInput = document.getElementById('cv-upload');
    const statusDiv = document.getElementById('upload-status');
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    if (!fileInput.files.length) {
        statusDiv.textContent = 'Veuillez sélectionner un fichier.';
        statusDiv.style.color = 'red';
        return;
    }
    const file = fileInput.files[0];
    statusDiv.textContent = 'Envoi du fichier...';
    statusDiv.style.color = '#008000';
    const formData = new FormData();
    formData.append('file', file);
    try {
        // Remplacer l'URL par celle de votre API FastAPI
        const response = await fetch('http://127.0.0.1:8001/upload-cv', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            const data = await response.json();
            statusDiv.textContent = 'Fichier uploadé avec succès !';
            resultsDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        } else {
            statusDiv.textContent = "Erreur lors de l'upload.";
            statusDiv.style.color = 'red';
        }
    } catch (error) {
        statusDiv.textContent = "Erreur de connexion à l'API.";
        statusDiv.style.color = 'red';
    }
});
