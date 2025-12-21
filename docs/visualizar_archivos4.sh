#!/bin/bash

# Nombre: Script_Fiel_Integridad_v20251220_03
# Cambios respecto a v02:
# 1. Entrada robusta: Usa 'cat' para capturar múltiples líneas pegadas de golpe.
# 2. Finalización: Se usa Ctrl+D para terminar la entrada (más fiable para pegados).

LISTA="lista_archivos.txt"

echo "--- Gestor de Inspección: Modo Integridad (Multilínea) ---"

# 1. Gestión del archivo de lista
if [ -f "$LISTA" ]; then
    read -p "El archivo '$LISTA' ya existe. ¿Deseas (b)orrarlo o (a)ñadir? [b/a]: " accion
    [[ "$accion" == "b" ]] && rm "$LISTA" && touch "$LISTA" && echo "Reiniciado." || echo "Anexando..."
else
    touch "$LISTA"
fi

# 2. Entrada de datos mejorada para PEGAR
echo -e "\n--- INSTRUCCIONES PARA PEGAR ---"
echo "1. Pega todas las rutas que quieras."
echo "2. Cuando termines, pulsa ENTER y luego Ctrl+D para procesar."
echo "--------------------------------"

# Capturamos todo el bloque pegado directamente al archivo
cat >> "$LISTA"

# 3. Lógica de visualización
echo -e "\n=== INICIANDO INSPECCIÓN DE LA LISTA ===\n"

while IFS= read -r linea || [ -n "$linea" ]; do
    # Limpiamos posibles espacios en blanco o retornos de carro invisibles
    linea=$(echo "$linea" | tr -d '\r')
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
