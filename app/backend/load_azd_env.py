"""Loads azd environment values into os.environ so local dev mirrors deployed config."""
import json
import os
import shutil
import subprocess


def load_azd_env() -> None:
    if not shutil.which("azd"):
        return
    try:
        result = subprocess.run(
            ["azd", "env", "get-values", "--output", "json"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if result.returncode != 0:
            return
        values = json.loads(result.stdout or "{}")
        for k, v in values.items():
            os.environ.setdefault(k, str(v))
    except Exception:
        pass
