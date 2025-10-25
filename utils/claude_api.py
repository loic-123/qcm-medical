"""
Module de gestion des appels à l'API Claude
Génération de QCM, feedback et récapitulatif
"""

import json
from typing import List, Dict, Any
from anthropic import Anthropic


class ClaudeQCMGenerator:
    """Classe pour générer des QCM médicaux via Claude"""
    
    def __init__(self, api_key: str):
        """
        Initialise le client Claude
        
        Args:
            api_key: Clé API Anthropic
        """
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-haiku-4-5"  # Haiku 4.5
    
    def generate_qcm(self, text: str, images: List[Dict]) -> List[Dict]:
        """
        Génère 10 questions QCM type EDN depuis un document
        
        Args:
            text: Texte extrait du document
            images: Liste d'images {data: base64, format: str}
            
        Returns:
            Liste de 10 questions au format:
            {
                "question": str,
                "options": [str],
                "correct_answers": [int],  # Indices des bonnes réponses (0-based)
                "explanation": str
            }
        """
        
        # Construction du prompt système
        system_prompt = """Tu es un expert en pédagogie médicale spécialisé dans la création de QCM pour les EDN (Examens Dématérialisés Nationaux) de médecine en France.

Ton rôle est de créer des QCM de haute qualité niveau DFASM (5e année de médecine) qui :
- Testent la compréhension profonde et le raisonnement clinique
- Sont représentatifs des questions EDN réelles
- Évitent les pièges trop évidents ou ambiguïtés
- Incluent des cas cliniques quand pertinent
- Couvrent différents aspects du cours (physiopathologie, diagnostic, traitement, etc.)

RÈGLES STRICTES :
- Exactement 10 questions
- 4 à 5 propositions par question
- Plusieurs bonnes réponses possibles par question (typique des EDN)
- Formulation claire et précise
- Explications pédagogiques détaillées"""

        # Construction du message utilisateur
        user_content = [
            {
                "type": "text",
                "text": f"""À partir du cours médical suivant, génère 10 questions QCM type EDN.

COURS :
{text}

CONSIGNES :
1. Crée des questions qui couvrent l'ensemble du cours
2. Varie les types de questions (connaissances, cas cliniques, raisonnement)
3. Assure-toi que plusieurs réponses sont correctes pour chaque question
4. Fournis des explications détaillées et pédagogiques

FORMAT DE SORTIE (JSON strict) :
{{
    "questions": [
        {{
            "question": "Énoncé complet de la question",
            "options": ["Option A", "Option B", "Option C", "Option D", "Option E"],
            "correct_answers": [0, 2],
            "explanation": "Explication détaillée des bonnes et mauvaises réponses"
        }}
    ]
}}

IMPORTANT : Réponds UNIQUEMENT avec le JSON, sans texte avant ou après."""
            }
        ]
        
        # Ajout des images si présentes (contexte visuel)
        if images and len(images) > 0:
            # Limiter à 5 images max pour ne pas surcharger
            for img in images[:5]:
                user_content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": f"image/{img['format']}",
                        "data": img['data']
                    }
                })
        
        try:
            # Appel API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10000,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": user_content
                }]
            )
            
            # Extraction et parsing du JSON
            response_text = response.content[0].text
            
            # Nettoyage du texte (au cas où Claude ajoute du texte autour)
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            parsed_response = json.loads(response_text)
            questions = parsed_response.get("questions", [])
            
            # Validation
            if len(questions) != 10:
                print(f"⚠️ Attention: {len(questions)} questions générées au lieu de 10")
            
            return questions
            
        except json.JSONDecodeError as e:
            print(f"❌ Erreur parsing JSON: {e}")
            print(f"Réponse brute: {response_text[:500]}")
            return []
        except Exception as e:
            print(f"❌ Erreur API Claude: {e}")
            return []
    
    def explain_answer(self, question: Dict, user_answers: List[int]) -> str:
        """
        Génère une explication personnalisée après soumission d'une réponse
        
        Args:
            question: Dict contenant la question complète
            user_answers: Liste des indices sélectionnés par l'utilisateur
            
        Returns:
            Explication personnalisée en markdown
        """
        
        correct_answers = set(question['correct_answers'])
        user_answers_set = set(user_answers)
        
        # Déterminer quelles options sont correctes/incorrectes
        correct_selected = user_answers_set & correct_answers
        incorrect_selected = user_answers_set - correct_answers
        correct_missed = correct_answers - user_answers_set
        
        prompt = f"""Question : {question['question']}

Options proposées :
{chr(10).join([f"{i}. {opt}" for i, opt in enumerate(question['options'])])}

Bonnes réponses : {', '.join([question['options'][i] for i in correct_answers])}
Réponses de l'étudiant : {', '.join([question['options'][i] for i in user_answers]) if user_answers else 'Aucune réponse'}

Génère un feedback PERSONNALISÉ et PÉDAGOGIQUE qui :
1. Félicite les bonnes réponses sélectionnées (si applicable)
2. Explique pourquoi les réponses incorrectes sélectionnées sont fausses (si applicable)
3. Mentionne les bonnes réponses manquées (si applicable)
4. Donne le raisonnement médical complet

Ton feedback doit être bienveillant mais précis. Utilise des émojis (✅ ❌ 💡) pour la clarté.
Format markdown."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1200,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"❌ Erreur génération feedback: {e}")
            return question.get('explanation', 'Explication non disponible.')
    
    def generate_final_summary(self, all_results: List[Dict]) -> str:
        """
        Génère un récapitulatif personnalisé basé sur les performances
        
        Args:
            all_results: Liste de dicts avec {question, user_answers, correct_answers}
            
        Returns:
            Récapitulatif en markdown
        """
        
        # Calcul des statistiques
        total_questions = len(all_results)
        perfect_answers = sum(
            1 for r in all_results 
            if set(r['user_answers']) == set(r['correct_answers'])
        )
        
        # Préparation du contexte pour Claude
        results_text = []
        for i, result in enumerate(all_results, 1):
            is_correct = set(result['user_answers']) == set(result['correct_answers'])
            status = "✅ Correct" if is_correct else "❌ Incomplet/Incorrect"
            
            results_text.append(f"""
Question {i} - {status}
Énoncé : {result['question']}
Réponses attendues : {', '.join([result['options'][j] for j in result['correct_answers']])}
Réponses données : {', '.join([result['options'][j] for j in result['user_answers']]) if result['user_answers'] else 'Aucune'}
""")
        
        prompt = f"""Tu es un tuteur médical bienveillant. Un étudiant en 5e année de médecine vient de terminer un QCM de 10 questions.

RÉSULTATS :
- Score : {perfect_answers}/{total_questions} questions parfaitement réussies
- Détails :
{chr(10).join(results_text)}

MISSION :
Génère un récapitulatif personnalisé et motivant qui inclut :

1. **📊 Analyse globale** (2-3 phrases sur la performance)
2. **🎯 Points forts** (ce qui est bien maîtrisé)
3. **📚 Axes d'amélioration** (concepts à revoir, avec suggestions concrètes)
4. **💡 Conseils de révision** (comment approfondir les notions fragiles)
5. **🔥 Mot d'encouragement** (personnalisé selon le score)

Ton ton doit être :
- Pédagogue et constructif
- Spécifique aux erreurs faites
- Motivant et encourageant

Format markdown avec émojis. Maximum 400 mots."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1200,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"❌ Erreur génération récapitulatif: {e}")
            return f"# Récapitulatif\n\nScore : {perfect_answers}/{total_questions} questions parfaitement réussies."
