from pydantic import BaseModel, Field


class RecamKeyInfo(BaseModel):
    """Key information model for RECAM"""
    drug_name: str = Field(description="name of the drug (generic name)")
    onset_after_start: int = Field(description="number of days between hepatotoxicity onset and start of drug exposure")
    onset_after_stop: int = Field(
        description="number of days between hepatotoxicity onset and stop of drug exposure. If not found, set to None")
    long_half_life: bool = Field(description="whether the drug has a long half life")
    sex: str = Field(description="Sex, either 'male' or 'female'")
    ast: float = Field(description="AST (Aspartate Aminotransferase) reading at the time of injury onset, in U/L")
    alt: float = Field(description="ALT (Alanine Aminotransferase) reading at the time of injury onset, in U/L")
    alp: float = Field(description="ALP (Alkaline Phosphatase) reading at the time of injury onset, in U/L")
    bili: float = Field(description="Bilirubin reading at the time of injury onset, in mg/dL")
    alt_baseline: float = Field(
        description="ALT (Alanine Aminotransferase) reading at baseline (before drug exposure), in U/L. If not found in the input data, set to None")
    alp_baseline: float = Field(
        description="ALP (Alkaline Phosphatase) reading at baseline (before drug exposure), in U/L. If not found in the input data, set to None")
    bili_baseline: float = Field(
        description="Bilirubin reading at baseline (before drug exposure), in mg/dL. If not found in the input data, set to None")
    alt_elevation: float = Field(
        description="ALT elevation, in how many times of ALT ULN or the baseline. If not found in the input data, set to None")
    alp_elevation: float = Field(
        description="ALP elevation, in how many times of ALP ULN or the baseline. If not found in the input data, set to None")
    bili_elevation: float = Field(
        description="Bilirubin elevation, in how many times of Bilirubin ULN or the baseline. If not found in the input data, set to None")
    days_to_50pct_alt_decline: float = Field(
        description="number of days to 50% decline in ALT elevation (compared to the peak ALT elevation)")
    drug_taken_at_50pct_alt_decline: bool = Field(
        description="whether the drug is still taken at 50% decline in ALT elevation")
    alt_declined_below_50pct: bool = Field(
        description="whether the ALT has declined below 50% of the peak ALT elevation")
    days_to_50pct_alp_decline: float = Field(
        description="number of days to 50% decline in ALP elevation (compared to the peak ALP elevation)")
    drug_taken_at_50pct_alp_decline: bool = Field(
        description="whether the drug is still taken at 50% decline in ALP elevation")
    alp_declined_below_50pct: bool = Field(
        description="whether the ALP has declined below 50% of the peak ALP elevation")
    days_to_50pct_bili_decline: float = Field(
        description="number of days to 50% decline in Bilirubin elevation as compared to the peak Bilirubin elevation")
    drug_taken_at_50pct_bili_decline: bool = Field(
        description="whether the drug is still taken at 50% decline in Bilirubin")
    bili_declined_below_50pct: bool = Field(
        description="whether the Bilirubin has declined below 50% at 50% decline in Bilirubin")
    persistent_high: bool = Field(
        description="whether the ALT, ALP or Bilirubin (whichever used by R-value criteria above) is > 90% of peak value at anytime >182 days and prior to any transplant without other explanation recurrent or persistent elevation")
    livertox_category: str = Field(description="LiverTox category, either 'A', 'B', 'C', 'D', 'E', or 'X'")
    missing_IgM_anti_HAV: bool = Field(
        description="whether IgM anti-HAV data is missing. HAV stands for Hepatitis A virus")
    IgM_anti_HAV: bool = Field(
        description="whether IgM anti-HAV is positive (if total anti-HAV is negative, consider IgM negative as well). HAV stands for Hepatitis A virus")
    missing_IgM_anti_HBc: bool = Field(
        description="whether IgM anti-HBc data is missing. HBc stands for Hepatitis B core antigen. Note: (−) anti-HBc total means IgM is negative, but (+) anti-HBc total does not inform IgM result")
    HBsAg: bool = Field(description="whether HBsAg is positive. HBsAg stands for Hepatitis B surface antigen")
    IgM_anti_HBc: bool = Field(
        description="whether IgM anti-HBc is positive. HBc stands for Hepatitis B core antigen. If total anti-HBc is negative, consider IgM negative; anti-HBc igG may be + or −")
    missing_anti_HCV: bool = Field(description="whether anti-HCV data is missing. HCV stands for Hepatitis C virus")
    missing_HCV_RNA: bool = Field(description="whether HCV RNA data is missing. HCV stands for Hepatitis C virus")
    anti_HCV: bool = Field(description="whether anti-HCV is positive. HCV stands for Hepatitis C virus")
    HCV_RNA: bool = Field(description="whether HCV RNA is positive. HCV stands for Hepatitis C virus")
    chronic_HCV: bool = Field(
        description="whether known chronic infection of HCV is present. HCV stands for Hepatitis C virus")
    HCV_risk_100d_before_onset: bool = Field(
        description="whether exposure risk is present less than 100 days before the onset of hepatotoxicity. HCV stands for Hepatitis C virus")
    missing_IgM_anti_HEV: bool = Field(
        description="whether IgM anti-HEV data is missing. HEV stands for Hepatitis E virus")
    IgM_anti_HEV: bool = Field(description="whether IgM anti-HEV is positive. HEV stands for Hepatitis E virus")
    standard_drinks_per_day: int = Field(
        description="number of standard drinks per day within 6 weeks of injury onset. A standard drink in the U.S. contains 0.6 fluid ounces (14 grams) of pure alcohol. For example, a standard drink is equivalent to about 12 ounces of beer, 5 ounces of wine, or 1.5 ounces of 80-proof distilled spirits. If not found, set to 0.")
    missing_image_biliary_or_parenchymal_disease: bool = Field(
        description="whether imaging data for biliary or parenchymal disease is missing. Imaging data includes ultrasound (US), computed tomography scan (CT), magnetic resonance imaging (MRI), magnetic resonance cholangiopancreatography (MRCP), cholangiogram, etc.")
    biliary_steuosis_or_obstruction: bool = Field(
        description="whether imaging data shows biliary steuosis(es) or obstruction. Imaging data includes ultrasound (US), computed tomography scan (CT), magnetic resonance imaging (MRI), magnetic resonance cholangiopancreatography (MRCP), cholangiogram, etc.")
    less_than_50pct_malignant_infiltration: bool = Field(
        description="whether imaging data shows infiltrating malignancy occupying ≥ 50% of the liver. Imaging data includes ultrasound (US), computed tomography scan (CT), magnetic resonance imaging (MRI), magnetic resonance cholangiopancreatography (MRCP), cholangiogram, etc.")
    is_minocycline_or_nitrofurantion_case: bool = Field(
        description="whether the drug belongs to minocycline or nitrofurantion family. If needed, search the drug name in the internet to determine if it belongs to this family.")
    ANA_autoimmune_hepatitis: float = Field(
        description="ANA (antinuclear antibodies) reading at the time of injury onset, in ratio. For example, if the ANA reading is 1:80, set to a float value of 1/80.")
    ASMA_autoimmune_hepatitis: float = Field(
        description="ASMA (anti-smooth muscle antibodies) reading at the time of injury onset, in ratio. For example, if the ASMA reading is 1:80, set to a float value of 1/80.")
    IgG_autoimmune_hepatitis: float = Field(
        description="IgG reading suggesting autoimmune hepatitis at the time of injury onset, in U/L.")
    missing_ischemic_liver_injury_data: bool = Field(
        description="whether ischemic liver injury data is missing. If no information is found for possible hypoxia, hypotension, shock or acute congestive hepatopathy (history incomplete or inadequate), set to True.")
    ischemic_liver_injury_1w_before_onset: bool = Field(
        description="whether ischemic liver injury (possible hypoxia, hypotension, shock or acute congestive hepatopathy) is present 1 week before the onset of hepatotoxicity.")
    missing_sepsis: bool = Field(
        description="whether sepsis data is missing. If no information is found for sepsis or SIRS (systemic inflammatory response syndrome), set to True.")
    sepsis: bool = Field(description="whether sepsis or SIRS (systemic inflammatory response syndrome) is present.")
    prior_exposure_dili_jaundice: bool = Field(
        description="whether the patient has a history of prior exposure to the drug and found to have DILI with jaundice after that prior exposure to the drug. Documentation by lab results is not necessary.")
    rechallenge_data: bool = Field(
        description="whether rechallenge data is available and the rechallenge data is documented with lab results (e.g., AST, ALT, ALP).")
    rechallenge_ast_alt_elevation: bool = Field(
        description="whether rechallenge of the drug resulted in AST or ALT elevation more than 3x ULN (or baseline) within 90 Days after the rechallenge.")
    rechallenge_alp_elevation: bool = Field(
        description="whether rechallenge of the drug resulted in ALP elevation more than 2x ULN (or baseline) within 90 Days after the rechallenge.")
    rechallenge_no_ast_alt_elevation: bool = Field(
        description="whether rechallenge of the drug showed non-significant AST or ALT elevation (less than 2x ULN or baseline).")
    rechallenge_no_alp_elevation: bool = Field(
        description="whether rechallenge of the drug showed non-significant ALP elevation (less than 2x ULN or baseline).")
    liver_biopsy_specific_dili: bool = Field(
        description="whether liver biopsy data shows features consistent with a specific DILI.")
    liver_biopsy_non_dili: bool = Field(
        description="whether liver biopsy data suggests non-DILI diagnosis (e.g. infiltrating cancer, ischemic injury, alcoholic hepatitis).")
    missing_IgM_anti_CMV: bool = Field(
        description="whether IgM anti-CMV data is missing. CMV stands for Cytomegalovirus.")
    IgM_anti_CMV: bool = Field(description="whether IgM anti-CMV is positive. CMV stands for Cytomegalovirus.")
    CMV_DNA: bool = Field(description="whether CMV DNA is detected by PCR. CMV stands for Cytomegalovirus.")
    missing_IgM_anti_EBV: bool = Field(
        description="whether IgM anti-EBV data is missing. EBV stands for Epstein-Barr virus.")
    IgM_anti_EBV: bool = Field(description="whether IgM anti-EBV is positive. EBV stands for Epstein-Barr virus.")
    EBV_DNA: bool = Field(description="whether EBV DNA is detected by PCR. EBV stands for Epstein-Barr virus.")
    missing_IgM_anti_HSV: bool = Field(
        description="whether IgM anti-HSV data is missing. HSV stands for Herpes simplex virus.")
    IgM_anti_HSV: bool = Field(description="whether IgM anti-HSV is positive. HSV stands for Herpes simplex virus.")
    HSV_DNA: bool = Field(description="whether HSV DNA is detected by PCR. HSV stands for Herpes simplex virus.")
    DRESS_or_SJS: bool = Field(
        description="whether Drug Reaction with Eosinophila and Systemic Symptoms (DRESS) or Steven Johnsons Syndrome (SJS) is present.")


class RecamResult(BaseModel):
    """Result model for RECAM"""
    score: int = Field(description="RECAM score")
    non_dili_evidence: dict = Field(description="non-DILI evidence")


class RecamAssessmentReport(BaseModel):
    """Report model for RECAM"""
    report_title: str = Field(description="Title of the report")
    generation_date: str = Field(description="Report generation date")
    dili_causality_assessment_summary: str = Field(description="A DILI causality assessment summary")
    key_findings: list = Field(
        description="List of key findings with their sources (if available)",
        default_factory=list
    )
    recam_score_analysis: list = Field(
        description="Detailed report sections",
        default_factory=list
    )
    supporting_evidence: list = Field(
        description="List of supporting evidence",
        default_factory=list
    )
    causality_assessment_conclusion: str = Field(description="DILI causality assessment conclusion")
    sources: list = Field(
        description="All sources used in the report",
        default_factory=list
    )


class RecamReviewReport(BaseModel):
    """Report model for RECAM"""
    report_title: str = Field(description="Title of the report")
    generation_date: str = Field(description="Report generation date")
    expert_summary: str = Field(description="A concise expert summary")
    key_findings: list = Field(
        description="List of key findings with their sources (if available)",
        default_factory=list
    )
    inconsistent_findings: list = Field(
        description="List of inconsistencies",
        default_factory=list
    )
    next_steps: list = Field(
        description="Recommended next steps",
        default_factory=list)
    sources: list = Field(
        description="All sources used in the report",
        default_factory=list
    )
