# Lineage / impact edges (spec §8.2)

The canonical dependency edges are `derived_from` and `evidence_refs` (both pin a mutable upstream
record revision). **Branch inheritance** and **baseline membership** are additional governance
edges. Compute downstream impact by scanning all four — never a hand-maintained reverse-impact list.

## Build edges, then call the helper

Assemble `{"dependent": <child id>, "dependency": <parent id>}` edges from:
- `derived_from` → dependent = the deriving record, dependency = its source (e.g. a solution depends
  on its concept; a hypothesis on its insights);
- `evidence_refs` → dependent = the assuming/claiming record, dependency = the `evidence:E-xxx@n`;
- branch inheritance → dependent = descendant-branch record, dependency = parent-branch record;
- baseline membership → dependent = every record frozen in a baseline, dependency = `baseline:B-xxx`.

Then shell out (the helper is stdlib-only, schema-agnostic; the CALLER builds edges):

    echo '{"edges": [...], "roots": ["assumption:A-001@4"]}' | bwkit scan impact

`lineage.transitive_dependents` returns `{"dependents": [...], "depth": {node: hops}}`. The
`dependents` list is the BT-record's `affected_refs`; the `depth` map drives the proposed backtrack
depth (§8.2 step 4). Roots are never listed as their own dependents.

## Five-step impact flow (§8.2)

1. find all transitive dependents; 2. append new invalidated/stale artifact revisions for affected
records; 3. list affected gate decisions and baselines; 4. propose the backtrack depth; 5. stop for
the accountable human to confirm routing.
