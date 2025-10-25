# 🏥 QCM Médical EDN

> Application web intelligente pour générer des **QCM type EDN** depuis vos cours de médecine, propulsée par **Claude Haiku 4.5**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table des Matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Déploiement](#️-déploiement-sur-streamlit-cloud)
- [Structure du Projet](#-structure-du-projet)
- [Coûts](#-coûts-estimés)
- [Personnalisation](#-personnalisation)
- [Support](#-support)

---

## ✨ Fonctionnalités

### 🎯 Génération Intelligente

- **📄 Upload Word/PDF** : Glissez-déposez vos cours (texte + images)
- **🤖 IA Médicale** : 10 questions pertinentes générées automatiquement
- **📚 Format EDN** : Réponses multiples possibles (format officiel)
- **🎓 Niveau DFASM** : Questions adaptées 5e année de médecine

### 💡 Apprentissage Interactif

- **✅ Feedback immédiat** : Explication détaillée après chaque question
- **📊 Récapitulatif personnalisé** : Analyse de vos forces et faiblesses
- **🔄 Régénération** : Créez plusieurs QCM depuis le même cours

### 📥 Export Professionnel

- **📄 PDF vierge** : Pour s'entraîner
- **📗 PDF avec corrigé** : Pour réviser
- **📊 PDF de résultats** : Votre performance détaillée

---

## 🚀 Installation

### Prérequis

- Python 3.9 ou supérieur
- Un compte Anthropic avec accès API

### Étapes

1. **Cloner le repository**

```bash
git clone https://github.com/loic-123/qcm-medical.git
cd qcm-medical
```

2. **Créer un environnement virtuel** (recommandé)

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Obtenir votre clé API Anthropic**

- Créez un compte sur [console.anthropic.com](https://console.anthropic.com/)
- Allez dans **Settings** → **API Keys**
- Créez une clé (commence par `sk-ant-`)

> ⚠️ **Important** : Ne partagez jamais votre clé API !

---

## 💻 Utilisation

### Lancement

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement à `http://localhost:8501`

### Workflow

#### 1️⃣ Upload & Génération

- Entrez votre clé API dans la barre latérale
- Glissez-déposez un fichier Word (.docx) ou PDF
- Cliquez sur **🚀 Générer le QCM**
- Attendez 30-60 secondes

#### 2️⃣ QCM Interactif

- Lisez chaque question
- Cochez toutes les bonnes réponses
- Validez et lisez le feedback de Claude
- Passez à la question suivante

#### 3️⃣ Résultats

- Consultez votre score
- Lisez le récapitulatif personnalisé
- Exportez en PDF
- Régénérez un nouveau QCM

---

## ☁️ Déploiement sur Streamlit Cloud

### Étape 1 : Préparer le Code

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/votre-username/qcm-medical.git
git push -u origin main
```

> ⚠️ **Ne commitez JAMAIS votre fichier `.env` avec la clé API !**

### Étape 2 : Déployer

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez-vous avec GitHub
3. Cliquez sur **New app**
4. Configurez :
   - **Repository** : `votre-username/qcm-medical`
   - **Branch** : `main`
   - **Main file** : `app.py`
5. Déployez !

### Étape 3 : Configurer les Secrets

Dans **Settings** → **Secrets**, ajoutez :

```toml
ANTHROPIC_API_KEY = "sk-ant-votre-cle-ici"
```

### Étape 4 : Partager

Votre app est en ligne à :
```
https://votre-username-qcm-medical.streamlit.app
```

---

## 📁 Structure du Projet

```
qcm-medical/
│
├── app.py                      # Application principale Streamlit
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── .gitignore                  # Fichiers à ignorer
│
└── utils/
    ├── __init__.py
    ├── document_parser.py      # Extraction Word/PDF
    ├── claude_api.py           # Gestion API Claude
    └── pdf_export.py           # Export PDF
```

---

## 💰 Coûts Estimés

Avec **Claude Haiku 4.5** (modèle le plus économique) :

| Type | Prix | Usage |
|------|------|-------|
| **Input** | $0.80 / M tokens | Lecture du cours |
| **Output** | $4.00 / M tokens | Génération questions |

### Par Session

- Upload cours (5000 mots + images) : ~8000 tokens input
- Génération 10 questions : ~3000 tokens output
- Feedback + récapitulatif : ~2000 tokens output

**Total ≈ $0.03 par session** (3 centimes) 💰

> 💡 Très économique pour un usage personnel !

---

## 🎨 Personnalisation

### Modifier le Nombre de Questions

Dans `utils/claude_api.py`, ligne 28 :

```python
"Exactement 10 questions"  # Changez le nombre ici
```

### Changer le Modèle Claude

Dans `utils/claude_api.py`, ligne 19 :

```python
self.model = "claude-haiku-4-5"  # Économique ⚡
# Alternatives :
# "claude-sonnet-4-5"  # Plus performant 🧠
# "claude-opus-4"      # Le meilleur 🎯
```

### Modifier le Style des Questions

Dans `utils/claude_api.py`, lignes 28-80, personnalisez le prompt système.

---

## 🛠️ Dépannage

<details>
<summary><b>❌ "Module not found"</b></summary>

```bash
pip install -r requirements.txt --upgrade
```
</details>

<details>
<summary><b>❌ "Invalid API key"</b></summary>

- Vérifiez que votre clé commence par `sk-ant-`
- Créez une nouvelle clé sur [console.anthropic.com](https://console.anthropic.com/)
- Vérifiez vos crédits API
</details>

<details>
<summary><b>❌ Erreur extraction PDF</b></summary>

```bash
pip install PyMuPDF --upgrade
```
</details>

<details>
<summary><b>⏱️ Génération lente</b></summary>

Normal ! La génération prend 30-60 secondes pour garantir des questions de qualité.
</details>

---

## 🤝 Support

### Ressources

- [Documentation Claude](https://docs.anthropic.com/)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Forum Streamlit](https://discuss.streamlit.io/)

### Questions Fréquentes

**Q : Puis-je utiliser l'app hors ligne ?**  
R : Non, connexion internet nécessaire pour l'API Claude.

**Q : Les données sont-elles sauvegardées ?**  
R : Non, tout est en mémoire. Exportez en PDF pour conserver vos résultats.

**Q : Les images sont-elles analysées ?**  
R : Oui ! Claude utilise les images comme contexte pour générer des questions.

---

## 📊 Technologies Utilisées

- **[Streamlit](https://streamlit.io)** - Interface web
- **[Claude API](https://www.anthropic.com)** - Intelligence artificielle
- **[PyMuPDF](https://pymupdf.readthedocs.io/)** - Traitement PDF
- **[python-docx](https://python-docx.readthedocs.io/)** - Traitement Word
- **[ReportLab](https://www.reportlab.com/)** - Génération PDF

---

## 📜 Licence

MIT License - Libre d'utilisation pour un usage personnel ou éducatif.

---

## 🎉 Contributeurs

Créé avec ❤️ pour faciliter les révisions médicales.

---

## ⭐ Soutenez le Projet

Si cette application vous aide dans vos révisions, n'hésitez pas à :

- ⭐ Star le projet sur GitHub
- 🐛 Signaler des bugs via [Issues](https://github.com/loic-123/qcm-medical/issues)
- 💡 Proposer des améliorations

---

**Bon courage pour les EDN !** 🚀
