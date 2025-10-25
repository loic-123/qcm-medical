"""
Application Streamlit - QCM Médical avec Claude
Interface interactive pour générer et passer des QCM depuis des cours
VERSION OPTIMISÉE avec sélecteur de difficulté et feedback rapide
"""

import streamlit as st
import os
from utils.document_parser import DocumentParser
from utils.claude_api import ClaudeQCMGenerator  # Version optimisée
from utils.pdf_export import PDFExporter


# Configuration de la page
st.set_page_config(
    page_title="QCM Médical - EDN",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #e8f4f8;
        border: 2px solid #1f77b4;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .correct-answer {
        background-color: #d4edda;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .incorrect-answer {
        background-color: #f8d7da;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    .difficulty-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .diff-facile { background-color: #d4edda; color: #155724; }
    .diff-intermediaire { background-color: #fff3cd; color: #856404; }
    .diff-difficile { background-color: #f8d7da; color: #721c24; }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialise les variables de session Streamlit"""
    if 'questions' not in st.session_state:
        st.session_state.questions = None
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'submitted_questions' not in st.session_state:
        st.session_state.submitted_questions = set()
    if 'all_submitted' not in st.session_state:
        st.session_state.all_submitted = False
    if 'final_summary' not in st.session_state:
        st.session_state.final_summary = None
    if 'document_text' not in st.session_state:
        st.session_state.document_text = None
    if 'document_images' not in st.session_state:
        st.session_state.document_images = None
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = 'intermediaire'


def reset_qcm():
    """Réinitialise le QCM pour permettre une nouvelle génération"""
    st.session_state.questions = None
    st.session_state.current_question_index = 0
    st.session_state.user_answers = {}
    st.session_state.submitted_questions = set()
    st.session_state.all_submitted = False
    st.session_state.final_summary = None


def main():
    initialize_session_state()
    
    # En-tête
    st.markdown('<h1 class="main-header">🏥 QCM Médical - EDN</h1>', unsafe_allow_html=True)
    st.markdown("### Générateur de QCM intelligent avec Claude Haiku 4.5 ⚡")
    
    # Barre latérale - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Clé API
        api_key = st.text_input(
            "Clé API Anthropic",
            type="password",
            help="Votre clé API Claude (commence par 'sk-ant-')"
        )
        
        if not api_key:
            st.warning("⚠️ Veuillez entrer votre clé API Anthropic")
            st.info("💡 Obtenez votre clé sur console.anthropic.com")
        
        st.divider()
        
        # Informations
        st.header("📚 À propos")
        st.markdown("""
        Cette application génère des **QCM type EDN** depuis vos cours de médecine.
        
        **Fonctionnalités :**
        - 📄 Upload Word/PDF avec images
        - 🤖 10 questions générées par IA
        - ✅ Feedback immédiat
        - 📊 Récapitulatif personnalisé
        - 📥 Export PDF
        - 🔄 Régénération possible
        - 🎯 **3 niveaux de difficulté**
        
        **Format :**
        - Plusieurs bonnes réponses possibles
        - 4-5 options par question
        - Niveau 5e année (DFASM)
        """)
        
        st.divider()
        st.caption("Propulsé par Claude Haiku 4.5 🚀")
    
    # Si pas de clé API, arrêter ici
    if not api_key:
        st.info("👈 Commencez par entrer votre clé API dans la barre latérale")
        return
    
    # Initialisation du générateur
    generator = ClaudeQCMGenerator(api_key)
    
    # Zone principale
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Génération", "📝 QCM Interactif", "📊 Résultats"])
    
    # ===== TAB 1 : UPLOAD & GÉNÉRATION =====
    with tab1:
        st.header("📤 Upload de votre cours")
        
        # Sélecteur de difficulté
        st.subheader("🎯 Niveau de difficulté des questions")
        
        difficulty_col1, difficulty_col2, difficulty_col3 = st.columns(3)
        
        with difficulty_col1:
            if st.button("📗 Facile\n(Révisions de base)", use_container_width=True, 
                        type="primary" if st.session_state.difficulty == 'facile' else "secondary"):
                st.session_state.difficulty = 'facile'
                st.rerun()
            st.caption("✓ Connaissances fondamentales\n✓ Questions directes\n✓ Idéal pour débuter")
        
        with difficulty_col2:
            if st.button("📘 Intermédiaire\n(Type EDN standard)", use_container_width=True,
                        type="primary" if st.session_state.difficulty == 'intermediaire' else "secondary"):
                st.session_state.difficulty = 'intermediaire'
                st.rerun()
            st.caption("✓ Raisonnement clinique\n✓ Cas cliniques simples\n✓ Niveau DFASM classique")
        
        with difficulty_col3:
            if st.button("📕 Difficile\n(Préparation intensive)", use_container_width=True,
                        type="primary" if st.session_state.difficulty == 'difficile' else "secondary"):
                st.session_state.difficulty = 'difficile'
                st.rerun()
            st.caption("✓ Cas complexes\n✓ Pièges subtils\n✓ Expertise avancée")
        
        # Badge du niveau sélectionné
        difficulty_labels = {
            'facile': ('📗 Facile', 'diff-facile'),
            'intermediaire': ('📘 Intermédiaire', 'diff-intermediaire'),
            'difficile': ('📕 Difficile', 'diff-difficile')
        }
        
        label, css_class = difficulty_labels[st.session_state.difficulty]
        st.markdown(f'<div class="difficulty-badge {css_class}">Niveau sélectionné : {label}</div>', 
                   unsafe_allow_html=True)
        
        st.divider()
        
        uploaded_file = st.file_uploader(
            "Glissez-déposez votre fichier Word ou PDF",
            type=['docx', 'pdf'],
            help="Le fichier peut contenir du texte et des images"
        )
        
        if uploaded_file:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.success(f"✅ Fichier chargé : **{uploaded_file.name}**")
                st.info(f"📦 Taille : {uploaded_file.size / 1024:.1f} KB")
            
            with col2:
                file_type = 'docx' if uploaded_file.name.endswith('.docx') else 'pdf'
                st.metric("Type", file_type.upper())
            
            # Bouton de génération
            generate_col1, generate_col2 = st.columns([2, 1])
            
            with generate_col1:
                generate_button = st.button(
                    f"🚀 Générer le QCM (10 questions - {label})",
                    type="primary",
                    use_container_width=True
                )
            
            with generate_col2:
                if st.session_state.questions is not None:
                    if st.button("🔄 Régénérer nouveau QCM", use_container_width=True):
                        reset_qcm()
                        st.rerun()
            
            if generate_button:
                with st.spinner("🔍 Extraction du contenu..."):
                    try:
                        # Extraction du document
                        file_bytes = uploaded_file.read()
                        text, images = DocumentParser.parse_document(file_bytes, file_type)
                        
                        # Stockage dans session
                        st.session_state.document_text = text
                        st.session_state.document_images = images
                        
                        st.success(f"✅ Extraction réussie : {len(text)} caractères, {len(images)} image(s)")
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de l'extraction : {e}")
                        return
                
                with st.spinner(f"🤖 Claude génère vos questions ({label})... (30-60 secondes)"):
                    try:
                        # Génération des questions avec le niveau de difficulté
                        questions = generator.generate_qcm(
                            st.session_state.document_text,
                            st.session_state.document_images,
                            difficulty=st.session_state.difficulty
                        )
                        
                        if not questions or len(questions) == 0:
                            st.error("❌ Aucune question n'a pu être générée. Réessayez.")
                            return
                        
                        st.session_state.questions = questions
                        st.success(f"✅ {len(questions)} questions générées avec succès !")
                        st.info("👉 Passez à l'onglet **QCM Interactif** pour commencer")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la génération : {e}")
                        return
        
        # Aperçu des questions générées
        if st.session_state.questions:
            st.divider()
            st.subheader("📋 Aperçu des questions générées")
            
            # Badge du niveau
            label, css_class = difficulty_labels[st.session_state.difficulty]
            st.markdown(f'<div class="difficulty-badge {css_class}">{label}</div>', 
                       unsafe_allow_html=True)
            
            with st.expander("Cliquez pour voir toutes les questions", expanded=False):
                for i, q in enumerate(st.session_state.questions, 1):
                    st.markdown(f"**Question {i} :** {q['question']}")
                    st.caption(f"→ {len(q['options'])} options, {len(q['correct_answers'])} bonne(s) réponse(s)")
                    st.divider()
    
    # ===== TAB 2 : QCM INTERACTIF =====
    with tab2:
        if st.session_state.questions is None:
            st.info("📤 Uploadez d'abord un document dans l'onglet **Upload & Génération**")
            return
        
        questions = st.session_state.questions
        current_idx = st.session_state.current_question_index
        
        # Badge du niveau
        label, css_class = difficulty_labels[st.session_state.difficulty]
        st.markdown(f'<div class="difficulty-badge {css_class}">Mode : {label}</div>', 
                   unsafe_allow_html=True)
        
        # Barre de progression
        progress = len(st.session_state.submitted_questions) / len(questions)
        st.progress(progress, text=f"Progression : {len(st.session_state.submitted_questions)}/{len(questions)} questions traitées")
        
        st.divider()
        
        # Navigation entre questions
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if current_idx > 0:
                if st.button("⬅️ Précédent"):
                    st.session_state.current_question_index -= 1
                    st.rerun()
        
        with col2:
            st.markdown(f"### Question {current_idx + 1} / {len(questions)}")
        
        with col3:
            if current_idx < len(questions) - 1:
                if st.button("Suivant ➡️"):
                    st.session_state.current_question_index += 1
                    st.rerun()
        
        st.divider()
        
        # Question actuelle
        current_question = questions[current_idx]
        is_submitted = current_idx in st.session_state.submitted_questions
        
        st.markdown(f"### {current_question['question']}")
        st.caption("ℹ️ Plusieurs réponses peuvent être correctes. Sélectionnez toutes les bonnes réponses.")
        
        # Options (checkboxes multiples)
        st.markdown("#### Propositions :")
        
        selected_options = []
        for i, option in enumerate(current_question['options']):
            # Récupérer la réponse précédente si déjà soumis
            default_value = False
            if current_idx in st.session_state.user_answers:
                default_value = i in st.session_state.user_answers[current_idx]
            
            # Désactiver si déjà soumis
            is_checked = st.checkbox(
                option,
                key=f"q{current_idx}_opt{i}",
                value=default_value,
                disabled=is_submitted
            )
            
            if is_checked:
                selected_options.append(i)
        
        st.divider()
        
        # Bouton de soumission
        if not is_submitted:
            if st.button("✅ Valider ma réponse", type="primary", use_container_width=True):
                if len(selected_options) == 0:
                    st.warning("⚠️ Veuillez sélectionner au moins une réponse")
                else:
                    # Enregistrer la réponse
                    st.session_state.user_answers[current_idx] = selected_options
                    st.session_state.submitted_questions.add(current_idx)
                    
                    # Vérifier si toutes les questions sont terminées
                    if len(st.session_state.submitted_questions) == len(questions):
                        st.session_state.all_submitted = True
                    
                    st.rerun()
        
        # Affichage du feedback si soumis
        if is_submitted:
            user_answer = st.session_state.user_answers[current_idx]
            correct_answer = set(current_question['correct_answers'])
            user_answer_set = set(user_answer)
            
            is_correct = user_answer_set == correct_answer
            
            # Boîte de résultat
            if is_correct:
                st.markdown('<div class="correct-answer">✅ <b>Bravo ! Réponse parfaitement correcte</b></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="incorrect-answer">❌ <b>Réponse incomplète ou incorrecte</b></div>', unsafe_allow_html=True)
            
            # Feedback détaillé (OPTIMISÉ - Plus rapide)
            with st.spinner("💡 Claude analyse votre réponse (⚡ rapide)..."):
                feedback = generator.explain_answer(current_question, user_answer)
            
            st.markdown("### 💡 Explication")
            st.markdown(feedback)
            
            st.divider()
            
            # Bouton suivant/terminer
            if current_idx < len(questions) - 1:
                if st.button("➡️ Question suivante", type="primary", use_container_width=True):
                    st.session_state.current_question_index += 1
                    st.rerun()
            else:
                st.success("🎉 Vous avez terminé toutes les questions !")
                if st.button("📊 Voir le récapitulatif complet", type="primary", use_container_width=True):
                    st.session_state.current_question_index = 0  # Reset pour navigation
                    st.rerun()
    
    # ===== TAB 3 : RÉSULTATS =====
    with tab3:
        if not st.session_state.all_submitted:
            st.info("📝 Terminez d'abord toutes les questions pour voir le récapitulatif complet")
            return
        
        st.header("📊 Récapitulatif de votre session")
        
        # Badge du niveau
        label, css_class = difficulty_labels[st.session_state.difficulty]
        st.markdown(f'<div class="difficulty-badge {css_class}">Niveau : {label}</div>', 
                   unsafe_allow_html=True)
        st.divider()
        
        # Calcul du score
        questions = st.session_state.questions
        total_questions = len(questions)
        correct_count = 0
        
        all_results = []
        for idx, question in enumerate(questions):
            user_ans = st.session_state.user_answers.get(idx, [])
            is_correct = set(user_ans) == set(question['correct_answers'])
            if is_correct:
                correct_count += 1
            
            all_results.append({
                'question': question['question'],
                'options': question['options'],
                'user_answers': user_ans,
                'correct_answers': question['correct_answers']
            })
        
        score_percentage = (correct_count / total_questions) * 100
        
        # Affichage du score
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Questions totales", total_questions)
        with col2:
            st.metric("Réponses parfaites", correct_count, delta=f"{score_percentage:.0f}%")
        with col3:
            st.metric("À revoir", total_questions - correct_count)
        
        st.divider()
        
        # Génération du récapitulatif personnalisé
        if st.session_state.final_summary is None:
            with st.spinner("🤖 Claude prépare votre récapitulatif personnalisé..."):
                summary = generator.generate_final_summary(all_results)
                st.session_state.final_summary = summary
        
        st.markdown("### 📝 Analyse personnalisée")
        st.markdown(st.session_state.final_summary)
        
        st.divider()
        
        # Export PDF
        st.subheader("📥 Exporter en PDF")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # QCM vierge
            pdf_blank = PDFExporter.create_qcm_pdf(questions, with_answers=False)
            st.download_button(
                label="📄 QCM vierge",
                data=pdf_blank,
                file_name="qcm_medical_vierge.pdf",
                mime="application/pdf",
                help="Questions sans réponses (pour révision)"
            )
        
        with col2:
            # QCM avec corrigé
            pdf_answers = PDFExporter.create_qcm_pdf(questions, with_answers=True)
            st.download_button(
                label="📗 QCM avec corrigé",
                data=pdf_answers,
                file_name="qcm_medical_corrige.pdf",
                mime="application/pdf",
                help="Questions avec explications complètes"
            )
        
        with col3:
            # Résultats de la session
            pdf_results = PDFExporter.create_results_pdf(all_results, st.session_state.final_summary)
            st.download_button(
                label="📊 Mes résultats",
                data=pdf_results,
                file_name="mes_resultats_qcm.pdf",
                mime="application/pdf",
                help="Votre performance sur cette session"
            )
        
        st.divider()
        
        # Bouton pour recommencer
        if st.button("🔄 Nouveau QCM (même document)", type="primary", use_container_width=True):
            # Garder le document mais régénérer les questions
            text = st.session_state.document_text
            images = st.session_state.document_images
            difficulty = st.session_state.difficulty
            
            reset_qcm()
            
            with st.spinner("🤖 Génération d'un nouveau QCM..."):
                questions = generator.generate_qcm(text, images, difficulty=difficulty)
                st.session_state.questions = questions
            
            st.success("✅ Nouveau QCM généré !")
            st.rerun()


if __name__ == "__main__":
    main()