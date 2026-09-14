# Tekken 8 Season 2 / v2.00.01 issue-tag analysis

## Data and method

- Clean comparison window: PRE 2025-03-17 22:00 UTC to 2025-03-31 22:00 UTC; POST to 2025-04-14 22:00 UTC.
- Reviews: PRE 193, POST 4,041.
- Recommended rate: PRE 61.1%, POST 6.8% (-54.36 pp).
- Manual validation: core keywords 45/45 plus defense supplemental 5/5.
- Six rule-based multi-label tags use word boundaries, phrase priority, conditional terms, and explicit exclusions.

## Largest PRE/POST share changes

- Defense_Movement: PRE 7.8% → POST 17.6% (+9.82 pp)
- Character_Homogenization: PRE 2.1% → POST 10.4% (+8.37 pp)
- Dev_Direction_Trust: PRE 6.2% → POST 12.3% (+6.13 pp)

These are observed review-share changes, not causal patch-effect estimates. The large PRE/POST recommendation-mix difference materially affects aggregate comparisons.

## POST Not Recommended

- Offensive_Pressure: 18.5% (698/3767)
- Defense_Movement: 18.5% (697/3767)
- Dev_Direction_Trust: 12.9% (486/3767)

Within Not Recommended reviews, Character_Homogenization rose from 2.7% (2/75) to 10.9% (410/3767). Defense_Movement was 18.7% before and 18.5% after, so its aggregate increase partly reflects the much larger Not Recommended share after the event.

## POST Recommended

POST Recommended has n=274; topic mentions are not automatically complaints.

- Defense_Movement: 5.1% (14/274)
- Dev_Direction_Trust: 4.7% (13/274)
- Offensive_Pressure: 4.4% (12/274)

Recommended reviews can mention the same systems as praise, qualified acceptance, or requested improvement. Interpretation therefore retains recommendation_group and the original review text.

## Representative context

Full-text QA examples are stored in `tagging_qa_examples.csv`. Representative POST Not Recommended recommendationids include 191933786. The sampled contexts repeatedly discuss excessive 50/50 pressure, reduced defensive counterplay, character identity loss, Heat mechanics, moveset properties, and developer direction.

## Limitations

- PRE and POST sample sizes are highly imbalanced.
- Steam reviews are self-selected and do not represent all players.
- Keyword and regex tagging cannot fully resolve sarcasm, negation, or every local context.
- Manual validation samples are small: five reviews per keyword.
- Tags are multi-label and overlapping shares should not be summed.
- Observational data cannot establish the causal effect of the patch.

## Conclusion

After Season 2 / v2.00.01, aggregate review shares increased most for defense/movement, character homogenization, and developer-direction topics. The four-group comparison shows that recommendation composition explains part of those aggregate shifts: among Not Recommended reviews, character homogenization increased clearly while defense/movement stayed near its already-high PRE level. This supports an interpretation of a broader post-update reaction centered on character identity and offensive design, without claiming that the patch alone caused the observed review changes.
