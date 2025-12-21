#!/bin/bash

# visualizar_archivos5.sh
# Opción de mejora: imprimir números de lineas con ceros significativos antes de cada línea.
# Para calcular los ceros significativos basarse en el número total de líneas.
# Hace un sort en el archivo ./lista_archivos.txt para tener una lista ordenada.
# > lista_archivos.txt equivale a sort ./lista_archivos.txt > !$
# Ya no se emplea read -e -r -p
# ¡Estudiarse la macro!. Aprender cada opción ufff.

# Nombre: Script_Fiel_Integridad_v20251220_04
# Cambios respecto a v03:
# 1. Optimización sugerida por el usuario: Uso de redirección directa '>' para limpiar la lista.
# 2. Mantenimiento de entrada robusta 'cat >>' para pegados masivos.

LISTA="lista_archivos.txt"

echo "--- Gestor de Inspección: Versión Navaja Suiza ---"

# 1. Gestión del archivo de lista (Simplificada)
if [ -f "$LISTA" ]; then
    read -p "El archivo '$LISTA' ya existe. ¿(b)orrar o (a)ñadir? [b/a]: " accion
    if [[ "$accion" == "b" ]]; then
        > "$LISTA"  # Esto vacía el archivo sin necesidad de borrarlo y recrearlo
        echo "Lista vaciada."
    else
        echo "Anexando..."
    fi
else
    touch "$LISTA"
fi

# 2. Entrada de datos (El método ganador)
echo -e "\n[ PEGA LAS RUTAS Y PULSA ENTER + CTRL+D PARA EMPEZAR ]\n"

cat >> "$LISTA"

# 3. Lógica de visualización
echo -e "\n=== INICIANDO INSPECCIÓN ===\n"

while IFS= read -r linea || [ -n "$linea" ]; do
    # Limpieza de retorno de carro de Windows (\r)
    linea=$(echo "$linea" | tr -d '\r')
    [[ -z "$linea" ]] && continue
    
    echo "########################################################################"
    echo " MOSTRANDO: $linea"
    echo "########################################################################"
    
    if [ -f "$linea" ]; then
        cat -A "$linea"
    else
        echo "ESTADO: No accesible."
    fi
    echo -e "\n[ FIN DE ARCHIVO ]\n"
done < "$LISTA"

echo "Proceso finalizado. Misión cumplida."
