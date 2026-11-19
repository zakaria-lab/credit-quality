# Projet Credit Quality - TP Qualité & Tests Unitaires

Ce dossier contient la résolution complète du TP **Qualité du code et tests unitaires (SonarQube + pytest)**.

## 🚀 Guide d'Exécution Rapide

### 1. Activer l'environnement virtuel
Depuis PowerShell :
```powershell
.venv\Scripts\Activate.ps1
```

### 2. Lancer les tests unitaires avec pytest
```powershell
python -m pytest -v
```

### 3. Mesurer la couverture de code
```powershell
python -m pytest --cov=credit --cov-report=term-missing
```

Générer le rapport HTML interactif :
```powershell
python -m pytest --cov=credit --cov-report=html
# Ouvrir le rapport :
Start-Process htmlcov\index.html
```

### 4. Lancer l'analyse SonarScanner
```powershell
$env:SONAR_TOKEN = "VOTRE_TOKEN_SONARCLOUD"
sonar-scanner -Dsonar.host.url=https://sonarcloud.io
```

Consultez le compte-rendu détaillé dans [RAPPORT_TP_COMPLET.md](../RAPPORT_TP_COMPLET.md).
