#!/bin/bash

# Nombre: Script_Fiel_Integridad_v20251220_02
# Cambios respecto a v01:
# 1. Mejora visual: Separadores más claros entre archivos para evitar fatiga.
# 2. Control de lectura: Asegura que el bucle de visualización sea atómico.

LISTA="lista_archivos.txt"

echo "--- Gestor de Inspección: Modo Integridad de Datos ---"

# 1. Gestión del archivo de lista
if [ -f "$LISTA" ]; then
    read -p "El archivo '$LISTA' ya existe. ¿Deseas (b)orrarlo o (a)ñadir? [b/a]: " accion
    [[ "$accion" == "b" ]] && rm "$LISTA" && touch "$LISTA" && echo "Reiniciado." || echo "Anexando..."
else
    touch "$LISTA"
fi

# 2. Entrada de datos
echo -e "\nIntroduce rutas. Escribe 'FIN' para terminar."

while true; do
    read -e -r -p "Siguiente ruta > " entrada
    [[ "$entrada" == "FIN" ]] && break
    [[ -z "$entrada" ]] && continue
    echo "$entrada" >> "$LISTA"
done

# 3. Lógica de visualización (Sin transformaciones)
echo -e "\n=== INICIANDO INSPECCIÓN DE LA LISTA ===\n"

while IFS= read -r linea || [ -n "$linea" ]; do
    [[ -z "$linea" ]] && continue
    
    echo "########################################################################"
    echo " MOSTRANDO: $linea"
    echo "########################################################################"
    
    if [ -f "$linea" ]; then
        cat -A "$linea"
    else
        echo "ESTADO: No accesible/encontrado."
    fi
    echo -e "\n[ FIN DE ARCHIVO ]\n"
done < "$LISTA"

echo "Proceso finalizado. Todo en orden."
