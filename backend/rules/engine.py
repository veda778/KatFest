import json
import os


# Get absolute path to schemes.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMES_PATH = os.path.join(BASE_DIR, "schemes.json")


def load_schemes():
    with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def check_eligibility(user_data):
    schemes = load_schemes()
    eligible_schemes = []

    for scheme in schemes:

        # State check
        if scheme["state"].lower() != user_data.state.lower():
            continue

        conditions = scheme.get("conditions", {})
        match = True
        reasons = []

        # Gender check
        if "gender" in conditions:
            if user_data.gender.lower() != conditions["gender"].lower():
                match = False
            else:
                reasons.append(f"Gender matches ({user_data.gender})")

        # Age minimum check
        if "age_min" in conditions:
            if user_data.age < conditions["age_min"]:
                match = False
            else:
                reasons.append(f"Age ≥ {conditions['age_min']}")

        # Age maximum check
        if "age_max" in conditions:
            if user_data.age > conditions["age_max"]:
                match = False
            else:
                reasons.append(f"Age ≤ {conditions['age_max']}")

        # Marital status check
        if "marital_status" in conditions:
            if (
                user_data.marital_status is None
                or user_data.marital_status.lower() != conditions["marital_status"].lower()
            ):
                match = False
            else:
                reasons.append(
                    f"Marital status matches ({user_data.marital_status})"
                )

        # Disability check
        if "disability" in conditions:
            if user_data.disability != conditions["disability"]:
                match = False
            else:
                reasons.append("Disability condition matched")

        # Category check
        if "category" in conditions:
            if (
                user_data.category is None
                or user_data.category != conditions["category"]
            ):
                match = False
            else:
                reasons.append(f"Category matches ({user_data.category})")

        if match:
            eligible_schemes.append(
                {
                    "scheme_name": scheme["name"],
                    "eligibility_reason": reasons,
                }
            )

    return eligible_schemes