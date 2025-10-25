"""
Module d'export des QCM en PDF
Format professionnel pour impression/révision
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, 
    PageBreak, Table, TableStyle
)
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from typing import List, Dict


class PDFExporter:
    """Classe pour exporter les QCM en PDF"""
    
    @staticmethod
    def create_qcm_pdf(questions: List[Dict], with_answers: bool = False) -> BytesIO:
        """
        Crée un PDF contenant les questions QCM
        
        Args:
            questions: Liste des questions générées
            with_answers: Si True, inclut les réponses et explications
            
        Returns:
            BytesIO contenant le PDF
        """
        buffer = BytesIO()
        
        # Création du document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=0.5*cm,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            spaceAfter=1*cm,
            alignment=TA_CENTER
        )
        
        question_style = ParagraphStyle(
            'QuestionStyle',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=0.3*cm,
            spaceBefore=0.5*cm
        )
        
        option_style = ParagraphStyle(
            'OptionStyle',
            parent=styles['Normal'],
            fontSize=11,
            leftIndent=0.5*cm,
            spaceAfter=0.2*cm
        )
        
        answer_style = ParagraphStyle(
            'AnswerStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#27ae60'),
            leftIndent=0.5*cm,
            spaceAfter=0.2*cm,
            spaceBefore=0.3*cm
        )
        
        explanation_style = ParagraphStyle(
            'ExplanationStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#34495e'),
            leftIndent=0.5*cm,
            spaceAfter=0.5*cm,
            spaceBefore=0.2*cm,
            backColor=colors.HexColor('#ecf0f1')
        )
        
        # Contenu du document
        story = []
        
        # En-tête
        story.append(Paragraph("QCM Médical - EDN", title_style))
        story.append(Paragraph(
            f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
            subtitle_style
        ))
        story.append(Spacer(1, 0.5*cm))
        
        # Informations
        if with_answers:
            info_text = "<b>Version avec corrigé</b> - Document de révision"
        else:
            info_text = "<b>Version vierge</b> - À compléter"
        story.append(Paragraph(info_text, styles['Normal']))
        story.append(Spacer(1, 0.5*cm))
        
        # Ligne de séparation
        line_data = [['', '']]
        line_table = Table(line_data, colWidths=[doc.width])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 2, colors.HexColor('#1f77b4')),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Questions
        for i, q in enumerate(questions, 1):
            # Numéro et question
            story.append(Paragraph(
                f"<b>Question {i}</b>",
                question_style
            ))
            story.append(Paragraph(q['question'], styles['Normal']))
            story.append(Spacer(1, 0.3*cm))
            
            # Options
            for j, option in enumerate(q['options']):
                checkbox = "☐"  # Case vide par défaut
                
                if with_answers and j in q['correct_answers']:
                    checkbox = "☑"  # Case cochée pour les bonnes réponses
                    option_text = f"<b>{checkbox} {option}</b>"
                else:
                    option_text = f"{checkbox} {option}"
                
                story.append(Paragraph(option_text, option_style))
            
            # Réponses et explications (si demandé)
            if with_answers:
                story.append(Spacer(1, 0.3*cm))
                
                correct_options = [q['options'][idx] for idx in q['correct_answers']]
                answer_text = f"<b>✓ Réponse(s) correcte(s) :</b> {', '.join(correct_options)}"
                story.append(Paragraph(answer_text, answer_style))
                
                explanation_text = f"<b>💡 Explication :</b><br/>{q.get('explanation', 'Non disponible')}"
                story.append(Paragraph(explanation_text, explanation_style))
            
            story.append(Spacer(1, 0.7*cm))
            
            # Saut de page toutes les 3 questions (sauf dernière)
            if i % 3 == 0 and i < len(questions):
                story.append(PageBreak())
        
        # Pied de page
        story.append(Spacer(1, 1*cm))
        footer_text = "QCM généré par Claude Haiku 4.5 - Application QCM Médical"
        story.append(Paragraph(footer_text, subtitle_style))
        
        # Construction du PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer
    
    @staticmethod
    def create_results_pdf(all_results: List[Dict], summary: str) -> BytesIO:
        """
        Crée un PDF avec les résultats du QCM complété
        
        Args:
            all_results: Liste des résultats complets
            summary: Récapitulatif textuel généré par Claude
            
        Returns:
            BytesIO contenant le PDF
        """
        buffer = BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # En-tête
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1f77b4'),
            alignment=TA_CENTER
        )
        
        story.append(Paragraph("Résultats du QCM", title_style))
        story.append(Paragraph(
            f"Session du {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
            styles['Normal']
        ))
        story.append(Spacer(1, 1*cm))
        
        # Score global
        total = len(all_results)
        perfect = sum(1 for r in all_results if set(r['user_answers']) == set(r['correct_answers']))
        score_text = f"<b>Score : {perfect}/{total} ({int(perfect/total*100)}%)</b>"
        story.append(Paragraph(score_text, styles['Heading2']))
        story.append(Spacer(1, 0.5*cm))
        
        # Récapitulatif
        story.append(Paragraph("<b>Récapitulatif personnalisé</b>", styles['Heading2']))
        for line in summary.split('\n'):
            if line.strip():
                story.append(Paragraph(line, styles['Normal']))
        
        story.append(PageBreak())
        
        # Détail des réponses
        story.append(Paragraph("<b>Détail des réponses</b>", styles['Heading2']))
        story.append(Spacer(1, 0.5*cm))
        
        for i, result in enumerate(all_results, 1):
            is_correct = set(result['user_answers']) == set(result['correct_answers'])
            
            # Question
            q_style = ParagraphStyle(
                'Q',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.green if is_correct else colors.red,
                spaceAfter=0.2*cm
            )
            
            status = "✓" if is_correct else "✗"
            story.append(Paragraph(f"<b>{status} Question {i} :</b> {result['question']}", q_style))
            
            # Réponses
            story.append(Paragraph(
                f"Vos réponses : {', '.join([result['options'][j] for j in result['user_answers']]) or 'Aucune'}",
                styles['Normal']
            ))
            story.append(Paragraph(
                f"Réponses attendues : {', '.join([result['options'][j] for j in result['correct_answers']])}",
                styles['Normal']
            ))
            story.append(Spacer(1, 0.5*cm))
        
        doc.build(story)
        buffer.seek(0)
        
        return buffer
