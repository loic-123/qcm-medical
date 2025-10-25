"""
Module de gestion des appels à l'API Claude
Génération de QCM, feedback et récapitulatif
VERSION OPTIMISÉE avec sélecteur de difficulté
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
    
    def generate_qcm(self, text: str, images: List[Dict], difficulty: str = "intermediaire") -> List[Dict]:
        """
        Génère 10 questions QCM type EDN depuis un document
        
        Args:
            text: Texte extrait du document
            images: Liste d'images {data: base64, format: str}
            difficulty: Niveau de difficulté ("facile", "intermediaire", "difficile")
            
        Returns:
            Liste de 10 questions au format:
            {
                "question": str,
                "options": [str],
                "correct_answers": [int],  # Indices des bonnes réponses (0-based)
                "explanation": str
            }
        """
        
        # Construction du prompt système adapté au niveau (VERSION COURTE pour rapidité)
        difficulty_instructions = {
            "facile": "Niveau DÉBUTANT : questions directes sur connaissances fondamentales et définitions de base. Évite les cas complexes.",
            "intermediaire": "Niveau DFASM standard : raisonnement clinique, cas simples, représentatif des EDN réels.",
            "difficile": "Niveau EXPERT : cas cliniques complexes, pièges subtils, diagnostics différentiels, situations atypiques."
        }
        
        # Prompt système court et efficace
        system_prompt = f"""Expert QCM médical EDN. {difficulty_instructions.get(difficulty, difficulty_instructions["intermediaire"])}

Crée 10 QCM (4-5 options, plusieurs bonnes réponses). Couvre physiopathologie, diagnostic, traitement. Format JSON strict."""

        # Construction du message utilisateur (VERSION COURTE)
        user_content = [
            {
                "type": "text",
                "text": f"""Génère 10 QCM EDN depuis ce cours médical.

COURS :
{text}

FORMAT JSON strict :
{{
    "questions": [
        {{
            "question": "Énoncé",
            "options": ["A", "B", "C", "D", "E"],
            "correct_answers": [0, 2],
            "explanation": "Explication détaillée"
        }}
    ]
}}

IMPORTANT : JSON uniquement, pas de texte autour."""
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
        OPTIMISÉ pour rapidité (tokens réduits)
        
        Args:
            question: Dict contenant la question complète
            user_answers: Liste des indices sélectionnés par l'utilisateur
            
        Returns:
            Explication personnalisée en markdown
        """
        
        correct_answers = set(question['correct_answers'])
        user_answers_set = set(user_answers)
        
        # Prompt optimisé et plus concis pour réponse rapide
        prompt = f"""Question : {question['question']}

Réponses correctes : {', '.join([question['options'][i] for i in correct_answers])}
Réponses données : {', '.join([question['options'][i] for i in user_answers]) if user_answers else 'Aucune'}

Feedback concis (max 150 mots) :
1. Statut (✅/❌) + analyse rapide
2. Explication médicale essentielle
3. Point clé à retenir

Sois direct et pédagogue."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=600,  # Réduit de 1200 -> 600 pour vitesse ~2x
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