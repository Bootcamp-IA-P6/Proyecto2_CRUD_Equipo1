#!/bin/bash

# --- Configuración ---
LISTA="lista_archivos.txt"

echo "--- Gestor de Inspección de Archivos ---"

# 1. Gestión del archivo de lista
if [ -f "$LISTA" ]; then
    read -p "El archivo '$LISTA' ya existe. ¿Deseas (b)orrarlo y crear uno nuevo o (a)ñadir archivos? [b/a]: " accion
    if [ "$accion" == "b" ]; then
        rm "$LISTA"
        touch "$LISTA"
        echo "Archivo reiniciado."
    else
        echo "Añadiendo a la lista existente..."
    fi
else
    touch "$LISTA"
    echo "Creado nuevo archivo de lista: $LISTA"
fi

# 2. Entrada de datos interactiva
echo -e "\nIntroduce las rutas de los archivos (ejemplo: /c/Users/...) "
echo "Escribe 'FIN' y pulsa Enter para terminar la entrada de datos."

while true; do
    read -p "> " entrada
    if [ "$entrada" == "FIN" ]; then
        break
    fi
    
    # Verificamos si la ruta existe antes de guardarla
    if [ -e "$entrada" ]; then
        echo "$entrada" >> "$LISTA"
        echo "  [OK] Añadido."
    else
        echo "  [!] Advertencia: No encuentro esa ruta, pero la guardaré de todos modos."
        echo "$entrada" >> "$LISTA"
    fi
done

# 3. Ejecución de la lógica de visualización
echo -e "\n--- Iniciando lectura de archivos ---\n"

if [ ! -s "$LISTA" ]; then
    echo "La lista está vacía. No hay nada que mostrar."
else
    while IFS= read -r linea || [ -n "$linea" ]; do
        [[ -z "$linea" ]] && continue
        
        echo "----------------------------------------"
        echo "ARCHIVO: $linea"
        echo "----------------------------------------"
        
        if [ -f "$linea" ]; then
            cat -A "$linea"
        else
            echo "ERROR: El archivo no existe o no se puede leer."
        fi
        echo -e "\n"
    done < "$LISTA"
fi

echo "Proceso finalizado. Que tengas un buen día."
exit 0
