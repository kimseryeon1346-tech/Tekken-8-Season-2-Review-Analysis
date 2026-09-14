"""Rule-based multi-label issue tagging used in the Tekken 8 portfolio analysis.

The repository excludes raw Steam reviews. This module can be applied to a clean
CSV supplied by the user. Required columns are recommendationid, period,
recommendation_group, and review_text.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import pandas as pd


TAG_ORDER = [
    "Offensive_Pressure",
    "Defense_Movement",
    "Character_Homogenization",
    "Heat_System",
    "Moveset_Balance_Issue",
    "Dev_Direction_Trust",
]

ISSUE_CUES = [
    r"\b(?:bad|worse|worst|broken|unbalanced|imbalance|oppressive|excessive|forced|forcing|"
    r"remove(?:d)?|nerf(?:ed)?|lack(?:ing|s)?|fewer|difficult|harder|punish(?:ed)?|"
    r"ruin(?:ed)?|problem(?:s)?|issue(?:s)?|braindead|mindless|casino|gambl\w*|"
    r"coin[\s-]?flip(?:s)?|guess(?:ing)?|bug(?:s|ged)?|same|similar|identity|archetype|"
    r"weakness(?:es)?|strength(?:s)?|out of touch|ignor(?:e|ed|es|ing)|feedback|"
    r"not listen(?:ing)?|lost faith)\b",
    r"\b50\s*/\s*50s?\b",
    r"\bplus[\s-]?frames?\b",
]

TAG_RULES: dict[str, dict[str, Any]] = {
    "Offensive_Pressure": {
        "direct": [
            r"\bplus[\s-]?frames?\b",
            r"\b50\s*/\s*50s?\b",
            r"\bcoin[\s-]?flips?\b",
            r"\boffense[\s-]?heavy\b",
            r"\bmindless\s+rushdown\b",
            r"\b(?:overly|too|excessively|more)\s+aggress(?:ive|ion)\b",
        ],
        "conditional": [
            (
                [r"\b(?:aggress(?:ive|ion)|offen(?:se|sive)|pressure|rushdown|mix[\s-]?ups?)\b"],
                ISSUE_CUES,
            )
        ],
    },
    "Defense_Movement": {
        "direct": [
            r"\bdefen(?:se|ce|sive|cive)\b",
            r"\b(?:back[\s-]?dash(?:ing)?|sidestep(?:ping)?|side[\s-]?step(?:ping)?|"
            r"korean back dash|kbd)\b",
        ],
        "conditional": [([r"\bmovement\b", r"\bneutral\b", r"\bblocking\b"], ISSUE_CUES)],
    },
    "Character_Homogenization": {
        "direct": [
            r"\bhomogeni[sz](?:e|ed|ing|ation)\b",
            r"\bhomogenous\b",
            r"\bhomogeneous\b",
        ],
        "conditional": [
            (
                [r"\bcharacters?\b", r"\broster\b"],
                [
                    r"\b(?:same|similar|identity|identities|archetype|archetypes|unique|"
                    r"uniqueness|strengths?|weaknesses?|homogeni[sz]\w*|everyone|"
                    r"all characters|play the same)\b"
                ],
            )
        ],
    },
    "Heat_System": {
        "direct": [r"\bheat\b"],
        "conditional": [],
        "idiom_exclusion": r"\bheat of (?:the )?(?:battle|moment)\b",
        "system_override": r"\bheat\s+(?:system|mechanic|mode|engage|smash|burst|dash|meter|activation)\b",
    },
    "Moveset_Balance_Issue": {
        "direct": [
            r"\bmovesets?\b",
            r"\bmove[\s-]?sets?\b",
            r"\boff[\s-]?axis\b",
            r"\bframe data\b",
        ],
        "conditional": [
            (
                [r"\bmoves?\b"],
                [
                    r"\b(?:remove(?:d|ing)?|nerf(?:ed|ing)?|buff(?:ed|ing)?|broken|"
                    r"bug(?:s|ged)?|damage|tracking|homing|unblockable|oppressive|aggressive|"
                    r"stance|properties|property|hitbox(?:es)?|spam(?:ming)?|force(?:d|s|ing)?)\b",
                    r"\b50\s*/\s*50s?\b",
                    r"\bplus[\s-]?frames?\b",
                ],
            )
        ],
    },
    "Dev_Direction_Trust": {
        "direct": [
            r"\bout of touch\b",
            r"\b(?:lost|lose|no)\s+(?:all\s+)?(?:my\s+)?(?:faith|trust)\b",
            r"\b(?:ignore|ignored|ignores|ignoring)\s+(?:the\s+)?(?:community|feedback|playerbase|players?)\b",
            r"\bnot\s+listen(?:ing)?\s+to\s+(?:the\s+)?(?:community|feedback|playerbase|players?)\b",
        ],
        "conditional": [
            (
                [r"\b(?:devs?|developers?|development team|bandai namco|harada|game director)\b"],
                [
                    r"\b(?:feedback|listen(?:ing)?|ignore(?:d|s|ing)?|trust|faith|direction|"
                    r"vision|lie(?:d|s)?|dishonest|care|greed(?:y)?|betray(?:al|ed)?|"
                    r"community|ruin(?:ed|ing)?)\b"
                ],
            )
        ],
    },
}


def normalize_text(text: str) -> str:
    """Lowercase and normalize whitespace before regex matching."""

    return re.sub(r"\s+", " ", str(text).lower().replace("’", "'")).strip()


def pattern_matches(text: str, patterns: list[str]) -> list[str]:
    matches: list[str] = []
    for pattern in patterns:
        matches.extend(
            match.group(0).strip().lower()
            for match in re.finditer(pattern, text, flags=re.IGNORECASE)
        )
    return list(dict.fromkeys(value for value in matches if value))


def apply_tag_rule(text: str, tag_name: str) -> tuple[int, list[str]]:
    """Apply one tag rule and return its binary result and matched terms."""

    rule = TAG_RULES[tag_name]
    direct = pattern_matches(text, rule.get("direct", []))
    conditional_matches: list[str] = []
    for primary_patterns, context_patterns in rule.get("conditional", []):
        primary = pattern_matches(text, primary_patterns)
        context = pattern_matches(text, context_patterns)
        if primary and context:
            conditional_matches.extend(primary + context)

    matched = list(dict.fromkeys(direct + conditional_matches))
    is_match = bool(matched)

    if tag_name == "Heat_System" and is_match:
        idiom = re.search(rule["idiom_exclusion"], text, flags=re.IGNORECASE)
        override = re.search(rule["system_override"], text, flags=re.IGNORECASE)
        if idiom and not override and len(re.findall(r"\bheat\b", text, flags=re.IGNORECASE)) == 1:
            return 0, []

    return int(is_match), matched


def tag_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    """Apply all six rules to a clean review-level dataframe."""

    required = {"recommendationid", "period", "recommendation_group", "review_text"}
    missing = sorted(required.difference(reviews.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    tagged = reviews.copy()
    normalized = tagged["review_text"].fillna("").map(normalize_text)
    tag_columns: list[str] = []

    for tag_name in TAG_ORDER:
        results = normalized.map(lambda text: apply_tag_rule(text, tag_name))
        tag_column = f"tag_{tag_name}"
        tagged[tag_column] = results.map(lambda value: value[0]).astype("int8")
        tagged[f"matched_{tag_name}"] = results.map(lambda value: "|".join(value[1]))
        tag_columns.append(tag_column)

    tagged["issue_tag_count"] = tagged[tag_columns].sum(axis=1).astype("int8")
    return tagged


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()

    reviews = pd.read_csv(
        args.input_csv,
        dtype={"recommendationid": "string"},
        keep_default_na=False,
    )
    tagged = tag_reviews(reviews)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    tagged.to_csv(args.output_csv, index=False, encoding="utf-8-sig")
    print(f"Tagged {len(tagged):,} reviews -> {args.output_csv}")


if __name__ == "__main__":
    main()
