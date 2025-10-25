"""
Script de test pour vérifier que toutes les dépendances sont correctement installées
"""

import sys

def test_imports():
    """Teste l'import de tous les modules nécessaires"""
    
    print("🧪 Test des imports...\n")
    
    modules = {
        'streamlit': 'Interface web',
        'anthropic': 'API Claude',
        'docx': 'Lecture fichiers Word',
        'fitz': 'Lecture fichiers PDF (PyMuPDF)',
        'PIL': 'Traitement d\'images',
        'reportlab': 'Génération PDF'
    }
    
    all_ok = True
    
    for module, description in modules.items():
        try:
            __import__(module)
            print(f"✅ {module:15} - {description}")
        except ImportError as e:
            print(f"❌ {module:15} - ERREUR : {e}")
            all_ok = False
    
    print("\n" + "="*50)
    
    if all_ok:
        print("✅ Tous les modules sont installés correctement !")
        print("\nVous pouvez lancer l'application avec :")
        print("   streamlit run app.py")
        return True
    else:
        print("❌ Certains modules sont manquants.")
        print("\nInstallez les dépendances avec :")
        print("   pip install -r requirements.txt")
        return False


def test_utils():
    """Teste l'import des modules utils"""
    
    print("\n🧪 Test des modules utils...\n")
    
    try:
        from utils.document_parser import DocumentParser
        print("✅ document_parser.py")
    except Exception as e:
        print(f"❌ document_parser.py - {e}")
        return False
    
    try:
        from utils.claude_api import ClaudeQCMGenerator
        print("✅ claude_api.py")
    except Exception as e:
        print(f"❌ claude_api.py - {e}")
        return False
    
    try:
        from utils.pdf_export import PDFExporter
        print("✅ pdf_export.py")
    except Exception as e:
        print(f"❌ pdf_export.py - {e}")
        return False
    
    print("\n✅ Tous les modules utils sont fonctionnels !")
    return True


def check_python_version():
    """Vérifie la version de Python"""
    
    print("🐍 Version Python\n")
    version = sys.version_info
    print(f"Version détectée : Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 9:
        print("✅ Version Python compatible (≥ 3.9)")
        return True
    else:
        print("❌ Version Python trop ancienne (besoin de ≥ 3.9)")
        return False


def main():
    """Point d'entrée du script de test"""
    
    print("\n" + "="*50)
    print("🏥 QCM MÉDICAL - Test d'Installation")
    print("="*50 + "\n")
    
    # Test version Python
    python_ok = check_python_version()
    print()
    
    # Test imports
    imports_ok = test_imports()
    print()
    
    # Test modules utils
    utils_ok = test_utils()
    
    print("\n" + "="*50)
    
    if python_ok and imports_ok and utils_ok:
        print("✅ Installation réussie ! L'application est prête.")
        print("\n🚀 Pour lancer l'application :")
        print("   streamlit run app.py")
    else:
        print("❌ Des problèmes ont été détectés.")
        print("\n🔧 Actions suggérées :")
        if not python_ok:
            print("   - Mettez à jour Python vers version ≥ 3.9")
        if not imports_ok:
            print("   - Exécutez : pip install -r requirements.txt")
        if not utils_ok:
            print("   - Vérifiez que tous les fichiers sont présents")
    
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
