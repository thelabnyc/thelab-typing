#!/usr/bin/env bash
# Update the local OpenAPI 3.1 JSON schema file.
#
# This script downloads the latest OpenAPI 3.1 schema from the official
# OpenAPI Initiative specification. The schema is used by test_e2e.py
# to validate generated OpenAPI specs.
#
# Usage: bin/update-openapi-schema.sh
#
# To find the latest schema version, check:
#   https://spec.openapis.org/oas/3.1/schema/
#
# Schema naming convention:
#   https://spec.openapis.org/oas/3.1/schema/{YYYY-MM-DD}

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SCHEMA_URL="https://spec.openapis.org/oas/3.1/schema/2025-09-15"
OUTPUT_FILE="${PROJECT_ROOT}/thelabtyping/tests/api/openapi/fixtures/openapi-3.1-schema.json"

echo "Downloading OpenAPI 3.1 schema..."
echo "  URL: ${SCHEMA_URL}"
echo "  Output: ${OUTPUT_FILE}"

curl -sL "${SCHEMA_URL}" -o "${OUTPUT_FILE}"

echo "Done. Schema updated."
echo
echo "Schema \$id: $(grep -m1 '"\$id"' "${OUTPUT_FILE}" | cut -d'"' -f4)"
