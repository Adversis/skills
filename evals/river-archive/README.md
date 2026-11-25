# River Archive skill evaluation

Use Git and Python 3 to prepare a local checkout. The scorer also uses PyYAML and jsonschema. Run the commands from the skills repository. Choose a new directory for each case.

```sh
python3 evals/river-archive/evaluate.py prepare export-worker /tmp/river-worker
```

Give an evaluator only the installed skills, the prepared checkout, and the request below. Keep this guide and the scoring criteria outside the evaluator's inputs.

1. Ask `/adversis-security:security-review` to review the tracked change from `HEAD^` to `HEAD` in CI mode. Request a source review. Ask it to write `review/assessment.json` in the checkout. Do not supply test results.
2. Ask `/security-verify` to verify the change covered by that review. Supply the candidate register. Authorize the fixture's local Python unit tests. Request `verification/assessment.json`. Keep provider settings out of scope. Preserve the first record.
3. Score both outputs. Repeat with `docs-only` and `deployment` in separate directories.

```sh
python3 evals/river-archive/evaluate.py score export-worker /tmp/river-worker review /tmp/river-worker/review/assessment.json
python3 evals/river-archive/evaluate.py score export-worker /tmp/river-worker verification /tmp/river-worker/verification/assessment.json
```

| Change | Evidence to check after scoring |
|---|---|
| Export worker | Review cites the queue write before the membership check. The worker still denies rendering. A claim that a document was disclosed exceeds the evidence. Verification cites the separate allowed and denied test results. Inspect the named log or captured output. |
| Documentation | The changed sentence names the maintainer. The review explains why it leaves runtime behavior, permissions, and release settings unchanged. |
| Deployment | The change selects production. Inspect the limitation and the requested provider evidence. The effective approval policy is unknown. |

For each record, read the summary and actions. Check that the writer names the actor, uses consistent terms, and gives one clear action per instruction. Check that IDs, paths, and quoted evidence retain their original spelling.
