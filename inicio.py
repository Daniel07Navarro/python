""" PRACTICA """


def es_palindromo(texto):
    texto = no_space(texto)
    texto_al_revez = reverse(texto)
    print(texto_al_revez)

def reverse(texto):
    texto_al_revez = ""
    for char in texto:
        texto_al_revez = char + texto_al_revez
    return texto_al_revez

def no_space(texto):
    nuevo_texto = ""
    for char in texto:
        if char != " ":
            nuevo_texto += char
    return nuevo_texto

es_palindromo("amo la paloma")

es_palindromo("amo la ")







