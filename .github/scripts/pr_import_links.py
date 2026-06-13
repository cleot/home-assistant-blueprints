#!/usr/bin/env python3
"""Build a PR comment with Home Assistant import links for changed blueprints.

Reads a file containing newline-separated paths (the blueprints changed in a
PR), keeps the ones that are actually blueprints, and prints a Markdown comment
with a "My Home Assistant" one-click import link for each — pointing at this
PR's head commit so reviewers can import and test the PR version before merge.

Prints nothing (and exits 0) when no blueprint changed, so the workflow can
skip commenting.

Env:
  REPO      owner/name of the repo hosting the head commit
  HEAD_SHA  commit SHA the import links should point at
"""
from __future__ import annotations

import os
import pathlib
import sys
import urllib.parse

import yaml

MARKER = "<!-- ha-import-links -->"


class HassLoader(yaml.SafeLoader):
    """SafeLoader that tolerates Home Assistant's custom YAML tags."""


def _construct_unknown(loader: yaml.Loader, tag_suffix: str, node: yaml.Node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    return None


HassLoader.add_multi_constructor("!", _construct_unknown)


def import_link(repo: str, sha: str, rel_path: str) -> str:
    blob_url = f"https://github.com/{repo}/blob/{sha}/{rel_path}"
    encoded = urllib.parse.quote(blob_url, safe="")
    return (
        "https://my.home-assistant.io/redirect/blueprint_import/"
        f"?blueprint_url={encoded}"
    )


def main() -> int:
    changed_file = pathlib.Path(sys.argv[1])
    repo = os.environ.get("REPO", "")
    sha = os.environ.get("HEAD_SHA", "")

    rows: list[tuple[str, str]] = []
    for rel in changed_file.read_text(encoding="utf-8").split():
        path = pathlib.Path(rel)
        if not path.is_file():
            continue  # deleted or renamed away
        try:
            data = yaml.load(path.read_text(encoding="utf-8"), Loader=HassLoader)
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict) or "blueprint" not in data:
            continue
        bp = data["blueprint"]
        name = bp.get("name", rel) if isinstance(bp, dict) else rel
        rows.append((str(name), import_link(repo, sha, rel)))

    if not rows:
        return 0

    lines = [
        MARKER,
        "🏠 **Blueprints changed in this PR** — import the PR version to test before merge:",
        "",
    ]
    lines += [f"- [Import **{name}**]({url})" for name, url in rows]
    lines += [
        "",
        "> Links point at this PR's head commit and require a Home Assistant "
        "instance connected to [My Home Assistant](https://my.home-assistant.io).",
    ]
    sys.stdout.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
