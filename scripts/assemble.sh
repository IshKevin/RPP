#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK_DIR="$ROOT_DIR/runtime"
mkdir -p "$WORK_DIR/web" "$WORK_DIR/engine"

ZIP4="${ZIP4:-RevenuePressAI_Platform_ZIP4_FullStack_QA_v1.4.zip}"
ZIP5="${ZIP5:-RevenuePressAI_Platform_ZIP5_Engine_Integrations_v1.4.zip}"

if [[ ! -f "$ROOT_DIR/$ZIP4" ]]; then
  echo "Missing ZIP4: $ROOT_DIR/$ZIP4" >&2
  exit 1
fi
if [[ ! -f "$ROOT_DIR/$ZIP5" ]]; then
  echo "Missing ZIP5: $ROOT_DIR/$ZIP5" >&2
  exit 1
fi

rm -rf "$WORK_DIR/web"/* "$WORK_DIR/engine"/*

# Extract
unzip -q "$ROOT_DIR/$ZIP4" -d "$WORK_DIR/web"
unzip -q "$ROOT_DIR/$ZIP5" -d "$WORK_DIR/engine"

# Normalize docker build contexts:
# If ZIPs contain a top-level folder, flatten one level.
flatten_one() {
  local dir="$1"
  local top
  top=$(find "$dir" -mindepth 1 -maxdepth 1 -type d | head -n 1 || true)
  if [[ -n "$top" ]] && [[ $(find "$dir" -mindepth 1 -maxdepth 1 | wc -l) -eq 1 ]]; then
    shopt -s dotglob
    mv "$top"/* "$dir"/
    rmdir "$top"
    shopt -u dotglob
  fi
}
flatten_one "$WORK_DIR/web"
flatten_one "$WORK_DIR/engine"

# Ensure required Docker files exist
if [[ ! -f "$WORK_DIR/web/Dockerfile" ]]; then
  cp "$ROOT_DIR/compose/Dockerfile.web" "$WORK_DIR/web/Dockerfile"
fi
if [[ ! -f "$WORK_DIR/engine/Dockerfile" ]]; then
  cp "$ROOT_DIR/compose/Dockerfile.engine" "$WORK_DIR/engine/Dockerfile"
fi

# Provide minimal requirements if missing (safe defaults)
if [[ ! -f "$WORK_DIR/web/requirements.txt" ]]; then
  cat > "$WORK_DIR/web/requirements.txt" <<'REQ'
flask==3.0.3
python-dotenv==1.0.1
psycopg[binary]==3.2.1
requests==2.32.3
REQ
fi
if [[ ! -f "$WORK_DIR/engine/requirements.txt" ]]; then
  cat > "$WORK_DIR/engine/requirements.txt" <<'REQ'
fastapi==0.111.0
uvicorn[standard]==0.30.1
python-dotenv==1.0.1
psycopg[binary]==3.2.1
REQ
fi

echo "Assembled runtime/web and runtime/engine successfully."
