import numpy as np
from crewai.tools import tool


def calculate_r_value(
    alt: float | None,
    alp: float | None,
    sex: str | None,
    alt_baseline: float | None,
    alp_baseline: float | None,
    alt_elevation: float | None,
    alp_elevation: float | None,
) -> float:
    """
    Compute R value for liver injury type determination.

    ALT ULN
    While many labs still use a 40 U/L threshold, recent studies suggest lower, sex-specific ULNs
    are more accurate, with the American College of Gastroenterology recommending 33 U/L for men
    and 25 U/L for women. We will use the American College of Gastroenterology recommendations. If
    the sex is not provided, we will use 33 U/L (for men) by default.

    ALP ULN
    ALP ULN is 115 U/L here (LiverTox default).

    Bilirubin ULN
    Bilirubin ULN is 1.2 mg/dL here (LiverTox default).
    """
    alt_uln = 25 if sex == "female" else 25
    alp_uln = 115

    if alt_elevation and alp_elevation:
        return alt_elevation / alp_elevation

    if alt_baseline:
        alt_uln = alt_baseline
    if alp_baseline:
        alp_uln = alp_baseline

    return (alt / alt_uln) / (alp / alp_uln)


def recam_domain1(
    onset_after_start: int,
    onset_after_stop: int | None,
    long_half_life: bool,
) -> int:
    """
    Domain 1: Onset after start and onset after stop.
    """
    if onset_after_start <= 1:
        a_score = -6
    elif 2 <= onset_after_start <= 9:
        a_score = 3
    elif 10 <= onset_after_start <= 60:
        a_score = 4
    elif 61 <= onset_after_start <= 90:
        a_score = 2
    else:
        a_score = 0

    if long_half_life:
        b_score = 0
    elif not onset_after_stop:
        b_score = 0
    else:
        if onset_after_stop <= 30:
            b_score = 0
        elif 31 <= onset_after_stop <= 60:
            b_score = -1
        elif 61 <= onset_after_stop <= 90:
            b_score = -2
        elif 91 <= onset_after_stop <= 120:
            b_score = -4
        else:
            b_score = -6

    return a_score + b_score


def recam_domain2(
    r_value: float,
    days_to_50pct_alt_decline: float | None,
    drug_taken_at_50pct_alt_decline: bool,
    alt_declined_below_50pct: bool,
    days_to_50pct_alp_decline: float | None,
    drug_taken_at_50pct_alp_decline: bool,
    alp_declined_below_50pct: bool,
    days_to_50pct_bili_decline: float | None,
    drug_taken_at_50pct_bili_decline: bool,
    bili_declined_below_50pct: bool,
    persistent_high: bool,
) -> int:
    """
    Domain 2: Dechallenge or washout score based on R-value type.
    """
    # ------------------- Choose marker based on R-value -------------------
    if r_value > 5:
        # Using ALT as the marker
        dechallange_score = 0

        if alt_declined_below_50pct:
            if days_to_50pct_alt_decline <= 30:
                dechallange_score += 3
            elif 31 <= days_to_50pct_alt_decline <= 90:
                dechallange_score += 2
            elif 91 <= days_to_50pct_alt_decline <= 182:
                dechallange_score += 2
            elif 183 <= days_to_50pct_alt_decline <= 365:
                dechallange_score += 1

            if drug_taken_at_50pct_alt_decline:
                dechallange_score += -6

        elif persistent_high:
            dechallange_score += -6

    else:
        # Using ALP as the marker
        dechallange_score_alp = 0

        if alp_declined_below_50pct:
            if days_to_50pct_alp_decline <= 30:
                dechallange_score_alp += 3
            elif 31 <= days_to_50pct_alp_decline <= 90:
                dechallange_score_alp += 2
            elif 91 <= days_to_50pct_alp_decline <= 182:
                dechallange_score_alp += 2
            elif 183 <= days_to_50pct_alp_decline <= 365:
                dechallange_score_alp += 1

            if drug_taken_at_50pct_alp_decline:
                dechallange_score_alp += -6

        elif persistent_high:
            dechallange_score_alp += -6

        # Using Bilirubin as the marker
        dechallange_score_bili = 0

        if bili_declined_below_50pct:
            if days_to_50pct_bili_decline <= 30:
                dechallange_score_bili += 3
            elif 31 <= days_to_50pct_bili_decline <= 90:
                dechallange_score_bili += 2
            elif 91 <= days_to_50pct_bili_decline <= 182:
                dechallange_score_bili += 2
            elif 183 <= days_to_50pct_bili_decline <= 365:
                dechallange_score_bili += 1

            if drug_taken_at_50pct_bili_decline:
                dechallange_score_bili += -6

        elif persistent_high:
            dechallange_score_bili += -6

        dechallange_score = np.max(dechallange_score_alp, dechallange_score_bili)

    return dechallange_score


def recam_domain3(livertox_category: str | None) -> int:
    """
    Domain 3: Literature supporting liver injury (via LiverTox category).
    """
    if not livertox_category:
        return 0

    cat = livertox_category.upper()
    if cat in ["A", "B"]:
        return 2
    elif cat in ["C", "D", "E*"]:
        return 1
    elif cat in ["E", "X"]:
        return 0

    return 0


def recam_domain4(
    missing_IgM_anti_HAV: bool,
    IgM_anti_HAV: bool,
    missing_IgM_anti_HBc: bool,
    HBsAg: bool,
    IgM_anti_HBc: bool,
    r_value: float,
    missing_anti_HCV: bool,
    missing_HCV_RNA: bool,
    anti_HCV: bool,
    HCV_RNA: bool,
    chronic_HCV: bool,
    HCV_risk_100d_before_onset: bool,
    missing_IgM_anti_HEV: bool,
    IgM_anti_HEV: bool,
    ast: float | None,
    alt: float | None,
    standard_drinks_per_day: int | None,
    sex: str | None,
    missing_image_biliary_or_parenchymal_disease: bool,
    biliary_steuosis_or_obstruction: bool,
    less_than_50pct_malignant_infiltration: bool,
    is_minocycline_or_nitrofurantion_case: bool,
    ANA_autoimmune_hepatitis: float | None,
    ASMA_autoimmune_hepatitis: float | None,
    IgG_autoimmune_hepatitis: float | None,
    missing_ischemic_liver_injury_data: bool,
    ischemic_liver_injury_1w_before_onset: bool,
    missing_sepsis: bool,
    sepsis: bool,
) -> tuple[int, dict]:
    """
    Domain 4: Competing diagnoses. Needs specific rules.
    `competing_diagnoses_rule_out`: True if alternatives are effectively ruled out.
    """
    score = 0

    non_dili_evidence = {}

    # ------------------- Domain 4: Exclusion of competing diagnoses -------------------
    # Hepatitis A
    if missing_IgM_anti_HAV:
        score += -3
    elif IgM_anti_HAV:
        score += -6
        non_dili_evidence["IgM_anti_HAV"] = "Hepatitis A considered as competing diagnoses due to positive IgM anti-HAV."

    # Hepatitis B
    if missing_IgM_anti_HBc:
        score += -3
    else:
        if IgM_anti_HBc:
            score += -6
            non_dili_evidence["IgM_anti_HBc"] = "Hepatitis B considered as competing diagnoses due to positive IgM anti-HBc."
        elif HBsAg:
            score += -1

    # Hepatitis C
    if missing_anti_HCV or missing_HCV_RNA:
        score += -3
    else:
        if r_value <= 5:
            if HCV_RNA:
                score += -1
        else:
            if chronic_HCV:
                score += -1
            elif HCV_risk_100d_before_onset:
                score += -6
                non_dili_evidence["HCV_risk_100d_before_onset"] = "Hepatitis C considered as competing diagnoses due to no known chronic infection but having exposure risk of HCV in ≤ 100 days prior to onset."
            else:
                score += -1

    # Hepatitis E
    if missing_IgM_anti_HEV:
        score += -3
    elif IgM_anti_HEV:
        score += -6
        non_dili_evidence["IgM_anti_HEV"] = "Hepatitis E considered as competing diagnoses due to positive IgM anti-HEV."

    # Alcohol (AST and ALT values at onset)
    if ast and alt:
        if ast / alt >= 2 and ast <= 500:
            if missing_alcohol_history:
                score += -3
            else:
                if sex == "female":
                    if standard_drinks_per_day > 2 and standard_drinks_per_day <= 4:
                        score += -3
                    elif standard_drinks_per_day > 4:
                        score += -6
                        non_dili_evidence["standard_drinks_per_day"] = "Alcohol considered as competing diagnoses due to average of > 4 standard drinks/d for women."
                else:
                    if standard_drinks_per_day > 3 and standard_drinks_per_day <= 6:
                        score += -3
                    elif standard_drinks_per_day > 6:
                        score += -6
                        non_dili_evidence["standard_drinks_per_day"] = "Alcohol considered as competing diagnoses due to average of > 6 standard drinks/d for men."

    # biliary or parenchymal disease
    if missing_image_biliary_or_parenchymal_disease:
        score += -3
    elif biliary_steuosis_or_obstruction:
        score += -6
        non_dili_evidence[
            "biliary_steuosis_or_obstruction"] = "Biliary or parenchymal disease considered as competing diagnoses due to imaging data showing biliary steuosis(es) or obstruction."
    elif less_than_50pct_malignant_infiltration:
        score += -6
        non_dili_evidence["less_than_50pct_malignant_infiltration"] = "Biliary or parenchymal disease considered as competing diagnoses due to imaging data showing less than 50% malignant infiltration."

    # Autoimmune hepatitis
    if is_minocycline_or_nitrofurantion_case:
        if missing_ANA_autoimmune_hepatitis and missing_ASMA_autoimmune_hepatitis and missing_IgG_autoimmune_hepatitis:
            score += -3
        elif ANA_autoimmune_hepatitis >= 1/80 or ASMA_autoimmune_hepatitis >= 1/80 or IgG_autoimmune_hepatitis >= 1.1:
            score += 1
    else:
        if missing_ANA_autoimmune_hepatitis and missing_ASMA_autoimmune_hepatitis and missing_IgG_autoimmune_hepatitis:
            score += -3
        else:
            if ANA_autoimmune_hepatitis >= 1/80 or ASMA_autoimmune_hepatitis >= 1/80 or IgG_autoimmune_hepatitis >= 1.1:
                score += -1
            if (ANA_autoimmune_hepatitis >= 1/80 or ASMA_autoimmune_hepatitis >= 1/80) and IgG_autoimmune_hepatitis >= 1.1 and liver_biopsy_with_typical_features_of_AIH:
                score += -6
                non_dili_evidence[
                    "liver_biopsy_with_typical_features_of_AIH"] = "Autoimmune hepatitis considered as competing diagnoses due to (ANA ≥ 1:80 or ASMA ≥ 1:80) and IgG ≥1.1 ULN, and liver biopsy with typical features of AIH for non-minocycline and non-nitrofurantion cases."

    # Ischemic liver injury
    if missing_ischemic_liver_injury_data:
        score += -1
    elif ischemic_liver_injury_1w_before_onset:
        score += -2

    # Sepsis
    if r_value < 5:
        if missing_sepsis:
            score += -1
        elif sepsis:
            score += -2

    return (score, non_dili_evidence)


def recam_domain5(
    r_value: float,
    prior_exposure_dili_jaundice: bool,
    rechallenge_data: bool,
    rechallenge_ast_alt_elevation: bool,
    rechallenge_alp_elevation: bool,
    rechallenge_no_ast_alt_elevation: bool,
    rechallenge_no_alp_elevation: bool,
    liver_biopsy_specific_dili: bool,
    liver_biopsy_non_dili: bool,
    missing_IgM_anti_CMV: bool,
    IgM_anti_CMV: bool,
    CMV_DNA: bool,
    missing_IgM_anti_EBV: bool,
    IgM_anti_EBV: bool,
    EBV_DNA: bool,
    missing_IgM_anti_HSV: bool,
    IgM_anti_HSV: bool,
    HSV_DNA: bool,
    DRESS_or_SJS: bool,
) -> tuple[int, dict]:
    """
    Domain 5: Additional data.
    """
    score = 0
    non_dili_evidence = {}

    # Retrospective Rechallenge: h/o DILI w/ jaundice to same drug
    if prior_exposure_dili_jaundice:
        score += 1

    # Prospective Rechallenge (documented with labs)
    if rechallenge_data:
        if r_value > 5:
            if rechallenge_ast_alt_elevation:
                score += 6
            elif rechallenge_no_ast_alt_elevation:
                score += -3
        else:
            if rechallenge_alp_elevation:
                score += 6
            elif rechallenge_no_alp_elevation:
                score += -3

    # Liver Biopsy
    if liver_biopsy_specific_dili:
        score += 1
    elif liver_biopsy_non_dili:
        score += -6
        non_dili_evidence["liver_biopsy_non_dili"] = "Liver biopsy suggested non-DILI diagnosis."

    # CMV
    if IgM_anti_CMV and not CMV_DNA:
        score += -2
    elif not IgM_anti_CMV and CMV_DNA:
        score += -2
    elif IgM_anti_CMV and CMV_DNA:
        score += -6
        non_dili_evidence["IgM_anti_CMV"] = "Cytomegalovirus considered as competing diagnoses due to positive IgM anti-CMV and PCR positive."

    # EBV
    if IgM_anti_EBV and not EBV_DNA:
        score += -2
    elif not IgM_anti_EBV and EBV_DNA:
        score += -2
    elif IgM_anti_EBV and EBV_DNA:
        score += -6
        non_dili_evidence["IgM_anti_EBV"] = "Epstein-Barr virus considered as competing diagnoses due to positive IgM anti-EBV and PCR positive."

    # HSV
    if IgM_anti_HSV and not HSV_DNA:
        score += -2
    elif not IgM_anti_HSV and HSV_DNA:
        score += -2
    elif IgM_anti_HSV and HSV_DNA:
        score += -6
        non_dili_evidence["IgM_anti_HSV"] = "Herpes simplex virus considered as competing diagnoses due to positive IgM anti-HSV and PCR positive."

    # DRESS or SJS
    if DRESS_or_SJS:
        score += 1

    return (score, non_dili_evidence)


@tool("RECAM Score Calculator")
def calculate_recamscore_all(
    ast: float | None,
    alt: float | None,
    alp: float | None,
    sex: str | None,
    alt_baseline: float | None,
    alp_baseline: float | None,
    alt_elevation: float | None,
    alp_elevation: float | None,
    onset_after_start: int,
    onset_after_stop: int | None,
    long_half_life: bool,
    days_to_50pct_alt_decline: float | None,
    drug_taken_at_50pct_alt_decline: bool,
    alt_declined_below_50pct: bool,
    days_to_50pct_alp_decline: float | None,
    drug_taken_at_50pct_alp_decline: bool,
    alp_declined_below_50pct: bool,
    days_to_50pct_bili_decline: float | None,
    drug_taken_at_50pct_bili_decline: bool,
    bili_declined_below_50pct: bool,
    persistent_high: bool,
    livertox_category: str | None,
    missing_IgM_anti_HAV: bool,
    IgM_anti_HAV: bool,
    missing_IgM_anti_HBc: bool,
    HBsAg: bool,
    IgM_anti_HBc: bool,
    r_value: float,
    missing_anti_HCV: bool,
    missing_HCV_RNA: bool,
    anti_HCV: bool,
    HCV_RNA: bool,
    chronic_HCV: bool,
    HCV_risk_100d_before_onset: bool,
    missing_IgM_anti_HEV: bool,
    IgM_anti_HEV: bool,
    standard_drinks_per_day: int | None,
    missing_image_biliary_or_parenchymal_disease: bool,
    biliary_steuosis_or_obstruction: bool,
    less_than_50pct_malignant_infiltration: bool,
    is_minocycline_or_nitrofurantion_case: bool,
    ANA_autoimmune_hepatitis: float | None,
    ASMA_autoimmune_hepatitis: float | None,
    IgG_autoimmune_hepatitis: float | None,
    missing_ischemic_liver_injury_data: bool,
    ischemic_liver_injury_1w_before_onset: bool,
    missing_sepsis: bool,
    sepsis: bool,
    prior_exposure_dili_jaundice: bool,
    rechallenge_data: bool,
    rechallenge_ast_alt_elevation: bool,
    rechallenge_alp_elevation: bool,
    rechallenge_no_ast_alt_elevation: bool,
    rechallenge_no_alp_elevation: bool,
    liver_biopsy_specific_dili: bool,
    liver_biopsy_non_dili: bool,
    missing_IgM_anti_CMV: bool,
    IgM_anti_CMV: bool,
    CMV_DNA: bool,
    missing_IgM_anti_EBV: bool,
    IgM_anti_EBV: bool,
    EBV_DNA: bool,
    missing_IgM_anti_HSV: bool,
    IgM_anti_HSV: bool,
    HSV_DNA: bool,
    DRESS_or_SJS: bool,
):
    """
    Compute scores for all RECAM domains (1–5) and sum total.
    """
    r_value = calculate_r_value(
        alt=alt,
        alp=alp,
        sex=sex,
        alt_baseline=alt_baseline,
        alp_baseline=alp_baseline,
        alt_elevation=alt_elevation,
        alp_elevation=alp_elevation
    )

    score_domain_1 = recam_domain1(
        onset_after_start=onset_after_start,
        onset_after_stop=onset_after_stop,
        long_half_life=long_half_life
    )

    score_domain_2 = recam_domain2(
        r_value=r_value,
        days_to_50pct_alt_decline=days_to_50pct_alt_decline,
        drug_taken_at_50pct_alt_decline=drug_taken_at_50pct_alt_decline,
        alt_declined_below_50pct=alt_declined_below_50pct,
        days_to_50pct_alp_decline=days_to_50pct_alp_decline,
        drug_taken_at_50pct_alp_decline=drug_taken_at_50pct_alp_decline,
        alp_declined_below_50pct=alp_declined_below_50pct,
        days_to_50pct_bili_decline=days_to_50pct_bili_decline,
        drug_taken_at_50pct_bili_decline=drug_taken_at_50pct_bili_decline,
        bili_declined_below_50pct=bili_declined_below_50pct,
        persistent_high=persistent_high
    )

    score_domain_3 = recam_domain3(
        livertox_category=livertox_category
    )

    score_domain_4, non_dili_evidence_domain_4 = recam_domain4(
        missing_IgM_anti_HAV=missing_IgM_anti_HAV,
        IgM_anti_HAV=IgM_anti_HAV,
        missing_IgM_anti_HBc=missing_IgM_anti_HBc,
        HBsAg=HBsAg,
        IgM_anti_HBc=IgM_anti_HBc,
        r_value=r_value,
        missing_anti_HCV=missing_anti_HCV,
        missing_HCV_RNA=missing_HCV_RNA,
        anti_HCV=anti_HCV,
        HCV_RNA=HCV_RNA,
        chronic_HCV=chronic_HCV,
        HCV_risk_100d_before_onset=HCV_risk_100d_before_onset,
        missing_IgM_anti_HEV=missing_IgM_anti_HEV,
        IgM_anti_HEV=IgM_anti_HEV,
        ast=ast,
        alt=alt,
        standard_drinks_per_day=standard_drinks_per_day,
        sex=sex,
        missing_image_biliary_or_parenchymal_disease=missing_image_biliary_or_parenchymal_disease,
        biliary_steuosis_or_obstruction=biliary_steuosis_or_obstruction,
        less_than_50pct_malignant_infiltration=less_than_50pct_malignant_infiltration,
        is_minocycline_or_nitrofurantion_case=is_minocycline_or_nitrofurantion_case,
        ANA_autoimmune_hepatitis=ANA_autoimmune_hepatitis,
        ASMA_autoimmune_hepatitis=ASMA_autoimmune_hepatitis,
        IgG_autoimmune_hepatitis=IgG_autoimmune_hepatitis,
        missing_ischemic_liver_injury_data=missing_ischemic_liver_injury_data,
        ischemic_liver_injury_1w_before_onset=ischemic_liver_injury_1w_before_onset,
        missing_sepsis=missing_sepsis,
        sepsis=sepsis,
    )

    score_domain_5, non_dili_evidence_domain_5 = recam_domain5(
        r_value=r_value,
        prior_exposure_dili_jaundice=prior_exposure_dili_jaundice,
        rechallenge_data=rechallenge_data,
        rechallenge_ast_alt_elevation=rechallenge_ast_alt_elevation,
        rechallenge_alp_elevation=rechallenge_alp_elevation,
        rechallenge_no_ast_alt_elevation=rechallenge_no_ast_alt_elevation,
        rechallenge_no_alp_elevation=rechallenge_no_alp_elevation,
        liver_biopsy_specific_dili=liver_biopsy_specific_dili,
        liver_biopsy_non_dili=liver_biopsy_non_dili,
        missing_IgM_anti_CMV=missing_IgM_anti_CMV,
        IgM_anti_CMV=IgM_anti_CMV,
        CMV_DNA=CMV_DNA,
        missing_IgM_anti_EBV=missing_IgM_anti_EBV,
        IgM_anti_EBV=IgM_anti_EBV,
        EBV_DNA=EBV_DNA,
        missing_IgM_anti_HSV=missing_IgM_anti_HSV,
        IgM_anti_HSV=IgM_anti_HSV,
        HSV_DNA=HSV_DNA,
        DRESS_or_SJS=DRESS_or_SJS,
    )

    total = score_domain_1 + score_domain_2 + score_domain_3 + score_domain_4 + score_domain_5

    non_dili_evidence = non_dili_evidence_domain_4 | non_dili_evidence_domain_5

    return {
        "Domain1": score_domain_1,
        "Domain2": score_domain_2,
        "Domain3": score_domain_3,
        "Domain4": score_domain_4,
        "Domain5": score_domain_5,
        "TotalScore": total,
        "NonDILIEvidence": non_dili_evidence
    }


# Example usage:
if __name__ == "__main__":
    pass

    # example = calculate_recamscore_all(
    #     alt=600,
    #     alp=120,
    #     sex="male",
    #     alt_baseline=40,
    #     alp_baseline=120,
    #     alt_elevation=600,
    #     alp_elevation=120,
    #     onset_after_start=15,
    #     onset_after_stop=10,
    #     long_half_life=False,
    #     days_to_50pct_alt_decline=40,
    #     drug_taken_at_50pct_alt_decline=False,
    #     alt_declined_below_50pct=True,
    #     days_to_50pct_alp_decline=40,
    #     drug_taken_at_50pct_alp_decline=False,
    #     alp_declined_below_50pct=True,
    #     days_to_50pct_bili_decline=40,
    #     drug_taken_at_50pct_bili_decline=False,
    #     bili_declined_below_50pct=True,
    #     persistent_high=False,
    #     livertox_category="B",
    # )
    # print(example)
