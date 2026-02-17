# 📝 Commandes utiles

## 🔀 Git — Branches

| Commande | Description |
|----------|-------------|
| `git branch` | Lister les branches locales |
| `git branch -a` | Lister toutes les branches (locales + distantes) |
| `git checkout -b nom_branche` | Créer et basculer sur une nouvelle branche |
| `git checkout nom_branche` | Basculer sur une branche existante |
| `git branch -d nom_branche` | Supprimer une branche locale (si mergée) |
| `git branch -D nom_branche` | Forcer la suppression d'une branche locale |
| `git push origin --delete nom_branche` | Supprimer une branche distante |

## 📤 Git — Add, Commit, Push

| Commande | Description |
|----------|-------------|
| `git add .` | Ajouter tous les fichiers modifiés |
| `git commit -m "message"` | Créer un commit avec un message |
| `git push -u origin nom_branche` | Pousser une branche (premier push) |
| `git push` | Pousser les commits sur la branche courante |
| `git pull` | Récupérer les dernières modifications distantes |

## 🔒 Hook pre-push — Protection de la branche main

| Commande | Description |
|----------|-------------|
| `chmod +x .git/hooks/pre-push` | ✅ Activer le hook (bloque le push direct sur main) |
| `chmod -x .git/hooks/pre-push` | ❌ Désactiver le hook (autorise le push sur main) |
| `rm .git/hooks/pre-push` | 🗑️ Supprimer définitivement le hook |

## 🐍 Conda — Environnement

| Commande | Description |
|----------|-------------|
| `conda activate Epsi-Tinho` | Activer l'environnement Epsi-Tinho |
| `conda deactivate` | Désactiver l'environnement courant |
| `conda env list` | Lister tous les environnements conda |
| `conda install nom_package` | Installer un package dans l'environnement actif |

---

*📌 Ce fichier sera enrichi au fur et à mesure du projet.*
