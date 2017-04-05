#!/usr/bin/python

paisOmision = "es"

def convertir(numero, pais="es"):

    numero = limpiar(numero)

    iban = numero[-24:]

    ccc = numero[-20:]

    if not esIBAN(numero) and not esCCC(numero):

        return "Error: No es IBAN ni CCC"

    elif esIBAN(numero) and not validarIBAN(iban):

        return "Error: IBAN incorrecto"

    elif not validarCCC(ccc):

        return "Error: CCC incorrecto"

    elif esIBAN(numero):

        return formatearIBAN(iban)

    else:

        return formatearIBAN(calcularIBAN(ccc, pais))

def calcular(numero, pais="es"):

    numero = limpiar(numero)

    if esCCC(numero):

        dc = numero[8:10]

        if not dc.isdigit():

            numero = calcularCCC(numero)

        return calcularIBAN(numero, pais)

    else:

        return numero

def validar(numero):

    numero = limpiar(numero)

    if esIBAN(numero):

        return validarIBAN(numero)

    elif esCCC(numero):

        return validarCCC(numero)

    else:

        return False

def formatear(numero, separador=None):

    numero = limpiar(numero)

    if esIBAN(numero):

        return formatearIBAN(numero, separador)

    elif esCCC(numero):

        return formatearCCC(numero, separador)

    else:

        return ""

def calcularIBAN(ccc, pais="es"):

    ccc = limpiar(ccc)

    pais = pais.upper()

    cifras = ccc + valorCifras(pais) + "00"

    resto = modulo(cifras, 97)

    return pais + cerosIzquierda(str(98 - resto), 2) + ccc

def validarIBAN(iban):

    iban = limpiar(iban)

    pais = iban[0:2]

    dc = iban[2:4]

    cifras = iban[4:] + valorCifras(pais) + dc

    resto = modulo(cifras, 97)

    return resto == 1

def validarCCC(ccc):

    ccc = limpiar(ccc)

    items = formatearCCC(ccc, " ").split()

    dc = str(modulo11(items[0] + items[1])) + str(modulo11(items[3]))

    return dc == items[2]

def calcularCCC(ccc):

    ccc = limpiar(ccc)

    return ccc[0:8] + calcularDC(ccc) + ccc[10:20]

def calcularDC(ccc):

    ccc = limpiar(ccc)

    items = formatearCCC(ccc, " ").split()

    return str(modulo11(items[0] + items[1])) + str(modulo11(items[3]))

def formatearCCC(ccc, separador=None):

    ccc = limpiar(ccc)

    if separador == None: separador = "-"

    return ccc[0:4] + separador + ccc[4:8] + separador + ccc[8:10] + separador + ccc[10:20]

def formatearIBAN(iban, separador=None):

    iban = limpiar(iban)

    if separador == None: separador = " "

    items = []

    for i in range(6): items.append(iban[i*4: (i+1)*4])

    return separador.join(items)

def esCCC(cifras):

    return len(cifras) == 20

def esIBAN(cifras):

    return len(cifras) == 24

def limpiar(numero):

	numero = numero.replace("IBAN", "")
	numero = numero.replace(" ", "")
	numero = numero.replace("-", "")
	return numero

def modulo(cifras, divisor):

    CUENTA, resto, i = 13, 0, 0

    while i < len(cifras):

        dividendo = str(resto) + cifras[i: i+CUENTA]

        resto = int(dividendo) % divisor

        i += CUENTA

    return resto

def modulo11(cifras):

    modulos = [(2**x)%11 for x in range(10)]

    suma = 0

    cifras = cerosIzquierda(cifras, 10)

    for cifra, modulo in zip(cifras, modulos):

        suma += int(cifra) * modulo

    control = suma % 11

    return control if control < 2 else 11 - control

def cerosIzquierda(cifras, largo):

    cantidad = largo - len(cifras)

    ceros = "0"*cantidad

    return ceros + cifras

def valorCifras(cifras):

    LETRAS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    
    items = []

    for cifra in cifras:

        posicion = LETRAS.find(cifra)

        items.append(str(posicion) if posicion >= 0 else "-")

    return "".join(items)
