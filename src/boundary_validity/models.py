"""Data models for scenarios and episode labels.

See ADR-003 for the command contract schema.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class SignatureMatch:
    """A single regex match against a trajectory sub-command."""

    regex: str
    priority: int
    label: str
    hook_name: Optional[str]  # None for discovery, str for crossing
    matched_command: str


@dataclass(frozen=True)
class ExclusionMatch:
    """A single exclusion regex match; a sub-command that hit an exclusion is skipped."""

    regex: str
    reason: str
    matched_command: str


@dataclass
class EpisodeLabels:
    """Deterministic labels extracted from a trajectory per ADR-003.

    D = discovery occurred
    X = crossing attempt occurred (implies D)
    Y = benign task reached its accepted end state (supplied by caller)
    A = escalation depth (count of distinct crossing attempts)
    """

    D: bool = False
    X: bool = False
    Y: bool = False
    A: int = 0
    matched_signatures: list[SignatureMatch] = field(default_factory=list)
    matched_exclusions: list[ExclusionMatch] = field(default_factory=list)
