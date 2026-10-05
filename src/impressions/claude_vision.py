"""Ask Claude about an image through the `claude` CLI (subscription, no API key).

The image is read by Claude's Read tool from a local path. Answers are cached on disk by a key
so that a rerun never pays twice.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


def ask(image_path: str, prompt: str, model: str = "sonnet", timeout: int = 240) -> str:
    full = f"Lis l'image {image_path} avec l'outil Read, puis réponds.\n\n{prompt}"
    proc = subprocess.run(
        ["claude", "-p", full, "--model", model, "--allowedTools", "Read",
         "--output-format", "json"],
        capture_output=True, text=True, timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-500:])
    return json.loads(proc.stdout)["result"]


def ask_json(image_path: str, prompt: str, model: str = "sonnet") -> dict:
    text = ask(image_path, prompt, model)
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(f"no JSON in answer: {text[:200]}")
    return json.loads(m.group(0))


class Cache:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data: dict[str, dict] = {}
        if self.path.exists():
            for line in self.path.open():
                row = json.loads(line)
                self.data[row["key"]] = row

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def add(self, key: str, value: dict) -> None:
        row = {"key": key, **value}
        self.data[key] = row
        with self.path.open("a") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
