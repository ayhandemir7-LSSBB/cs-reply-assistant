# Template retest findings

Ten new OpenAI calls completed using the same five briefs and configured model. Original results were not overwritten. No templates or application code were changed during this retest.

## Before and after: system outputs

- linkedin / gravel: 120 ? 117 words; allowed 120?200; new result: FAIL.
- email / road: 113 ? 116 words; allowed 120?180; new result: FAIL.
- linkedin / mountain: 120 ? 115 words; allowed 120?200; new result: FAIL.
- newsletter / gravel: 212 ? 202 words; allowed 200?280; new result: pass.
- instagram / mountain: 74 ? 75 words; allowed 80?150; new result: FAIL.

Length passes: 3/5 ? 1/5. Drafts with banned phrases: 3/5 ? 3/5. These length totals use actual channel-template bounds, not the incomplete production length check.

## Recommended next changes ? not implemented

1. Add newsletter (200?280) and Instagram (80?150) bounds to the production checker.
2. Use a bounded correction pass: send measured length and exact banned hits back to the model, then recheck. Cap retries and flag unresolved failures for the marketer.
3. Check channel structure explicitly: newsletter section titles and one closing CTA. Current quality checks miss these failures.
4. Add targeted qualifier/benefit test briefs, including Endurace tyre clearance by version and Grizl frame versus VCLS comfort. The new run omitted some problematic features, so omission cannot establish reliable correction.
5. Evaluate fresh briefs and multiple samples per brief before claiming improvement. Here there is only one before/after sample; randomness and updated generic format prompts limit causal conclusions.

The Ultimate product-name exception was verified locally in the previous change. These new system drafts do not mention Ultimate, so this run adds no evidence on that case.

[Open the retest presentation](comparison.html). Raw prompts and outputs: results.json.
