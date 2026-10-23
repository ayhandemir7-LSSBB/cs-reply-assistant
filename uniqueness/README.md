# M6 comparison

From the repository root, using the Python environment that runs the app:

```powershell
python uniqueness/run_comparison.py
```

This sends ten requests to OpenAI using the configured key and model: five generic
drafts and five real pipeline drafts. The system arm sends selected company KB
content. There are no automatic retries or extra judge calls. Existing results
are never overwritten; archive `results.json` before deliberately rerunning.
If a call fails, completed evidence is preserved and the run is labelled failed.

Open `uniqueness/comparison.html` in a browser for presentation or use its Print /
save as PDF button. `comparison.md` is the repo deliverable. `results.json` stores
the exact prompts, unedited outputs, automatic quality checks and source hashes.

To rebuild the presentation without paying for generation:

```powershell
python uniqueness/run_comparison.py --render-only
```

Review each output against `knowledge_base/primary/product_specs.md` and the brand
guidelines. Optional `review.json` supplies a `headline`, `summary` and a `cases`
object mapping case IDs (`"1"` through `"5"`) to lists of evidence notes. Rebuild
after adding notes. Be explicit about who reviewed the outputs and retain failures.
Do not treat a house-style pass as proof of factual correctness.

The controlled baseline is the same API model without company documents, not
the ChatGPT application. Both arms get the same output-format instructions.
The comparison measures the combined prompt/KB package; one run cannot establish
general superiority or isolate which component caused a difference.

The current report includes all four channels. The original three pairs are archived
in `results.original-three.json`. `--append-channels` adds the newsletter and Instagram
pairs only to an unchanged, complete three-case run; it makes four API calls.
Newsletter and Instagram template lengths are checked separately in the report
because the production quality checker currently has no length bounds for them.
