#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
MAILBOX="$ROOT/mailbox"
SOURCE="$ROOT/data/inbox/inbox"
LOG="$MAILBOX/run.log"

echo "=== Mail sorter ==="

if ! command -v python >/dev/null 2>&1; then
  echo "FAIL: python не найден"
  exit 1
fi

if [ ! -d "$SOURCE" ]; then
  echo "FAIL: нет папки с письмами: $SOURCE"
  exit 1
fi

mkdir -p "$MAILBOX"

echo "Запуск обработки..."
if python "$ROOT/main.py" --mailbox "$MAILBOX" --source "$SOURCE" --force 2>&1 | tee "$LOG"; then
  echo "SUCCESS: обработка завершена"
  if [ -f "$MAILBOX/stats.txt" ]; then
    echo "--- stats ---"
    cat "$MAILBOX/stats.txt"
  fi
  exit 0
else
  echo "FAIL: программа завершилась с ошибкой"
  exit 1
fi
