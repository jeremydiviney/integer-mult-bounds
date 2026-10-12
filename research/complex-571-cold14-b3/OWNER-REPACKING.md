# Coordinated owner repacking of PR617

The input is PR617 commit `904d62855723c00f8acef9a287a10768598fdeb2`, independently replayed here through all 42 stages with no reused baseline or provider outputs. The new owner map preserves all 72 calls, every helper's identity and residual width, the invocation order, the capacity inventory and the jp8 ×60 / atm3 ×12 dispatch.

## Exact result and scope

- Conditional κ: `1635199825038547/1000000000000000000` = **0.001635199825038547**.
- Conservative κ: **0.001635199822189889**.
- Native complex lower: `327575616598658529771/200000000000000000000000`.
- Global paid profile: `{1:181848,2:24768,3:31776,4:13729,5:5040,6:1008,8:577,12:1,48:2150}`.
- Spare-capacity profile: `{1:24,4:1,8:1,12:1,48:2150}`; exactly 103,248 spare ranks, as before.
- Live 7,168; physical 7,682; deficit 2,560; total paid rank 520,704.

There are 1,432 changed owner placements. Prefix-packing those bins also changes 1,258 offsets on helpers whose owner remains the same. The 2,690 changed role records preserve the other fields. Moves are simultaneous: the exporter validates the complete resulting map rather than requiring each intermediate move to be a valid physical schedule.

This repacks the fixed supplier family. It does not evade the inherited all-size compiler, common-label/mutable-source, whole-call hosting, precision/tape, analytic-transfer or bit H1–H5 assumptions. The cited PR543 bit supplier is repriced in the package replay, not rebuilt there. No unconditional theorem, complete Lean certification or global packing optimum is claimed.

## Reproduce the nomination

Fetch PR617's pinned commit and provide its `data` directory:

```sh
python3 -B research/complex-571-cold14-b3/tools/replay_repacking.py \
  --base-data /path/to/pr617/research/complex-571-cold14-b3/data \
  --out /tmp/pr617-repacked
```

Compare PLAN bytes and decompressed OWNERS payloads with this package. The exporter checks both immutable input hashes, every listed original placement and width, final family uniqueness, windows, capacities, exact rank mass and the output content hash. It refuses `-O` before creating output. These are nomination checks; the unchanged physical verifier is the admission boundary.

## Strict admission

Use the five immutable source packages listed in the inherited README/NOTICE, including the archived PR569 source at `897213a855b7fb8a1b8b0e552a2f5c42e6c1b326`:

```sh
python3 -B research/complex-571-cold14-b3/verify.py --jobs 2 \
  --work /tmp/pr617-repacked-fresh \
  --source multicold=/path/to/pr568/research/complex-multicold \
  --source structural_gain=/path/to/pr571/research/structural-gain \
  --source larger_gain=/path/to/pr569/research/larger-gain \
  --source joint_prefix=/path/to/pr575/research/complex-joint-prefix \
  --source frame_coalescing=/path/to/pr583/research/kernel-frame-coalescing
```

The contributor evidence is in the sibling repacking audit directory. The package's default SPEC and MANIFEST bind the final inputs. Both exact moment engines, the conservative calculation and outer constraints remain unchanged; discovery's floating-point entropy objective is never used for admission. WITNESS's input pins and EXPECTED's global fields are copied from these recomputed values, with their binding hash refreshed. The generic witness tool present at this historical checkout does not support the later cold-end steps and is not used to claim a second independent replay.

## Search provenance

Uniform random two-owner swaps found no gain in one million trials. Favoring partners in partially occupied bins allowed coordinated rearrangements: one million seed-0 trials at temperature 1 followed by ten million seed-1 trials produced this spare-rank profile. A further ten million seed-2 trials at temperature 4 found no improvement. A restricted old-or-new placement model then removed 417 unnecessary placement changes while preserving every bin's load; its optimum applies only to that small choice model.

All search inputs and settings are retained in the sibling audit directory. The recorded-move exporter is the portable reproduction route and needs no numerical solver. PR620's separately published 61/11 dispatch lead informed a different experiment; this result keeps PR617's 60/12 mix and does not solve that lead. Attribution for the suppliers remains with PR617, PR604 and their credited predecessors. Prepared by Jeremy Diviney with OpenAI Codex assistance.
