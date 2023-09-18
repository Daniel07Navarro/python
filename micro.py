
#archivo = pd.read_csv(r'C:\Users\Daniel\Desktop\prueba.txt',delimiter = '\t')
archivo = open('prueba.txt','r')
print(archivo.read())

archivoV2 = archivo.read().split()
archivoArreglo = []
for palabra in archivoV2:
    if (palabra not in archivoArreglo) :
        archivoArreglo.append(palabra)
print(str(archivoArreglo))
archivo.close()

"""
def NLP_Ascci_BIN(mensajeNLP):
  total_cpu = 0
  total_ciclo_reloj = 0
  for palabra in mensajeNLP:
    asc = ""
    for d in palabra:
      cad = str(ord(d))
      asc = asc+cad
    asc = int(asc)
    bin = decima_a_binario(asc)
    TCPU = len(palabra)*2
    total_cpu = total_cpu+TCPU
    CRELOJ = 4*TCPU
    total_ciclo_reloj= total_ciclo_reloj+CRELOJ
    print("Unidad de analisis:","",palabra)
    print("Unidad de analisis:","",asc)
    print("Tiempo CPUS:","",TCPU)
    print("CLICLOS RELOJ:","",CRELOJ)
    print("BINARIO:","",bin)
  print("Tiempo total CPU: "+str(total_cpu))
  print("Tiempo total de ciclos reloj: "+str(total_ciclo_reloj))
  print("Se recomienda una computadora de : "+str(total_ciclo_reloj/1000)+ " khz")

cadena_vacia = []
for palabra in cadena:
    if palabra not in cadena_vacia:
      cadena_vacia.append(palabra)

print(str(cadena))
print(str(cadena_vacia))

NLP_Ascci_BIN(cadena_vacia)"""
