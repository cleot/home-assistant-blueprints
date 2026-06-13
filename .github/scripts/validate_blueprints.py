#!/usr/bin/env python3
"""Validate Home Assistant blueprints in this repository.

Checks every *.yaml file that looks like a blueprint (has a top-level
`blueprint:` key) for the structure Home Assistant requires:

  - `blueprint` is a mapping
  - `blueprint.name` is present and non-empty
  - `blueprint.domain` is a valid blueprint domain
  - the file parses as YAML (HA custom tags like !input / !include are tolerated)

`source_url` is reported as a warning when missing (recommended for the
one-click import flow and update tracking, but not strictly required).

Exit code is non-zero if any error-level problem is found.
"""
from __future__ import annotations

import pathlib
import sys

import yaml

VALID_DOMAINS = {"automation", "script", "template"}


class HassLoader(yaml.SafeLoader):
    """SafeLoader that tolerates Home Assistant's custom YAML tags."""


def _construct_unknown(loader: yaml.Loader, tag_suffix: str, node: yaml.Node):
    # Resolve !input / !include / !secret etc. to plain Python values so the
    # rest of the document still loads. The resolved value is irrelevant here;
    # we only care about structure.
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    return None


HassLoader.add_multi_constructor("!", _construct_unknown)


def iter_yaml_files(root: pathlib.Path):
    for path in sorted(root.rglob("*.yaml")):
        if ".github" in path.parts:
            continue
        yield path


def main() -> int:
    root = pathlib.Path(".")
    errors: list[str] = []
    warnings: list[str] = []
    checked = 0

    for path in iter_yaml_files(root):
        try:
            data = yaml.load(path.read_text(encoding="utf-8"), Loader=HassLoader)
        except yaml.YAMLError as exc:
            errors.append(f"{path}: YAML parse error: {exc}")
            continue

        if not isinstance(data, dict) or "blueprint" not in data:
            continue  # not a blueprint file

        checked += 1
        bp = data["blueprint"]

        if not isinstance(bp, dict):
            errors.append(f"{path}: top-level 'blueprint' must be a mapping")
            continue

        name = bp.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{path}: blueprint is missing a non-empty 'name'")

        domain = bp.get("domain")
        if domain not in VALID_DOMAINS:
            errors.append(
                f"{path}: blueprint 'domain' is {domain!r}, "
                f"expected one of {sorted(VALID_DOMAINS)}"
            )

        if "source_url" not in bp:
            warnings.append(f"{path}: blueprint has no 'source_url' (recommended)")

    print(f"Checked {checked} blueprint(s).")

    for warning in warnings:
        print(f"::warning::{warning}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"::error::{error}")
        return 1

    print("All blueprints valid. ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
