"""bwkit — narrow v5 runtime helpers (single-writer lock, revision CAS, ...).

Schema-agnostic utilities invoked by skills through the CLI. Distinct from the
legacy `bw` package: bwkit targets the v5 `_bewater/` layout and never binds to
business schemas. See design spec §12 (Runtime Minimization).
"""
