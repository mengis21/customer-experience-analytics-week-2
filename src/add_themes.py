import os
import re
import pandas as pd


THEME_RULES = {
    "Account Access Issues": [r"login", r"log in", r"password", r"pin", r"otp", r"register", r"verification"],
    "Transaction Performance": [r"transfer", r"slow", r"loading", r"timeout", r"network", r"delay", r"balance update"],
    "User Interface & Experience": [r"ui", r"interface", r"design", r"layout", r"usability", r"navigation"],
    "Reliability": [r"crash", r"bug", r"error", r"freeze", r"stopped", r"fail"],
    "Customer Support": [r"support", r"help", r"service", r"contact", r"response"],
    "Feature Requests": [r"feature", r"fingerprint", r"biometric", r"face id", r"statement", r"notification"],
}


def assign_themes(text: str, keywords: str | None) -> str:
    hay = (text or "") + " " + (keywords or "")
    hay = hay.lower()
    found = []
    for theme, patterns in THEME_RULES.items():
        for pat in patterns:
            if re.search(pat, hay):
                found.append(theme)
                break
    if not found:
        return "Other"
    # stable unique order
    seen = set()
    ordered = []
    for t in found:
        if t not in seen:
            seen.add(t)
            ordered.append(t)
    return ", ".join(ordered)


def main():
    path = "data/clean_reviews_enriched.csv"
    if not os.path.exists(path):
        print("Missing enriched data. Run sentiment_keywords.py first.")
        return
    df = pd.read_csv(path)
    df["themes"] = [assign_themes(t, k) for t, k in zip(df.get("review"), df.get("keywords"))]
    df.to_csv(path, index=False)
    print(f"Updated themes in {path} (rows={len(df)})")


if __name__ == "__main__":
    main()
import os
import pandas as pd


THEME_RULES = {
    "Account Access Issues": [
        "login", "log in", "sign in", "otp", "pin", "password", "account locked", "verification"
    ],
    "Transaction Performance": [
        "transfer", "slow", "delay", "pending", "failed", "timeout", "network", "loading", "processing"
    ],
    "User Interface & Experience": [
        "ui", "ux", "design", "interface", "navigation", "layout", "dark mode"
    ],
    "Reliability / Bugs": [
        "crash", "bug", "error", "freeze", "hang", "issue"
    ],
    "Customer Support": [
        "support", "help", "call", "service", "response"
    ],
    "Feature Requests": [
        "feature", "fingerprint", "biometric", "statement", "budget", "analytics"
    ],
}


def assign_themes(text: str) -> str:
    text_l = str(text).lower()
    hits = []
    for theme, kws in THEME_RULES.items():
        if any(k in text_l for k in kws):
            hits.append(theme)
    if not hits:
        return "Other"
    return ", ".join(sorted(set(hits)))


def main():
    in_path = "data/clean_reviews_enriched.csv"
    if not os.path.exists(in_path):
        print("Missing enriched data. Run sentiment_keywords.py first.")
        return
    df = pd.read_csv(in_path)
    df["themes"] = df["review"].apply(assign_themes)
    out_path = "data/clean_reviews_enriched.csv"
    df.to_csv(out_path, index=False)
    print(f"Added themes and saved to {out_path}")


if __name__ == "__main__":
    main()
