import numpy as np
import scipy
import math
import random
import statistics as stats
#np.random.seed(1334)

#Poblacion inicial
def PI(n,a):
    f=np.zeros((n,a))
    for i in range(n):
        for j in range(a):
            f[i,j]=xl+np.random.uniform(0,1)*(xu-xl)
    return f

#Fitness
def eval(n,a,solu):
    cont=0
    for j in range(a):
        cont=cont+(solu[j]**2)-10*np.cos(2*np.pi*solu[j])
    fitness=cont+10*a                                                                                                                    
    return fitness

#Padres y juveniles
def ordenados(n,a,f):
    padres=np.zeros((2,a))
    juveniles=np.zeros((n-2,a))
    funcion=np.zeros((n))
    x=np.zeros((n))
    for i in range(n):
        f1=eval(n,a,f[i])
        funcion[i]=f1
    x=np.argsort(funcion)
    for i in range(2):
        padres[i,:]=f[x[i],:]
    for i in range(n-2):
        juveniles[i,:]=f[x[i+2],:]
    return padres,juveniles,funcion

#Learning phase
def learning(n,padres,juveniles,funcion):
    f2=np.zeros(n-2)
    jumutado=np.zeros((n-2,a))
    for i in range(0,n-2):
        for j in range(a):
            ale=np.random.uniform(0,1)                         
            #Social learning                                     
            if ale<=sl:
                ale2=np.random.uniform(0,1)
                if ale2<=vsl:
                    ale3=random.uniform(0,1)
                    if ale3<=p1:
                        jumutado[i,j]=padres[0,j]
                    else:
                        jumutado[i,j]=padres[1,j]
                else:
                    ale4=int(2+(np.random.uniform(0,1)*(i-2)))
                    fit=eval(n,a,juveniles[i])
                    f2[i]=fit
                    if f2[i]<=f2[ale4]:
                        jumutado[i,j]=juveniles[i,j]
                    else:
                        jumutado[i,j]=juveniles[ale4,j]        
            #Asocial Learning 
            else:
                ale5=random.uniform(0,1)
                if taeq<=ale5:
                    jumutado[i,j]=xl+np.random.uniform(0,1)*(xu-xl)
                else:
                    jumutado[i,j]=juveniles[i,j]
    return jumutado

#Reinforcement phase 
def reinforcement(juveniles,jumutado,padres,n,a):
    rjuveniles=np.zeros((n-2,a))
    rpadres=np.zeros((2,a))
    alfa=np.zeros((n-2,a))
    beta=np.zeros((n-2,a)) 
    #Juveniles reinforcement                                    
    for i in range(n-2):
        for j in range(a):
            ale6=np.random.uniform(0,1)
            if ale6<=Rprob:
                alfa[i,j]=abs(jumutado[i,j]-juveniles[i,j])
                lf=lfmin+((lfmax-lfmin)/maxt)*t 
                r=np.random.normal(0,1)
                beta[i,j]=juveniles[i,j]*np.exp(-lf*r*t*np.mean(jumutado[j]))
                if i<(n/2):
                    rjuveniles[i,j]=jumutado[i,j]+(beta[i,j]-alfa[i,j])
                else:
                    r1=np.random.uniform(0,1)
                    r2=np.random.uniform(0,1)
                    rjuveniles[i,j]=jumutado[i,j]+(r1*((r2*beta[i,j])-alfa[i,j]))
            else:
                rjuveniles[i,j]=jumutado[i,j]
    #Parents reinforcement
    for i in range(2):
        for j in range(a):
            ale7=np.random.uniform(0,1)
            if ale7<=Rprob:
                r3=np.random.normal(0,1)
                r4=np.random.uniform(0,1)
                if i==0:
                    rpadres[i,j]=padres[i,j]-(padres[0,j]+(np.exp(r3*(np.mean(padres[j-2])-padres[i,j]))))    
                else:
                    rpadres[i,j]=padres[i,j]-(r4*(padres[0,j]-(np.exp(r3*(np.mean(padres[j-2])-padres[i,j])))))
            else:
                rpadres[i,j]=padres[i,j]  
    return rjuveniles,rpadres
   
def actualizacion(rjuveniles,rpadres,n,a,bcrow,bestfit):
    funcion2=np.zeros((n))
    funcion3=np.zeros((n))
    npobl=np.zeros((n,a))
    mpobl=np.zeros((n,a))
    y=np.zeros((n,1))
    pnuevos=np.zeros((2,a))
    jnuevos=np.zeros((n-2,a))
    npobl[0]=rpadres[0]
    npobl[1]=rpadres[1]
    for i in range(2,n):
        npobl[i]=rjuveniles[i-2] 
    for i in range(n):
        for j in range(a):
            if npobl[i,j]<-5.12:
                npobl[i,j]=-5.12
            if npobl[i,j]>5.12:
                npobl[i,j]=5.12
    for i in range(n):
        f3=eval(n,a,npobl[i])
        funcion2[i]=f3
    y=np.argsort(funcion2)
    for i in range(n):
        mpobl[i]=npobl[y[i]]
        f4=eval(n,a,mpobl[i])
        funcion3[i]=f4
        if funcion3[0]<bestfit:
            bestfit=funcion3[0]
            bcrow[0,:]=mpobl[0,:]
    pnuevos[0]=mpobl[0]
    pnuevos[1]=mpobl[1]
    for i in range(n-2):
        jnuevos[i,:]=mpobl[i+2,:]
    return bcrow,bestfit,mpobl,y,pnuevos,jnuevos
 
#Programa principal
a=4
n=80
xl=-5.12
xu=5.12
maxt=500
bcrow=np.zeros((1,a))
bestfit=10000000
for t in range(maxt):
    f=PI(n,a)
    padres,juveniles,funcion=ordenados(n,a,f)
    sl=0.99        #Social learning
    vsl=0.99      #learning from their parents
    p1=0.95        #which parent?
    taeq=0.3     #Asocial learning
    Rprob=0.9    #Reinforcement probability
    jumutado=learning(n,padres,juveniles,funcion)
    lfmin=0.0005
    lfmax=0.02
    rjuveniles,rpadres=reinforcement(juveniles,jumutado,padres,n,a)
    bcrow,bestfit,mpobl,y,pnuevos,jnuevos=actualizacion(rjuveniles,rpadres,n,a,bcrow,bestfit)
    padres=pnuevos.copy()
    juveniles=jnuevos.copy()
t=t+1
print(bcrow)
print(bestfit)

    




