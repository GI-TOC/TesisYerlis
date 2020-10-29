import numpy as np

def PI(Tp,N):
    filas=Tp
    columnas=N
    
    matriz=np.random.rand(filas,columnas)
    
    return matriz

def secuencias(Tp,N,matriz):
    sec=np.zeros((Tp,N))
    for i in range(Tp):
        sec[i]=matriz[i].argsort()+1 
    return sec

def Eval(Tp,N,dem,cap,sec,PI):  
    clie=np.zeros((Tp,(N*2)))
    cont=0
    for i in range (Tp):
        clie[i,1]=sec[i,0]
    for i in range (Tp):
       cont=dem[sec[i,0]-1]
       j=1
       k=1
       while j<N:
           cont=cont+dem[sec[i,j]-1]
           if cont<=cap:
               clie[i,k+1]=sec[i,j]
               j=j+1
               k=k+1
           else:
               cont=0
               k=k+1  
               clie[i,k+1]=0
    return clie

def Costos(sec,N,Tp,clie,dem):
    costos=np.array([[0,2,3,3,3,1],[2,0,3,3,2,2],[3,3,0,4,2,3],[3,3,4,0,3,4],[3,2,2,3,0,1],[3,2,2,1,2,0]])
    #print(costos)
    cost=np.zeros((Tp))
    for i in range(Tp):
        count=0
        for j in range(9):
            count=count+costos[clie[i,j],clie[i,j+1]]       
        cost[i]=count
    return cost

def torneo(Tp,N,matriz,clie,dem):
    padres=np.zeros((Tp,N))
    for i in range(Tp):
        ale1=np.random.randint(Tp)
        ale2=np.random.randint(Tp)
        while ale2==ale1:
            ale2=np.random.randint(Tp)
        f1=cost[ale1]
        f2=cost[ale2]
        if f1<f2:
            padres[i,:]=matriz[ale1,:]
        else:
            padres[i,:]=matriz[ale2,:]
    return padres

def cruzamiento(Tp,N,padres):
    hijos=np.zeros((Tp,N))    
    for i in range(0,Tp,2):
        ale3=np.random.randint(Tp)
        madre=padres[ale3, :]
        ale4=np.random.randint(Tp)
        while ale4==ale3:  
            ale4=np.random.randint(Tp)
        padre=padres[ale4, :]
        
        punto=np.random.randint(0,N-1)
        
        ca1=madre[0:punto+1]
        co2=padre[punto+1:N]
        hijo1=np.append(ca1,co2)
        
        ca2=padre[0:punto+1]
        co1=madre[punto+1:N]
        hijo2=np.append(ca2,co1)
      
        hijos[i,:]=hijo1
        hijos[i+1,:]=hijo2
       
    return hijos

def mutacion(Tp,N):
    hijosmutados=np.zeros((Tp,N)) 
    for i in range(Tp): 
        ale5=np.random.uniform(0,1)
        if ale5<=0.05:
            ale6=np.random.randint(Tp)
            hijosele1=hijos[ale6, :]
            ale7=np.random.randint(N)
            ale8=np.random.uniform(0,1)
            hijosele1[ale7]=ale8        
          
        else: 
            ale6=np.random.randint(Tp)
            hijosele1=hijos[ale6, :]
          
        hijosmutados[i, :]=hijosele1
   
    return hijosmutados

def MejorValor(Tp,N,hijosmutados): 
    for i in range(Tp):   
        menorvalor=costo[0]
        mejorsecuencia=secu[0]
    for i in range(Tp):
        if costo[i]<menorvalor:   
            menorvalor=costo[i]
            mejorsecuencia=secu[i]       
    return menorvalor,mejorsecuencia

#Programa principal
Tp=int(input("Ingrese el tamaño de la poblacion: "))
if Tp%2==0:
    Tp=Tp
else:
    Tp=Tp+1
N=5
Ngen=int(input("ingrese el numero de generaciones: "))
#Datos
cap=15
dem=[5,10,6,4,2]
matriz=PI(Tp,N) 
#Generacion de secuencias
sec=secuencias(Tp,N,matriz)
sec=sec.astype(int)
#Evaluacion
clie=Eval(Tp,N,dem,cap,sec,PI)
clie=clie.astype(int)
#Calculo del costo
cost=Costos(sec,N,Tp,clie,dem)
cost=cost.astype(int)
#Torneo
for i in range(Ngen):
    padres=torneo(Tp,N,matriz,clie,dem)
#Cruzamiento
    hijos=cruzamiento(Tp,N,padres)
#Mutacion
    hijosmutados=mutacion(Tp,N)
#Evaluacionhijosmutados
    secu=secuencias(Tp,N,hijosmutados)
    secu=secu.astype(int)
    clien=Eval(Tp,N,dem,cap,secu,PI)
    clien=clien.astype(int)
    costu=Costos(secu,N,Tp,clien,dem)
    costu=costu.astype(int)
    costo=costu
#MejorValor
menorvalor,mejorsecuencia=MejorValor(Tp,N,hijosmutados)
print(menorvalor)
print(mejorsecuencia)
#Actualizar
matriz=hijosmutados.copy


