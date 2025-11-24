
def to_mgdl(value, unit):
    """Convert to mg/dL from mg/dL or mmol/L."""
    if value is None:
        return None
    u = unit.strip().lower()
    if u == "mg/dl" or u == "mg/dL":
        return float(value)
    if u == "mmol/l" or u == "mmol/l":
        return float(value) * 18.0
    raise ValueError(f"Unknown glucose unit: {unit}")

def diagnose(a1c, fpg, fpg_unit, ogtt2h, ogtt2h_unit, rpg=None, rpg_unit=None, rpg_symptoms=None, pregnancy_status=""):
    """
    Return diagnosis string based on ADA-style thresholds.
    - Diabetes if any threshold met
    - Prediabetes if within prediabetes ranges
    - Normal otherwise
    Gestational diabetes is noted if pregnancy_status indicates pregnant.
    """
    # Normalize values
    FPG = to_mgdl(fpg, fpg_unit) if fpg is not None else None
    OGTT2h = to_mgdl(ogtt2h, ogtt2h_unit) if ogtt2h is not None else None
    RPG = None
    if rpg is not None and rpg_unit is not None:
        try:
            RPG = to_mgdl(rpg, rpg_unit)
        except ValueError:
            RPG = None

    symptoms = None
    if isinstance(rpg_symptoms, str):
        s = rpg_symptoms.strip().lower()
        symptoms = (s in ("yes", "y", "true", "1"))
    else:
        symptoms = bool(rpg_symptoms) if rpg_symptoms is not None else None

    # Diabetes thresholds
    diabetic = False
    if a1c is not None and a1c >= 6.5:
        diabetic = True
    if FPG is not None and FPG >= 126:
        diabetic = True
    if OGTT2h is not None and OGTT2h >= 200:
        diabetic = True
    if RPG is not None and RPG >= 200 and symptoms:
        diabetic = True

    # Prediabetes thresholds
    prediabetes = False
    if a1c is not None and 5.7 <= a1c <= 6.4:
        prediabetes = True
    if FPG is not None and 100 <= FPG <= 125:
        prediabetes = True
    if OGTT2h is not None and 140 <= OGTT2h <= 199:
        prediabetes = True

    if pregnancy_status and pregnancy_status.strip().lower() == "pregnant":
        return "Gestational diabetes: apply obstetric thresholds (not implemented here)"

    if diabetic:
        return "Diabetes (probable); consider a repeat test on a different day for confirmation"
    if prediabetes:
        return "Prediabetes; monitor and implement risk-reduction strategies"
    return "Normal glucose regulation"

def prompt_float(prompt_text, allow_empty=False):
    while True:
        v = input(prompt_text).strip()
        if allow_empty and v == "":
            return None
        try:
            return float(v)
        except ValueError:
            print("Please enter a numeric value.")

def main():
    print("Diabetes classifier (rule-based). Enter data for one person to get a diagnosis.")
    while True:
        print("\nEnter data for one person (or type 'exit' to quit):")

        a1c_input = input("A1C (%): ").strip()
        if a1c_input.lower() in ("exit", "quit"):
            break
        a1c = float(a1c_input) if a1c_input != "" else None

        fpg = prompt_float("Fasting Plasma Glucose value: ")
        fpg_unit = input("FPG unit (mg/dL or mmol/L): ").strip() or "mg/dL"

        ogtt2h = prompt_float("2-hour OGTT glucose value: ")
        ogtt2h_unit = input("OGTT 2h unit (mg/dL or mmol/L): ").strip() or "mg/dL"

        rpg = prompt_float("Random Plasma Glucose value (if available): ")
        rpg_unit = input("RPG unit (mg/dL or mmol/L) [press Enter to skip]: ").strip() or None
        rpg_symptoms_input = input("RPG symptoms present? (y/n) [optional]: ").strip().lower()
        rpg_symptoms = None
        if rpg_symptoms_input in ("y", "yes", "true", "1"):
            rpg_symptoms = True
        elif rpg_symptoms_input in ("n", "no", "false", "0"):
            rpg_symptoms = False

        pregnancy_status = input("Pregnancy status (pregnant / nonpregnant / leave empty if not applicable): ").strip()

        # Compute diagnosis
        diagnosis = diagnose(
            a1c=a1c,
            fpg=fpg,
            fpg_unit=fpg_unit if fpg_unit else "mg/dL",
            ogtt2h=ogtt2h,
            ogtt2h_unit=ogtt2h_unit if ogtt2h_unit else "mg/dL",
            rpg=rpg,
            rpg_unit=rpg_unit,
            rpg_symptoms=rpg_symptoms,
            pregnancy_status=pregnancy_status,
        )

        print(f"Diagnosis: {diagnosis}")

        cont = input("Analyze another person? (y/n): ").strip().lower()
        if cont not in ("y", "yes"):
            break

    print("Goodbye.")

if __name__ == "__main__":
    main()
