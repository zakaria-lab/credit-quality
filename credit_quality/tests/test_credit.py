from credit import calculate_risk

# ==========================================
# Partie A : Cas normaux
# ==========================================

def test_high_risk():
    result = calculate_risk(1000, 700, 30)
    assert result == "HIGH"

def test_medium_risk():
    result = calculate_risk(1000, 400, 30)
    assert result == "MEDIUM"

def test_low_risk():
    result = calculate_risk(1000, 100, 30)
    assert result == "LOW"

# ==========================================
# Partie B : Cas limites
# ==========================================

def test_zero_income():
    result = calculate_risk(0, 500, 30)
    assert result == -1

def test_negative_income():
    result = calculate_risk(-1000, 500, 30)
    assert result == -1

def test_zero_debt():
    result = calculate_risk(1000, 0, 30)
    assert result == "LOW"

def test_ratio_exactly_0_3():
    # ratio = 300 / 1000 = 0.3 -> ratio > 0.3 est Faux -> renvoie "LOW"
    result = calculate_risk(1000, 300, 30)
    assert result == "LOW"

def test_ratio_exactly_0_6():
    # ratio = 600 / 1000 = 0.6 -> ratio > 0.6 est Faux, ratio > 0.3 est Vrai -> renvoie "MEDIUM"
    result = calculate_risk(1000, 600, 30)
    assert result == "MEDIUM"
