"""bwkit/lineage — transitive impact / dependents (stdlib-only, schema-agnostic).
Operates on caller-built dependent->dependency edges; never parses YAML. See spec
§8.2, §12.3. Resolves A3 (linear scan cost) by doing one reverse-BFS from the roots."""
from __future__ import annotations

from collections import deque


def transitive_dependents(edges: list[dict], roots: list[str]) -> dict:
    """Reverse-reachability from `roots` over dependent->dependency edges.
    edge = {"dependent": str, "dependency": str} (dependent depends on dependency).
    Returns {"dependents": sorted[node ids], "depth": {node: hops from nearest root}}.
    Roots are never listed as dependents."""
    rev: dict[str, list[str]] = {}
    for e in edges:
        rev.setdefault(e["dependency"], []).append(e["dependent"])

    root_set = set(roots)
    depth: dict[str, int] = {}
    dq: deque[tuple[str, int]] = deque((r, 0) for r in roots)
    while dq:
        node, d = dq.popleft()
        for dep in rev.get(node, []):
            if dep not in depth or d + 1 < depth[dep]:
                depth[dep] = d + 1
                dq.append((dep, d + 1))
    depth = {n: d for n, d in depth.items() if n not in root_set}  # roots aren't their own dependents
    return {"dependents": sorted(depth), "depth": depth}
