import sys
import os

# Ajouter le chemin pour importer les services
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from compilateur import Compiler

def test_specific_queries():
    compiler = Compiler()
    
    queries = [
        {
            "nl": "Affiche les 5 zones les plus polluées",
            "expected_contains": ["SELECT zone", "AVG(pollution)", "FROM mesures", "GROUP BY zone", "ORDER BY AVG(pollution) DESC", "LIMIT 5"]
        },
        {
            "nl": "Combien de capteurs sont hors service ?",
            "expected_contains": ["SELECT COUNT(*)", "FROM capteurs", "WHERE statut = 'hors_service'"]
        },
        {
            "nl": "Quels citoyens ont un score écologique > 80 ?",
            "expected_contains": ["SELECT nom, score_ecolo", "FROM citoyens", "WHERE score_ecolo > 80", "ORDER BY score_ecolo DESC"]
        },
        {
            "nl": "Donne-moi le trajet le plus économique en CO2",
            "expected_contains": ["SELECT id_trajet", "economie_co2", "FROM trajets", "ORDER BY economie_co2 DESC", "LIMIT 1"]
        },
        {
            "nl": "pollution par heure",
            "expected_contains": ["time_bucket('1 hour', timestamp)", "AVG(pollution)", "FROM mesures"]
        }
    ]

    print("\n" + "="*70)
    print("  VERIFICATION DES REQUETES NLP SPECIFIQUES (Neo-Sousse 2030)")
    print("="*70 + "\n")

    all_passed = True
    for i, q in enumerate(queries, 1):
        print(f"Test {i}: \"{q['nl']}\"")
        result = compiler.compile(q["nl"])
        print(f"  Normalisé : {result.normalized}")
        print(f"  Tokens    : {result.tokens}")
        
        if result.success:
            sql = result.sql.replace('\n', ' ')
            print(f"  SQL Genéré : {sql}")
            
            missing = []
            for part in q["expected_contains"]:
                if part.upper() not in sql.upper():
                    missing.append(part)
            
            if not missing:
                print("  [OK] PASS")
            else:
                print(f"  [FAIL] FAIL (Manquant: {missing})")
                all_passed = False
        else:
            print(f"  [ERROR] ERROR: {result.error_message}")
            all_passed = False
        print("-" * 70)

    if all_passed:
        print("\nSUCCESS: TOUTES LES REQUETES SONT SUPPORTEES CORRECTEMENT !\n")
    else:
        print("\nWARNING: CERTAINES REQUETES ONT ECHOUE.\n")

if __name__ == "__main__":
    test_specific_queries()
