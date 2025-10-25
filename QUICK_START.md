# 🚀 Guide de Démarrage Rapide

## Pour utilisateurs Windows

### 1️⃣ Installation (5 minutes)

```cmd
# Ouvrir PowerShell ou CMD dans le dossier du projet

# Installer les dépendances
pip install -r requirements.txt

# Tester l'installation
python test_installation.py
```

### 2️⃣ Lancement

```cmd
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur !

---

## Pour utilisateurs Mac/Linux

### 1️⃣ Installation (5 minutes)

```bash
# Ouvrir Terminal dans le dossier du projet

# (Optionnel) Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# Installer les dépendances
pip install -r requirements.txt

# Tester l'installation
python test_installation.py
```

### 2️⃣ Lancement

```bash
streamlit run app.py
```

---

## 🔑 Configuration de la clé API

### Obtenir votre clé API Anthropic

1. **Créer un compte** : [console.anthropic.com](https://console.anthropic.com/)
2. **Ajouter des crédits** : $5 minimum (suffisant pour des centaines de QCM)
3. **Générer une clé** : Settings → API Keys → Create Key
4. **Copier la clé** : Elle commence par `sk-ant-`

### Utiliser la clé dans l'application

**Option simple** : Entrez directement dans l'interface Streamlit
- Ouvrez l'application
- Dans la barre latérale, collez votre clé API
- ✅ Prêt !

---

## 📝 Utilisation en 3 étapes

### Étape 1 : Upload
- Onglet "📤 Upload & Génération"
- Glissez-déposez un fichier Word ou PDF
- Cliquez "🚀 Générer le QCM"
- ⏳ Attendez 30-60 secondes

### Étape 2 : Répondre
- Onglet "📝 QCM Interactif"
- Lisez chaque question
- Cochez **toutes** les bonnes réponses
- Validez et lisez le feedback

### Étape 3 : Réviser
- Onglet "📊 Résultats"
- Consultez votre score
- Lisez le récapitulatif personnalisé
- Exportez en PDF

---

## 💡 Conseils

### Pour de meilleurs QCM
- ✅ Cours bien structurés (titres, paragraphes)
- ✅ Contenu substantiel (>500 mots)
- ✅ Images de qualité (schémas, tableaux)
- ❌ Éviter les cours trop courts (<200 mots)

### Économiser des tokens
- 📄 Un seul cours à la fois
- 🖼️ Images essentielles uniquement (max 5)
- 🔄 Régénérez plutôt que re-upload

---

## 🆘 Problèmes courants

| Problème | Solution |
|----------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "Invalid API key" | Vérifiez votre clé sur console.anthropic.com |
| Génération lente | Normal ! 30-60s pour 10 questions de qualité |
| Questions en anglais | Vérifiez que votre cours est en français |
| PDF non supporté | Certains PDF scannés ne fonctionnent pas (OCR nécessaire) |

---

## ☁️ Déploiement Express sur Streamlit Cloud

1. **GitHub** : Créez un repo et uploadez le code
2. **Streamlit Cloud** : [share.streamlit.io](https://share.streamlit.io) → New app
3. **Sélectionnez** : votre repo, branch main, fichier app.py
4. **Deploy** : Cliquez et attendez 2-3 minutes
5. **Partagez** : L'URL générée est accessible partout !

⚠️ **N'oubliez pas** : Ne mettez JAMAIS votre clé API dans le code public !

---

## 📞 Besoin d'aide ?

- 📖 Consultez le `README.md` complet
- 🧪 Lancez `python test_installation.py`
- 💬 [Documentation Claude](https://docs.anthropic.com/)
- 📚 [Forum Streamlit](https://discuss.streamlit.io/)

---

Bonne chance pour les révisions ! 🎓✨
