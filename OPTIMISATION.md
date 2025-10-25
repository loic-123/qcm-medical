# 🎯 Optimisation Avancée

Ce document contient des conseils pour optimiser l'utilisation de l'application et personnaliser son comportement.

---

## 🔧 Personnalisation des Prompts

Les prompts sont l'élément clé de la qualité des QCM générés. Voici comment les optimiser.

### Modifier le prompt de génération

**Fichier** : `utils/claude_api.py`, ligne 28-42

**Ajustements possibles :**

1. **Niveau de difficulté**
```python
# Plus facile (pour révisions de base)
"Ton rôle est de créer des QCM de niveau intermédiaire qui testent les connaissances fondamentales..."

# Plus difficile (pour préparation intensive)
"Ton rôle est de créer des QCM avancés avec des cas cliniques complexes et pièges subtils..."
```

2. **Type de questions**
```python
# Plus de cas cliniques
"Privilégie les cas cliniques réalistes avec contexte patient, anamnèse et examens..."

# Plus de physiopathologie
"Concentre-toi sur les mécanismes physiopathologiques et le raisonnement causal..."

# Mélange équilibré
"Alterne entre questions de connaissances pures (30%), raisonnement clinique (40%) et cas pratiques (30%)..."
```

3. **Spécialité médicale**
```python
# Pour cours de cardiologie
"Tu es expert en cardiologie. Crée des QCM type EDN spécifiques à cette spécialité..."

# Pour cours de pharmacologie
"Concentre-toi sur les mécanismes d'action, interactions médicamenteuses et effets indésirables..."
```

### Modifier le prompt de feedback

**Fichier** : `utils/claude_api.py`, ligne 125-138

**Exemple d'amélioration :**
```python
prompt = f"""Question : {question['question']}

Contexte : Tu es un tuteur médical expert. L'étudiant est en 5e année.

Génère un feedback qui :
1. Commence par un emoji selon la performance (🎉 parfait / 💪 bien / 🔍 à revoir)
2. Analyse chaque option sélectionnée
3. Explique la physiopathologie sous-jacente
4. Donne un moyen mnémotechnique si pertinent
5. Suggère des ressources complémentaires

Ton ton doit être bienveillant mais exigeant."""
```

---

## ⚡ Optimisation des Performances

### Réduire les coûts API

1. **Limiter les images contextuelles**
```python
# Dans document_parser.py, ligne 68
# Actuellement : 5 images max
for img in images[:3]:  # Réduire à 3 images
```

2. **Réduire le max_tokens**
```python
# Dans claude_api.py, ligne 87
max_tokens=4096,  # Actuellement
max_tokens=3000,  # Réduit (économie ~25%)
```

3. **Utiliser le cache de prompts** (feature Claude avancée)
```python
# Ajoutez ceci dans les appels API pour réutiliser les prompts
cache_control={"type": "ephemeral"}
```

### Accélérer la génération

1. **Réduire le nombre de questions**
```python
# Changer "10 questions" par "5 questions" dans le prompt système
```

2. **Générer en parallèle** (avancé)
```python
# Remplacer les appels séquentiels par asyncio
import asyncio

async def generate_multiple_qcm():
    tasks = [generate_qcm_async(text, images) for _ in range(3)]
    return await asyncio.gather(*tasks)
```

---

## 🎨 Personnalisation Interface

### Modifier le thème visuel

**Fichier** : `app.py`, ligne 16-42

Ajoutez des styles CSS personnalisés :

```python
st.markdown("""
    <style>
    /* Votre thème personnalisé */
    .main-header {
        color: #2c3e50;  /* Couleur personnalisée */
    }
    
    /* Changer la couleur de fond */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Boutons personnalisés */
    .stButton button {
        background-color: #3498db;
        color: white;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)
```

### Ajouter un logo

```python
# Au début de main()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=200)  # Ajoutez votre logo
```

---

## 📊 Ajout de Fonctionnalités

### 1. Sauvegarde des résultats

Ajoutez après le calcul du score (app.py, ligne ~460) :

```python
import json
from datetime import datetime

# Créer un fichier JSON avec les résultats
results_data = {
    'date': datetime.now().isoformat(),
    'score': f"{correct_count}/{total_questions}",
    'questions': all_results,
    'summary': st.session_state.final_summary
}

# Sauvegarder localement
with open(f"resultats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
    json.dump(results_data, f, ensure_ascii=False, indent=2)

st.success("💾 Résultats sauvegardés localement !")
```

### 2. Timer par question

Ajoutez dans l'onglet QCM (app.py, après ligne 300) :

```python
import time

# Initialiser le timer
if 'question_start_time' not in st.session_state:
    st.session_state.question_start_time = time.time()

# Afficher le temps écoulé
elapsed = int(time.time() - st.session_state.question_start_time)
st.sidebar.metric("⏱️ Temps écoulé", f"{elapsed}s")

# Réinitialiser à chaque nouvelle question
# (Ajoutez après la soumission de la réponse)
st.session_state.question_start_time = time.time()
```

### 3. Statistiques globales

Créez un nouveau fichier `statistics.py` :

```python
import json
from pathlib import Path
from typing import List, Dict

class Statistics:
    def __init__(self, stats_file='stats.json'):
        self.stats_file = Path(stats_file)
        self.stats = self.load_stats()
    
    def load_stats(self) -> Dict:
        if self.stats_file.exists():
            return json.loads(self.stats_file.read_text())
        return {'sessions': []}
    
    def add_session(self, score: int, total: int):
        self.stats['sessions'].append({
            'date': datetime.now().isoformat(),
            'score': score,
            'total': total
        })
        self.stats_file.write_text(json.dumps(self.stats, indent=2))
    
    def get_average_score(self) -> float:
        if not self.stats['sessions']:
            return 0
        scores = [s['score']/s['total'] for s in self.stats['sessions']]
        return sum(scores) / len(scores) * 100
```

---

## 🔐 Sécurité et Bonnes Pratiques

### Pour déploiement public

1. **Ne jamais commit la clé API**
```bash
# Vérifier le .gitignore
cat .gitignore | grep .env
```

2. **Utiliser Streamlit Secrets**
```python
# Dans app.py
import streamlit as st

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    api_key = st.text_input("Clé API", type="password")
```

3. **Limiter les requêtes**
```python
# Ajouter un rate limiting simple
import time

if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = 0

current_time = time.time()
if current_time - st.session_state.last_request_time < 10:
    st.warning("⏳ Attendez 10 secondes entre chaque génération")
    return

st.session_state.last_request_time = current_time
```

---

## 🧪 Mode Debug

Ajoutez un mode debug pour développement (app.py, sidebar) :

```python
with st.sidebar.expander("🔧 Mode Debug"):
    debug_mode = st.checkbox("Activer")
    
    if debug_mode:
        st.json(st.session_state.to_dict())
        
        if st.button("Réinitialiser session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
```

---

## 📈 Métriques et Monitoring

Pour suivre l'utilisation en production :

```python
import logging

# Configuration logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Logger les événements importants
logging.info(f"QCM généré : {len(questions)} questions")
logging.info(f"Score final : {correct_count}/{total_questions}")
```

---

## 🌍 Internationalisation

Pour supporter plusieurs langues :

```python
# Créer un fichier translations.py
TRANSLATIONS = {
    'fr': {
        'title': 'QCM Médical',
        'upload': 'Télécharger un document',
        # ...
    },
    'en': {
        'title': 'Medical MCQ',
        'upload': 'Upload document',
        # ...
    }
}

# Dans app.py
language = st.sidebar.selectbox("🌍 Langue", ['Français', 'English'])
lang_code = 'fr' if language == 'Français' else 'en'
t = TRANSLATIONS[lang_code]

st.title(t['title'])
```

---

## 💡 Idées d'Améliorations Futures

1. **Base de données** : SQLite pour historique complet
2. **Authentification** : Multi-utilisateurs avec comptes
3. **Modes d'examen** : Conditions chronométrées strictes
4. **Révisions espacées** : Algorithme de répétition espacée
5. **Collaboration** : Partage de QCM entre étudiants
6. **Analyse avancée** : Graphiques de progression
7. **Export Anki** : Pour révisions sur mobile
8. **API REST** : Permettre intégration externe

---

Ces optimisations permettent d'adapter l'application à vos besoins spécifiques ! 🚀
