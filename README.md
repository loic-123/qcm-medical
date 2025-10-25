# 🏥 QCM Médical - Application EDN

Application web intelligente pour générer des **QCM type EDN** depuis vos cours de médecine, propulsée par **Claude Haiku 4.5**.

## 🎯 Fonctionnalités

### ✨ Génération Intelligente
- 📄 **Upload Word/PDF** : Glissez-déposez vos cours (texte + images)
- 🤖 **IA Médicale** : 10 questions pertinentes générées automatiquement
- 📚 **Format EDN** : Réponses multiples possibles (format officiel)
- 🎓 **Niveau DFASM** : Questions adaptées 5e année de médecine

### 💡 Apprentissage Interactif
- ✅ **Feedback immédiat** : Explication détaillée après chaque question
- 📊 **Récapitulatif personnalisé** : Analyse de vos forces et faiblesses
- 🔄 **Régénération** : Créez plusieurs QCM depuis le même cours

### 📥 Export Professionnel
- 📄 **PDF vierge** : Pour s'entraîner
- 📗 **PDF avec corrigé** : Pour réviser
- 📊 **PDF de résultats** : Votre performance détaillée

---

## 🚀 Installation

### 1. Prérequis
- Python 3.9 ou supérieur
- Un compte Anthropic avec accès API

### 2. Cloner/Télécharger le projet

```bash
# Si vous avez git
git clone <url-du-repo>
cd qcm-medical

# Sinon, téléchargez et décompressez le dossier
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de la clé API

**Option A : Via l'interface Streamlit (Recommandé)**
- Pas besoin de fichier .env
- Entrez directement votre clé API dans l'interface

**Option B : Via fichier .env (Optionnel)**
```bash
# Copier le fichier exemple
cp .env.example .env

# Éditer avec votre clé
nano .env  # ou utilisez votre éditeur préféré
```

### 5. Obtenir votre clé API Anthropic

1. Créez un compte sur [console.anthropic.com](https://console.anthropic.com/)
2. Allez dans **Settings** → **API Keys**
3. Cliquez sur **Create Key**
4. Copiez votre clé (commence par `sk-ant-`)

⚠️ **Important** : Gardez votre clé secrète !

---

## 💻 Utilisation Locale

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à `http://localhost:8501`

### Workflow complet

1. **📤 Onglet "Upload & Génération"**
   - Entrez votre clé API dans la barre latérale
   - Glissez-déposez un fichier Word (.docx) ou PDF
   - Cliquez sur "🚀 Générer le QCM"
   - Attendez 30-60 secondes

2. **📝 Onglet "QCM Interactif"**
   - Lisez chaque question
   - Cochez **toutes** les bonnes réponses (plusieurs possibles)
   - Cliquez sur "✅ Valider ma réponse"
   - Lisez le feedback détaillé de Claude
   - Passez à la question suivante

3. **📊 Onglet "Résultats"**
   - Consultez votre score global
   - Lisez le récapitulatif personnalisé
   - Exportez en PDF (3 versions disponibles)
   - Régénérez un nouveau QCM si souhaité

---

## ☁️ Déploiement sur Streamlit Cloud

### Étape 1 : Préparer votre code

1. Créez un compte GitHub (si pas déjà fait)
2. Créez un nouveau repository public
3. Uploadez tous les fichiers **SAUF** :
   - ❌ `.env` (contient votre clé API)
   - ❌ `__pycache__` et autres fichiers temporaires

```bash
# Exemple avec git
git init
git add .
git commit -m "Initial commit"
git remote add origin <votre-url-github>
git push -u origin main
```

### Étape 2 : Déployer sur Streamlit Cloud

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez-vous avec votre compte GitHub
3. Cliquez sur **New app**
4. Sélectionnez :
   - **Repository** : votre repo GitHub
   - **Branch** : main (ou master)
   - **Main file path** : `app.py`
5. Cliquez sur **Deploy**

### Étape 3 : Configuration (IMPORTANT !)

⚠️ **NE METTEZ PAS votre clé API dans le code !**

**Option 1 : Saisie directe (Recommandé pour 1 utilisateur)**
- L'utilisateur entre sa clé API directement dans l'interface
- Pas de configuration supplémentaire nécessaire

**Option 2 : Secrets Streamlit (Pour partager l'app)**
1. Dans Streamlit Cloud, allez dans **Settings** → **Secrets**
2. Ajoutez :
```toml
ANTHROPIC_API_KEY = "sk-ant-votre-cle-ici"
```
3. Modifiez `app.py` pour lire ce secret :
```python
# Dans la fonction main(), remplacez la ligne api_key par :
api_key = st.secrets.get("ANTHROPIC_API_KEY", "") or st.text_input(...)
```

### Étape 4 : Partager l'application

Une fois déployée, vous obtenez une URL comme :
```
https://votre-app-qcm-medical.streamlit.app
```

Partagez cette URL avec votre copine ! 🎉

---

## 📁 Structure du Projet

```
qcm-medical/
├── app.py                    # 🎯 Application principale
├── requirements.txt          # 📦 Dépendances Python
├── .env.example             # 🔑 Exemple configuration
├── README.md                # 📖 Ce fichier
└── utils/
    ├── __init__.py
    ├── document_parser.py   # 📄 Extraction Word/PDF
    ├── claude_api.py        # 🤖 Gestion API Claude
    └── pdf_export.py        # 📥 Export PDF
```

---

## 💰 Coûts Estimés

Avec **Claude Haiku 4.5** (modèle le plus économique) :

- **Input** : $0.80 / million de tokens (~$0.0008 / 1000 tokens)
- **Output** : $4.00 / million de tokens (~$0.004 / 1000 tokens)

**Estimation par session :**
- Upload d'un cours de 5000 mots + 2 images : ~8000 tokens input
- Génération de 10 questions : ~3000 tokens output
- Feedback + récapitulatif : ~2000 tokens output

**Total ≈ $0.03 par session complète** (moins de 3 centimes)

💡 **Très économique pour un usage personnel !**

---

## 🛠️ Dépannage

### Problème : "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Problème : "Invalid API key"
- Vérifiez que votre clé commence par `sk-ant-`
- Créez une nouvelle clé sur console.anthropic.com
- Vérifiez que vous avez des crédits API

### Problème : "Erreur extraction PDF"
```bash
pip install PyMuPDF --upgrade
```

### Problème : Génération lente
- Normal ! La génération prend 30-60 secondes
- C'est le temps nécessaire à Claude pour analyser et générer des questions de qualité

### Problème : Questions en anglais
- Claude peut parfois générer en anglais
- Ajoutez "Génère en français" dans le prompt système (ligne 32 de `claude_api.py`)

---

## 🎨 Personnalisation

### Modifier le nombre de questions

Dans `claude_api.py`, ligne 28, changez :
```python
"Ton rôle est de créer des QCM de haute qualité..."
# Remplacez "Exactement 10 questions" par le nombre souhaité
```

Et dans `app.py`, ligne 136, adaptez le texte d'interface.

### Modifier le nombre de propositions

Dans `claude_api.py`, ligne 30 :
```python
# Changez "4 à 5 propositions" par "3 à 6 propositions" (par exemple)
```

### Changer le modèle Claude

Dans `claude_api.py`, ligne 19 :
```python
self.model = "claude-haiku-4-20250514"  # Haiku 4.5 (économique)
# Alternatives :
# self.model = "claude-sonnet-4-20250514"  # Sonnet 4 (plus performant mais plus cher)
# self.model = "claude-opus-4-20250514"    # Opus 4 (le meilleur mais coûteux)
```

---

## 🤝 Support

### Ressources utiles
- [Documentation Claude](https://docs.anthropic.com/)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Forum Streamlit](https://discuss.streamlit.io/)

### Questions fréquentes

**Q : Puis-je utiliser l'app hors ligne ?**
R : Non, elle nécessite une connexion internet pour l'API Claude.

**Q : Les données sont-elles sauvegardées ?**
R : Non, tout est en mémoire. Exportez en PDF pour conserver vos résultats.

**Q : Combien d'utilisateurs peuvent l'utiliser ?**
R : Sur Streamlit Cloud gratuit : illimité, mais ressources partagées. Pour un usage intensif, envisagez un plan payant.

**Q : Les images sont-elles analysées ?**
R : Oui ! Claude utilise les images comme contexte pour générer des questions pertinentes.

---

## 📜 Licence

Ce projet est fourni tel quel pour un usage personnel ou éducatif.

---

## 🎉 Bon courage pour les EDN !

Créé avec ❤️ pour faciliter les révisions médicales.

N'hésitez pas à adapter l'application selon vos besoins ! 🚀
#   m e d _ q u e s t i o n s  
 