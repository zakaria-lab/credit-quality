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
