# Contributor replay evidence: PR617 owner repacking

This directory records the new owner-map contribution based on PR617 at `904d62855723c00f8acef9a287a10768598fdeb2`. Its source package is the sibling `complex-571-cold14-b3`. This is contributor validation, awaiting independent review; it does not replace the inherited conditional proof obligations.

`PREDECESSOR-RESULT.json` and `PREDECESSOR-RECEIPT.json` record our fresh 42-stage reproduction of PR617. The new package's `RESULT.json`, `RECEIPT.json`, stage logs and validation record describe the repacked witness. Raw compressed artifacts are pinned as inputs; cross-environment generated owner maps should be compared after decompression.

## Reproduction and search

The package's `tools/replay_repacking.py` reproduces the final nomination using only the standard library and the pinned original PR617 data. `data/REPACKING.json` binds both original input hashes and every simultaneous owner move. The package's unchanged `verify.py` performs strict admission; see its `OWNER-REPACKING.md` for all five pinned dependencies and the fresh-run command.

The `search/` directory retains the discovery scripts as run, their settings/results and intermediate owner maps. They are not part of the verifier trust boundary. The annealer uses a floating entropy surrogate, temporarily accepts uphill moves, and exports only its best incumbent. The biased version chooses 80% of prospective swap partners from partially occupied owners. The final recipe comes from these runs:

```sh
python3 anneal_owner_swaps_biased.py --data /path/to/pr617/data \
  --out /tmp/seed0 --trials 1000000 --seed 0 --temperature 1
python3 anneal_owner_swaps_biased.py --data /tmp/seed0 \
  --out /tmp/seed1 --trials 10000000 --seed 1 --temperature 1
python3 minimize_owner_delta.py --base /path/to/pr617/data \
  --candidate /tmp/seed1 --out /tmp/minimal --seconds 30
```

The last command uses OR-Tools 9.15.6755. Its `OPTIMAL` status refers only to choosing each changed helper's original or proposed owner while holding every bin's load fixed. It is not an optimal-packing certificate. It reduces 1,849 changed placements to 1,432. The final standard-library exporter replaces intermediate PLAN provenance with the directly pinned PR617 inputs and recomputes all offsets and profiles. Uniform seed-0 swaps and the later temperature-4 seed-2 continuation found no further gain; their search summaries are retained.

Python 3.12.3 and Linux x86_64 were used. The new work was prepared by Jeremy Diviney with OpenAI Codex assistance. Construction and prior-verifier credit remains with jeremykothe2 (PR617), DreamingOfClouds (PR604), and all predecessor contributors named in the package NOTICE. No supplier construction is attributed to this repacking.
