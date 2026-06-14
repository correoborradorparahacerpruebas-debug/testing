#!/usr/bin/awk -f

BEGIN {
    # Expresión regular para separar campos de CSV que maneja comillas y comas internas (requiere GNU Awk / gawk)
    FPAT = "([^,]*)|(\"[^\"]+\")"
    OFS = ","
}

# 1. Cabecera (primera línea)
NR == 1 {
    print $1, $2, $3, $4, $5, $6
    next
}

{
    # Trim y limpieza básica de cada campo (remover espacios al inicio y final)
    for (i = 1; i <= NF; i++) {
        gsub(/^[ \t]+|[ \t]+$/, "", $i)
    }

    # Campo 1: ID
    id = $1
    # Asignar ID 4 a Ana Ruiz que no tiene ID
    if (id == "" && $2 == "Ana Ruiz") {
        id = 4
    }

    # Campo 2: Nombre
    nombre = $2
    # Colapsar múltiples espacios internos en uno solo
    gsub(/[ \t]+/, " ", nombre)

    # Campo 3: Edad
    edad = $3
    # Limpiar si es "veinticinco" (texto), edad negativa o mayor a 100
    if (edad == "veinticinco" || edad < 0 || edad > 100) {
        edad = ""
    }

    # Campo 4: Fecha Registro
    fecha = $4
    # Estandarizar a YYYY-MM-DD
    # Formato DD/MM/YYYY o DD-MM-YYYY (ej. 15/02/2023 o 10-05-2023)
    if (fecha ~ /^[0-9]{2}[\/-][0-9]{2}[\/-][0-9]{4}$/) {
        split(fecha, partes, /[\/-]/)
        fecha = partes[3] "-" partes[2] "-" partes[1]
    }
    # Formato YYYY/MM/DD (ej. 2023/04/05)
    else if (fecha ~ /^[0-9]{4}\/[0-9]{2}\/[0-9]{2}$/) {
        gsub(/\//, "-", fecha)
    }

    # Campo 5: Email
    email = $5
    # Validar formato de email
    if (email !~ /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/) {
        email = ""
    }

    # Campo 6: Salario
    salario = $6
    # Quitar $, comillas y comas (ej. "$2,200" -> 2200)
    gsub(/[\$ \"]/, "", salario)
    gsub(/,/, "", salario)
    if (salario == "N/A") {
        salario = ""
    }

    # Control de Duplicados (por ID)
    # Si el ID ya existe, preferimos el registro que tenga datos de edad válidos
    if (id in guardado_id) {
        if (edad != "" && guardado_edad[id] == "") {
            guardado_id[id] = id
            guardado_nombre[id] = nombre
            guardado_edad[id] = edad
            guardado_fecha[id] = fecha
            guardado_email[id] = email
            guardado_salario[id] = salario
        }
    } else {
        # Agregar registro único
        orden[++count] = id
        guardado_id[id] = id
        guardado_nombre[id] = nombre
        guardado_edad[id] = edad
        guardado_fecha[id] = fecha
        guardado_email[id] = email
        guardado_salario[id] = salario
    }
}

END {
    # Imprimir registros limpios
    for (j = 1; j <= count; j++) {
        id = orden[j]
        print guardado_id[id], guardado_nombre[id], guardado_edad[id], guardado_fecha[id], guardado_email[id], guardado_salario[id]
    }
}
