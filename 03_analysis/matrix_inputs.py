"""
Monte Carlo inputs — IROs + Risks/Opportunities per topic.

Every base value is sourced:
- IRO Scale/Scope/Remediability/Probability: informed by Aqualia 2025
  review IRO density + our sector-core / blind-spot positioning
  (see short_list_lock.md and aqualia_2025_baseline.md).
- Financial magnitude low/base/high: from financials.md tables (scaled
  to 1-5 via scoring_rubric.md §3.1 thresholds).
- Stakeholder salience weights: stakeholder_salience.md §3.
"""

from __future__ import annotations

# Stakeholder salience weights (normalised, sum to 1).
# Keys match aqualia_2025_baseline.md §2.
STAKEHOLDER_WEIGHTS: dict[str, float] = {
    "public_authorities": 0.120,
    "customers": 0.120,
    "shareholders": 0.120,
    "employees": 0.120,
    "investors": 0.080,
    "suppliers": 0.080,
    "society": 0.080,
    "local_communities": 0.080,
    "business_partners": 0.080,
    "environment": 0.080,
    "academy": 0.040,
}

# IROs per topic. Only the high-weight IROs are modelled (covers ~70% of
# topic variance per financials.md sensitivity).
# current=True forces probability to max per Aqualia methodology.
TOPIC_IROS: dict[str, list[dict]] = {
    "T1 Water Resilience & Equitable Access": [
        # E3 sustainability of water resource (9 IROs — core)
        {"id": "E3-deplete",       "stakeholders": ["customers","public_authorities","local_communities","environment"],
         "scale": 5, "scope": 5, "rem": 4, "prob": 5, "current": True},
        {"id": "E3-quality",       "stakeholders": ["customers","public_authorities","society","environment"],
         "scale": 4, "scope": 4, "rem": 3, "prob": 4, "current": True},
        # E1 climate mitigation + adaptation (9 IROs)
        {"id": "E1-adaptation",    "stakeholders": ["customers","public_authorities","local_communities","environment"],
         "scale": 4, "scope": 5, "rem": 4, "prob": 4, "current": False},
        {"id": "E1-emissions",     "stakeholders": ["society","environment","public_authorities"],
         "scale": 3, "scope": 4, "rem": 3, "prob": 4, "current": True},
        # S4 service resilience & security (8 IROs)
        {"id": "S4-continuity",    "stakeholders": ["customers","public_authorities","local_communities"],
         "scale": 5, "scope": 4, "rem": 3, "prob": 4, "current": False},
        # S3 affected communities (restored — blind spot)
        {"id": "S3-equity-access", "stakeholders": ["local_communities","customers","society"],
         "scale": 4, "scope": 3, "rem": 3, "prob": 5, "current": True},  # Colombia now
    ],
    "T2 Digital & Cyber Infrastructure": [
        # Tech innovation (5 IROs)
        {"id": "Tech-pace",        "stakeholders": ["customers","employees","investors","public_authorities"],
         "scale": 3, "scope": 4, "rem": 3, "prob": 4, "current": False},
        # Digitalisation (2 IROs — BLIND SPOT; we reposition with higher scale)
        {"id": "Dig-adoption",     "stakeholders": ["customers","employees","suppliers"],
         "scale": 3, "scope": 4, "rem": 2, "prob": 4, "current": True},
        {"id": "Dig-data-gov",     "stakeholders": ["customers","employees","public_authorities"],
         "scale": 3, "scope": 3, "rem": 3, "prob": 4, "current": False},
        # Cybersecurity (4 IROs)
        {"id": "Cyber-incident",   "stakeholders": ["customers","public_authorities","shareholders","investors"],
         "scale": 4, "scope": 4, "rem": 2, "prob": 3, "current": False},
        {"id": "Cyber-OT-IT",      "stakeholders": ["customers","employees","public_authorities","local_communities"],
         "scale": 4, "scope": 4, "rem": 2, "prob": 3, "current": False},
    ],
    "T3 Green Finance & Integrity": [
        # Compliance culture (11 IROs — highest density)
        {"id": "Compl-CSRD",       "stakeholders": ["investors","shareholders","public_authorities"],
         "scale": 3, "scope": 4, "rem": 3, "prob": 5, "current": True},
        {"id": "Compl-CSDDD",     "stakeholders": ["suppliers","investors","public_authorities","local_communities"],
         "scale": 3, "scope": 4, "rem": 3, "prob": 4, "current": False},
        # Anti-corruption (3 IROs)
        {"id": "Anti-corruption",  "stakeholders": ["shareholders","investors","public_authorities","society"],
         "scale": 3, "scope": 3, "rem": 2, "prob": 3, "current": False},
        # Green finance (6 IROs)
        {"id": "Green-fin-access", "stakeholders": ["investors","shareholders","public_authorities"],
         "scale": 3, "scope": 4, "rem": 3, "prob": 4, "current": False},
        # Supply-chain HR (4 IROs)
        {"id": "SC-human-rights",  "stakeholders": ["suppliers","society","investors"],
         "scale": 3, "scope": 4, "rem": 3, "prob": 3, "current": False},
    ],
}

# Financial R&Os per topic.
# mag_score as 1-5 via scoring_rubric.md §3.1:
#   1 <0.1% rev (<€1.4M)   2: 0.1-0.5%   3: 0.5-2% (€7-28M)
#   4: 2-5% (€28-70M)   5: >5% (>€70M)
# Triangular given as (low_score, base_score, high_score).
# Horizon: "short" | "medium" | "long" (discount 1.0 / 0.8 / 0.6).
TOPIC_ROS: dict[str, list[dict]] = {
    "T1 Water Resilience & Equitable Access": [
        # Net of opportunity: revenue at risk + CAPEX
        {"id": "R-stress-revenue",  "type": "risk",        "mag_lbh": (3, 4, 5), "prob": 5, "horizon": "medium"},   # A03
        {"id": "R-capex-uwwtd",     "type": "risk",        "mag_lbh": (4, 5, 5), "prob": 4, "horizon": "medium"},   # A06 (converted)
        {"id": "R-fines-wfd",       "type": "risk",        "mag_lbh": (2, 3, 4), "prob": 3, "horizon": "short"},
        {"id": "O-reuse-market",    "type": "opportunity", "mag_lbh": (2, 3, 4), "prob": 4, "horizon": "medium"},   # A04
        {"id": "O-nature-credits",  "type": "opportunity", "mag_lbh": (1, 2, 4), "prob": 3, "horizon": "long"},
    ],
    "T2 Digital & Cyber Infrastructure": [
        {"id": "R-cyber-incident",  "type": "risk",        "mag_lbh": (2, 3, 5), "prob": 3, "horizon": "short"},    # A08
        {"id": "R-nis2-gdpr",       "type": "risk",        "mag_lbh": (2, 3, 4), "prob": 3, "horizon": "short"},    # A12
        {"id": "R-digital-capex",   "type": "risk",        "mag_lbh": (3, 4, 4), "prob": 4, "horizon": "medium"},   # A11
        {"id": "O-tender-uplift",   "type": "opportunity", "mag_lbh": (2, 3, 4), "prob": 4, "horizon": "short"},    # A09
        {"id": "O-pred-maint-opex", "type": "opportunity", "mag_lbh": (2, 2, 3), "prob": 4, "horizon": "medium"},
    ],
    "T3 Green Finance & Integrity": [
        {"id": "R-coc-spread",      "type": "risk",        "mag_lbh": (2, 3, 4), "prob": 4, "horizon": "medium"},   # A13
        {"id": "R-csrd-compliance", "type": "risk",        "mag_lbh": (2, 3, 3), "prob": 4, "horizon": "medium"},   # A16
        {"id": "R-csddd-liab",      "type": "risk",        "mag_lbh": (1, 2, 4), "prob": 2, "horizon": "long"},
        {"id": "O-green-bond-prem", "type": "opportunity", "mag_lbh": (2, 3, 4), "prob": 4, "horizon": "medium"},   # A14 & §3.3
        {"id": "O-coc-saving",      "type": "opportunity", "mag_lbh": (2, 3, 4), "prob": 4, "horizon": "medium"},   # A15
        {"id": "O-tender-esg",      "type": "opportunity", "mag_lbh": (1, 2, 3), "prob": 4, "horizon": "short"},
    ],
}

HORIZON_DISCOUNT: dict[str, float] = {"short": 1.00, "medium": 0.80, "long": 0.60}

# Perturbation magnitude for Monte Carlo.
# Each base integer score becomes a triangular(base-PERTURB, base, base+PERTURB)
# clipped to [1, 5]. 0.7 gives meaningful but bounded spread.
PERTURB = 0.7
