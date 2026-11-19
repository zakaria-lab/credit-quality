# COMPTE-RENDU DE TRAVAUX PRATIQUES
## Déploiement des Systèmes Intelligents
### TP : Qualité du code et tests unitaires (SonarQube + pytest)

---

## 1. Introduction et Objectifs du TP

Ce travail pratique a pour objectif de mettre en place une démarche complète d'assurance qualité logicielle sur un projet Python :
1. **Analyse statique avec SonarQube Cloud et SonarLint (SonarQube for IDE)** : détection automatique des anomalies (Bugs, Vulnérabilités de sécurité, Code Smells, Duplications de code) et respect du Quality Gate.
2. **Tests unitaires et couverture avec pytest & pytest-cov** : développement de cas de tests (cas normaux, cas limites, tests de régression) et mesure de la couverture de code.

---

## 2. Exercice 1 : Analyse de la qualité avec SonarQube

### 2.1 Code initial et analyse des défauts

Le fichier `credit.py` initialement fourni présente la structure suivante :

```python
import os
import math

def calculate_risk(income, debt, age):
    if income <= 0:
        return -1
    
    ratio = debt / income
    
    if ratio > 0.6:
        return "HIGH"
    elif ratio > 0.3:
        return "MEDIUM"
    else:
        return "LOW"

def calculate_risk2(income, debt, age):
    if income <= 0:
        return -1
    
    ratio = debt / income
    
    if ratio > 0.6:
        return "HIGH"
    elif ratio > 0.3:
        return "MEDIUM"
    else:
        return "LOW"
```

#### Inventaire des problèmes détectés :
1. **Imports inutilisés (Code Smells - Règle `python:S1128`)** :
   - `import os` (ligne 1) n'est jamais utilisé.
   - `import math` (ligne 2) n'est jamais utilisé.
2. **Paramètres non utilisés (Code Smells - Règle `python:S1172`)** :
   - Le paramètre `age` dans `calculate_risk(income, debt, age)` n'intervient à aucun moment dans le calcul du risque.
   - Le paramètre `age` dans `calculate_risk2(income, debt, age)` est également inutilisé.
3. **Duplication de code massive (Duplications)** :
   - La fonction `calculate_risk2` est une copie conforme ligne par ligne de `calculate_risk` (13 lignes dupliquées, soit 100% de duplication sur la logique métier et ~50% du fichier total).
4. **Code mort / Inutilisé (Dead Code)** :
   - `calculate_risk2` n'est jamais appelée par les modules clients ou les tests unitaires.

---

### 2.2 Configuration SonarQube Cloud et SonarScanner

#### Fichier de configuration : `sonar-project.properties`
Ce fichier est placé à la racine du projet (`credit_quality/sonar-project.properties`) :

```properties
sonar.projectKey=credit-quality
sonar.organization=votre-organisation
sonar.projectName=Credit Quality
sonar.projectVersion=1.0

sonar.sources=.
sonar.sourceEncoding=UTF-8

sonar.exclusions=.venv/**,tests/**,htmlcov/**
```

#### Commandes d'exécution de l'analyse SonarScanner CLI
1. Définir le jeton d'authentification dans le terminal PowerShell :
   ```powershell
   $env:SONAR_TOKEN = "VOTRE_JETON_SONARCLOUD"
   ```
2. Lancer l'analyse :
   ```powershell
   sonar-scanner -Dsonar.host.url=https://sonarcloud.io
   ```
3. Résultat attendu dans la console :
   ```text
   INFO: ANALYSIS SUCCESSFUL, you can find the results at: https://sonarcloud.io/dashboard?id=credit-quality
   INFO: Note that you will be able to access the updated dashboard once the server has finished processing the submitted analysis report
   INFO: EXECUTION SUCCESS
   ```

---

### 2.3 SonarQube for IDE (SonarLint) dans VS Code

- **Installation** : Extension `SonarQube for IDE` (SonarSource) installée via la marketplace VS Code (`Ctrl+Shift+X`).
- **Analyse locale instantanée** : Dès l'ouverture de `credit.py`, l'onglet **Problems** (`Ctrl+Shift+M`) liste directement les alertes suivantes :
  - `[SonarLint] Remove this unused import 'os'. (python:S1128)`
  - `[SonarLint] Remove this unused import 'math'. (python:S1128)`
  - `[SonarLint] Remove this unused function parameter 'age'. (python:S1172)`
  - `[SonarLint] Remove this duplicated code block. (python:S1172 / duplication)`

---

### 2.4 Code corrigé : `credit.py`

```python
def calculate_risk(income, debt, _age=None):
    """
    Calcule le niveau de risque de crédit en fonction du ratio d'endettement.

    :param income: Revenu de l'emprunteur (doit être strictement positif)
    :param debt: Montant de la dette
    :param _age: Âge (conservé pour compatibilité avec l'API existante, préfixé
                 d'un tiret bas selon la convention SonarLint/PEP8 pour les paramètres non utilisés)
    :return: -1 si revenu invalide (<= 0), sinon 'HIGH', 'MEDIUM' ou 'LOW'
    """
    if income <= 0:
        return -1

    ratio = debt / income

    if ratio > 0.6:
        return "HIGH"
    elif ratio > 0.3:
        return "MEDIUM"
    else:
        return "LOW"
```

#### Améliorations apportées :
- Suppression des deux imports superflus `os` et `math`.
- Suppression de la fonction dupliquée `calculate_risk2`.
- Gestion propre de `_age=None` pour respecter la rétrocompatibilité des appels existants sans déclencher l'alerte de paramètre inutilisé.

---

### 2.5 Tableau comparatif Avant / Après correction

| Indicateur | Avant correction | Après correction |
| :--- | :--- | :--- |
| **Problèmes de fiabilité (Bugs)** | 0 | 0 |
| **Problèmes de sécurité (Vulnerabilities)** | 0 | 0 |
| **Problèmes de maintenabilité (Code Smells)** | **4** (`import os`, `import math`, `age` x2) | **0** |
| **Duplication de code** | **52.2%** (1 bloc dupliqué, 13 lignes) | **0.0%** (0 ligne dupliquée) |
| **Quality Gate** | **FAILED** (échec lié au seuil de duplication > 3%) | **PASSED** (vert sur tous les indicateurs) |

---

### 2.6 Réponses aux questions de l'Exercice 1

#### 1. Quelle différence existe-t-il entre un Bug et un Code Smell ?
- **Bug** : Erreur de programmation entraînant un dysfonctionnement effectif, un calcul erroné ou une interruption brutale du programme lors de l'exécution (ex: pointeur nul, division par zéro non interceptée). Le bug impacte directement la **fiabilité** (Reliability).
- **Code Smell** : Problème de structure, de lisibilité ou de non-respect des bonnes pratiques de conception qui n'empêche pas le programme de fonctionner, mais rend le code difficile à comprendre, à tester et à faire évoluer (ex: code dupliqué, fonctions trop complexes, imports inutiles). Le Code Smell génère de la **dette technique** et pénalise la **maintenabilité**.

#### 2. Pourquoi la duplication du code augmente-t-elle les coûts de maintenance ?
- **Multiplication des corrections** : Tout bug corrigé dans une portion de code doit être répercuté manuellement sur l'ensemble de ses copies, augmentant considérablement le risque d'oubli et d'incohérence.
- **Risque de divergence** : Avec le temps, les différentes copies évoluent séparément, rendant le comportement global imprévisible.
- **Volume et lisibilité** : Le volume superflu de lignes de code allonge le temps de lecture, de compréhension et de revue de code.
- **Coût des tests** : Nécessité de doubler ou tripler les tests unitaires pour tester les mêmes logiques.

#### 3. Quel est le rôle du Quality Gate ?
Le Quality Gate est un ensemble de critères et de seuils d'acceptabilité (ex: 0 nouveau bug bloquant, 0 nouvelle faille de sécurité, couverture de tests ≥ 80%, duplication < 3%) qu'une version de code doit impérativement valider pour être intégrée, fusionnée (Pull Request) ou déployée en production. Il joue le rôle de garde-fou automatisé empêchant l'accumulation de dette technique ("Clean as You Code").

#### 4. Quelle différence existe-t-il entre SonarScanner CLI et SonarQube for IDE (SonarLint) ?
- **SonarQube for IDE (SonarLint)** est un analyseur local intégré à l'éditeur (VS Code). Il fonctionne en temps réel (au fil de la frappe) pour offrir un retour immédiat au développeur avant même le commit ("shift-left").
- **SonarScanner CLI** est un outil en ligne de commande déclenché manuellement ou automatiquement dans un pipeline CI/CD. Il analyse l'intégralité du projet, calcule les métriques globales (couverture, duplication cross-fichiers) et envoie le rapport au serveur central SonarQube/SonarCloud pour validation du Quality Gate.

#### 5. Pourquoi faut-il relancer l'analyse après correction ?
Il est indispensable de relancer l'analyse pour :
1. Confirmer formellement que les problèmes détectés ont bien disparu.
2. Vérifier qu'aucune régression (nouveau bug ou nouveau code smell) n'a été introduite pendant le refactoring.
3. Valider que le projet franchit désormais avec succès le Quality Gate (`PASSED`).

---

## 3. Exercice 2 : Tests unitaires avec pytest

### 3.1 Organisation et installation

- **Environnement virtuel** : `.venv` initialisé avec Python 3.13.
- **Dépendances installées** : `pytest` (v9.2.0) et `pytest-cov` (v7.1.0).
- **Arborescence mise en place** :
  ```text
  credit_quality/
  |-- .venv/
  |-- htmlcov/
  |-- tests/
  |   `-- test_credit.py
  |-- credit.py
  |-- credit_initial.py
  `-- sonar-project.properties
  ```

---

### 3.2 Fichier complet des tests unitaires : `tests/test_credit.py`

Le fichier regroupe l'ensemble des scénarios de la **Partie A (Cas normaux)** et de la **Partie B (Cas limites)** :

```python
from credit import calculate_risk

# ==========================================
# Partie A : Cas normaux
# ==========================================

def test_high_risk():
    """Vérifie le risque élevé lorsque ratio > 0.6 (700/1000 = 0.7)."""
    result = calculate_risk(1000, 700, 30)
    assert result == "HIGH"

def test_medium_risk():
    """Vérifie le risque moyen lorsque 0.3 < ratio <= 0.6 (400/1000 = 0.4)."""
    result = calculate_risk(1000, 400, 30)
    assert result == "MEDIUM"

def test_low_risk():
    """Vérifie le risque faible lorsque ratio <= 0.3 (100/1000 = 0.1)."""
    result = calculate_risk(1000, 100, 30)
    assert result == "LOW"

# ==========================================
# Partie B : Cas limites
# ==========================================

def test_zero_income():
    """Vérifie qu'un revenu nul renvoie -1 sans provoquer de ZeroDivisionError."""
    result = calculate_risk(0, 500, 30)
    assert result == -1

def test_negative_income():
    """Vérifie qu'un revenu négatif renvoie -1."""
    result = calculate_risk(-1000, 500, 30)
    assert result == -1

def test_zero_debt():
    """Vérifie qu'une dette nulle donne ratio = 0.0 -> renvoie 'LOW'."""
    result = calculate_risk(1000, 0, 30)
    assert result == "LOW"

def test_ratio_exactly_0_3():
    """
    Cas limite : ratio exactement égal à 0.3 (300/1000 = 0.3).
    La condition ratio > 0.3 étant stricte, elle est fausse, donc renvoie 'LOW'.
    """
    result = calculate_risk(1000, 300, 30)
    assert result == "LOW"

def test_ratio_exactly_0_6():
    """
    Cas limite : ratio exactement égal à 0.6 (600/1000 = 0.6).
    La condition ratio > 0.6 étant stricte, elle est fausse.
    La condition suivante ratio > 0.3 est vraie, donc renvoie 'MEDIUM'.
    """
    result = calculate_risk(1000, 600, 30)
    assert result == "MEDIUM"
```

---

### 3.3 Exécution des tests et résultats

Commande exécutée :
```bash
python -m pytest -v
```

Trace d'exécution obtenue :
```text
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\hp\Downloads\TPSonarQube\credit_quality
plugins: cov-7.1.0
collecting ... collected 8 items

tests/test_credit.py::test_high_risk PASSED                              [ 12%]
tests/test_credit.py::test_medium_risk PASSED                            [ 25%]
tests/test_credit.py::test_low_risk PASSED                               [ 37%]
tests/test_credit.py::test_zero_income PASSED                            [ 50%]
tests/test_credit.py::test_negative_income PASSED                        [ 62%]
tests/test_credit.py::test_zero_debt PASSED                              [ 75%]
tests/test_credit.py::test_ratio_exactly_0_3 PASSED                      [ 87%]
tests/test_credit.py::test_ratio_exactly_0_6 PASSED                      [100%]

============================== 8 passed in 0.22s ==============================
```

---

### 3.4 Partie C : Détection d'erreurs (Test de mutation)

Une mutation volontaire a été introduite dans la fonction `calculate_risk` :
```python
# Condition modifiée :
if ratio > 0.8:  # au lieu de ratio > 0.6
```

#### 1. Quel test échoue ?
Le test **`test_high_risk`** échoue (`1 failed, 7 passed`).

#### 2. Pourquoi échoue-t-il ?
Pour le cas de test `calculate_risk(1000, 700, 30)` :
- Le ratio calculé est $700 / 1000 = 0.7$.
- Avec la condition altérée `if ratio > 0.8:`, le test $0.7 > 0.8$ s'évalue à **Faux** (`False`).
- L'évaluation bascule vers la clause suivante `elif ratio > 0.3:`, qui s'évalue à **Vrai** ($0.7 > 0.3$).
- La fonction retourne donc `"MEDIUM"` au lieu de `"HIGH"`.
- L'assertion `assert result == "HIGH"` échoue et pytest génère l'erreur :
  ```text
  E   AssertionError: assert 'MEDIUM' == 'HIGH'
  E     - HIGH
  E     + MEDIUM
  ```

#### 3 & 4. Correction et ré-exécution :
La condition a été rétablie à `if ratio > 0.6:`. Les 8 tests passent à nouveau avec succès (`8 passed`).

---

### 3.5 Mesure de la couverture de code

#### A. Rapport sur le code initial (avec `calculate_risk2`) :
```text
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
credit.py      20      8    60%   20-30
-----------------------------------------
TOTAL          20      8    60%
```
**Analyse des lignes non couvertes** : Les lignes 20 à 30 correspondent au corps de la fonction dupliquée `calculate_risk2`. Comme aucun test n'appelle cette fonction, le taux de couverture est plafonné à **60%**, ce qui démontre comment la couverture dynamique permet de repérer le code mort.

#### B. Rapport sur le code nettoyé et optimisé :
Commande exécutée :
```bash
python -m pytest --cov=credit --cov-report=term-missing
```

Résultat obtenu :
```text
=============================== tests coverage ================================
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
credit.py       9      0   100%
-----------------------------------------
TOTAL           9      0   100%
============================== 8 passed in 0.52s ==============================
```

Génération du rapport HTML :
```bash
python -m pytest --cov=credit --cov-report=html
```
Le rapport interactif est généré dans `credit_quality/htmlcov/index.html`. Toutes les branches et déclarations sont vertes avec **100% de couverture**.

---

### 3.6 Réponses aux questions de l'Exercice 2

#### 1. Quel est le rôle de l'instruction `assert` ?
En Python et dans les frameworks de test comme pytest, l'instruction `assert <condition>` valide qu'une condition logique attendue est vraie.
- Si la condition est vérifiée (`True`), le programme poursuit son cours.
- Si la condition est fausse (`False`), Python déclenche une exception de type `AssertionError`, signalant l'échec immédiat du test et affichant la comparaison entre la valeur réelle et la valeur attendue.

#### 2. Quelle différence existe-t-il entre PASS et FAIL ?
- **PASS** : Le test s'est exécuté jusqu'au bout, toutes les assertions ont été satisfaites et aucune exception anormale n'est survenue. Le composant testé se comporte conformément aux spécifications.
- **FAIL** : Au moins une assertion a retourné `False` ou une exception inattendue a été soulevée. Le résultat effectif diverge du résultat attendu, révélant une régression ou un bug logique.

#### 3. Pourquoi faut-il tester les valeurs limites (boundary testing) ?
Les anomalies logiques se concentrent très fréquemment aux frontières de décision des conditions (ex: opérateurs `<` versus `<=`, seuils 0, valeurs négatives). Tester spécifiquement les limites (ex: 0, 0.3, 0.6) permet :
- De détecter les erreurs d'un cran ("off-by-one errors").
- De s'assurer de la bonne gestion des cas extrêmes (ex: division par zéro évitée si `income = 0`).
- De clarifier l'inclusion ou l'exclusion stricte des bornes d'intervalles.

#### 4. Une couverture de 100% garantit-elle l'absence de bugs ?
**Non.** La métrique de couverture (Line Coverage) indique simplement que chaque ligne de code a été traversée au moins une fois par le flux d'exécution lors des tests.
Cependant, elle ne garantit pas :
- Que les assertions écrites sont exhaustives et pertinentes.
- Que toutes les combinaisons d'entrées et types de données invalides ont été explorées.
- Que des cas métiers manquants (spécifications omises dans le code) sont traités.

#### 5. Quelle différence existe-t-il entre pytest et SonarQube ?
- **pytest** est un outil de test **dynamique** : il exécute le programme pour valider son comportement fonctionnel par rapport à des scénarios d'entrées/sorties prédéfinis.
- **SonarQube** est un outil d'analyse **statique** (SAST) et de gouvernance globale : il examine le code source sans l'exécuter pour y traquer les failles de sécurité, vulnérabilités, non-respect des conventions de codage, dette technique et duplications.
- **Synergie** : pytest produit les rapports d'exécution et de couverture que SonarQube ingère pour alimenter son Quality Gate global.

---

## 4. Synthèse des Livrables

Tous les livrables demandés sont prêts et disponibles dans l'espace de travail :
1. `credit_quality/credit.py` : code source corrigé et nettoyé.
2. `credit_quality/credit_initial.py` : code source initial conservé pour comparaison.
3. `credit_quality/sonar-project.properties` : configuration officielle pour SonarScanner.
4. `credit_quality/tests/test_credit.py` : suite de tests couvrant 100% du code (Partie A, B, C).
5. `credit_quality/htmlcov/index.html` : rapport HTML complet de couverture pytest-cov.
6. Le présent rapport complet contenant l'ensemble des réponses, tableaux comparatifs et analyses techniques.
