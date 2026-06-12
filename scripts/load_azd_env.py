"""Dump azd env values to .env.local (for local backend dev)."""
import os
import subprocess


def main() -> int:
    result = subprocess.run(["azd", "env", "get-values"], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(result.stderr)
        return result.returncode
    with open(".env.local", "w") as f:
        f.write(result.stdout)
    print("wrote .env.local")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
