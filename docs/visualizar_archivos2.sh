#!/bin/bash

# Nombre: Script_Fiel_Integridad_v20251220_01
# Cambios: 
# 1. Uso estricto de 'read -e -r' para mantener integridad de rutas Windows (\).
# 2. Eliminación de filtros 'sed' para asegurar trazabilidad total del origen.
# 3. Mantenimiento de autocompletado (TAB) mediante flag '-e'.

LISTA="lista_archivos.txt"

echo "--- Gestor de Inspección: Modo Integridad de Datos ---"

# 1. Gestión del archivo de lista
if [ -f "$LISTA" ]; then
    read -p "El archivo '$LISTA' ya existe. ¿Deseas (b)orrarlo o (a)ñadir? [b/a]: " accion
    [[ "$accion" == "b" ]] && rm "$LISTA" && touch "$LISTA" && echo "Reiniciado." || echo "Anexando..."
else
    touch "$LISTA"
fi

# 2. Entrada de datos (Respeta fielmente la entrada del usuario)
echo -e "\nIntroduce las rutas originales. (Usa TAB para locales o pega rutas de Windows)."
echo "Escribe 'FIN' para terminar."

while true; do
    # -e permite TAB | -r impide que \ se interprete como escape
    read -e -r -p "> " entrada
    
    [[ "$entrada" == "FIN" ]] && break
    [[ -z "$entrada" ]] && continue

    # Guardamos la ruta EXACTA en el archivo
    echo "$entrada" >> "$LISTA"
done

# 3. Lógica de visualización (Sin transformaciones)
echo -e "\n--- Iniciando inspección de rutas originales ---\n"

while IFS= read -r linea || [ -n "$linea" ]; do
    [[ -z "$linea" ]] && continue
    
    echo "----------------------------------------"
    echo "ARCHIVO (Origen): $linea"
    echo "----------------------------------------"
    
    # IMPORTANTE: Usamos "$linea" entre comillas dobles para que Bash 
    # intente resolver la ruta tal cual fue escrita.
    if [ -f "$linea" ]; then
        cat -A "$linea"
    else
        echo "ESTADO: No accesible/encontrado desde este entorno."
        echo "NOTA: Si es una ruta de Windows, asegúrate de que el entorno tiene permisos."
    fi
    echo -e "\n"
done < "$LISTA"

echo "Proceso finalizado de forma discreta."
