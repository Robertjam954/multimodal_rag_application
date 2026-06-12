"""Manage per-document ACLs in Azure AI Search.

Usage:
    python scripts/manageacl.py list <docid>
    python scripts/manageacl.py add <docid> <oid>
    python scripts/manageacl.py remove <docid> <oid>
"""
from __future__ import annotations

import os
import sys


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    op, docid = sys.argv[1], sys.argv[2]
    oid = sys.argv[3] if len(sys.argv) > 3 else None
    service = os.getenv("AZURE_SEARCH_SERVICE")
    index = os.getenv("AZURE_SEARCH_INDEX")
    if not (service and index):
        print("AZURE_SEARCH_SERVICE and AZURE_SEARCH_INDEX required")
        return 2
    # Real impl uses azure-search-documents to update the acls field.
    print(f"[stub] {op} docid={docid} oid={oid} -> {service}/{index}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
