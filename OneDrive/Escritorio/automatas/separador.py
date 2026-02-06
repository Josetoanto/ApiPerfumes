VF = set("aeoáéó")
VD = set("iuíú")
ACENTUADAS = set("áéíóú")
DIGRAFOS = ["ch", "ll", "rr"]
GC = ["pr", "tr", "cl", "bl", "fr", "dr", "cr", "pl", "gr", "gl", "fl", "br"]

def tipo_letra(l):
    if l.lower() in VF:
        return "VF"
    if l.lower() in VD:
        return "VD"
    return "C"

def es_vocal(l):
    return l.lower() in VF.union(VD)

def separar_en_digrafos(palabra):
    i = 0
    salida = []
    while i < len(palabra):
        if i+1 < len(palabra):
            par = palabra[i:i+2].lower()
            if par in DIGRAFOS:
                salida.append(par)
                i += 2
                continue
        salida.append(palabra[i])
        i += 1
    return salida

def es_hiato(a, b):
    if a.lower() in VF and b.lower() in VF:
        return True
    if a.lower() in VD and b.lower() in VF and a.lower() in ACENTUADAS:
        return True
    if a.lower() in VF and b.lower() in VD and b.lower() in ACENTUADAS:
        return True
    return False

def es_diptongo(a, b):
    if es_hiato(a, b):
        return False
    if es_vocal(a) and es_vocal(b):
        return True
    return False

def separar_silabas(palabra):
    original = palabra
    palabra = palabra.lower()
    letras = separar_en_digrafos(palabra)

    i = 0
    silabas = []
    actual = ""
    reglas = []

    while i < len(letras):
        actual += letras[i]

        if i+1 < len(letras) and es_vocal(letras[i]) and es_vocal(letras[i+1]):
            if es_hiato(letras[i], letras[i+1]):
                silabas.append(actual)
                reglas.append("Hiato")
                actual = ""
            else:
                reglas.append("Diptongo")
        elif (i+2 < len(letras)
              and es_vocal(letras[i])
              and not es_vocal(letras[i+1])
              and es_vocal(letras[i+2])):
            silabas.append(actual)
            reglas.append("V-C-V")
            actual = ""

        elif i+1 < len(letras) and not es_vocal(letras[i]) and not es_vocal(letras[i+1]):
            grupo = letras[i] + letras[i+1]

            if grupo in DIGRAFOS:
                reglas.append("Dígrafo")
            elif grupo in GC:
                reglas.append("Grupo Consonántico (G.C.)")
            else:
                silabas.append(actual[:-1])
                actual = actual[-1:]
                reglas.append("C-C")

        i += 1

    if actual:
        silabas.append(actual)

    return original, "-".join(silabas), ", ".join(list(dict.fromkeys(reglas)))


def main():
    palabras = []
    with open("palabras_entrada.txt", "r", encoding="utf-8") as f:
        palabras = [p.strip() for p in f.readlines() if p.strip()]

    with open("tokens_salida.txt", "w", encoding="utf-8") as out:
        out.write("Palabra | Separación | Reglas aplicadas\n")
        out.write("--------------------------------------------\n")

        for p in palabras:
            orig, sep, reglas = separar_silabas(p)
            out.write(f"{orig} | {sep} | {reglas}\n")

    print("\nTabla generada:\n")
    print("Palabra Original | Separación Silábica | Reglas")
    print("-----------------------------------------------------------")
    for p in palabras:
        orig, sep, reglas = separar_silabas(p)
        print(f"{orig:15} | {sep:20} | {reglas}")


if __name__ == "__main__":
    main()
