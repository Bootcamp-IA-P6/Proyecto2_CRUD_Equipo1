#!/usr/bin/env bash

# Directorio del proyecto = directorio donde está este script
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"

DATE=$(date +%Y-%m-%d)
COUNT=$(ls "$LOG_DIR" | grep "$DATE" | wc -l)
COUNT=$(printf "%03d" $((COUNT + 1)))

LOG_FILE="$LOG_DIR/${DATE}.terminal.${COUNT}.bash.vscode.log"

echo "Registrando sesión en: $LOG_FILE"
echo "--------------------------" | tee "$LOG_FILE"

# Subshell interactivo REAL
bash --noprofile --norc -i |& tee -a "$LOG_FILE"
