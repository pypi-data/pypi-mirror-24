import numpy as np

def period(t,y):
    """
    Período de una función
    
    Esta función entrega el período de la función y la cantidad de muestras
    usadas para determinarlo. 
    
    NOTA: - Se deben tener muestreos igualmente espaciados
          - Se asume que la función tiene cruce por cero para obtener el
              período
    
    Donde:
        t: es el vector de tiempo
        y: es el vector con la magnitud asociada a cada t[i]
        
    Retorna:
        periodo,Numero de muestras
    
    """
    t = np.array(t)
    y=np.array(y)
    cross = []
    DN = []
    DT = []
    for i in range(len(t)-1):
        if(y[i]*y[i+1]<=0):
            cross.append(i)
    for i in range(len(cross)-1):
        DN.append(cross[i+1]-cross[i])
        DT.append(t[cross[i+1]]-t[cross[i]])
    per = 2*sum(DT)/len(DT)
    ND = int(2*sum(DN)/len(DN))
    return(per,ND)
def frec(t):
    """
        Frecuencia de muestreo
        
        Esta función entrega la frecuencia de muestreo promedio y el intervalo
        (min, max) en Hz
        
        Donde:
            t: es el vector de tiempos en segundos
    """
    t = np.array(t)
    dt = np.diff(t)
    dmax = np.max(dt)
    dmin = np.min(dt)
    dmean = np.mean(dt)
    return 1/dt_p,(1/dt_min,1/dt_max)
def RMS(t,y):
    """
    Valor eficaz de una función (RMS)
    
    Esta función entrega el valor eficaz (RMS) de una función
    
    Donde:
        t: es el vector de tiempos
        y: es el es el vector con la magnitud asociada a cada t[i]
    """
    t=np.array(t)
    y=np.array(y)
    Periodo = t[-1]-t[0]
    yy = y**2
    int_yy = np.trapz(yy,t)
    rms = np.sqrt(int_yy/Periodo)
    return rms
def DC(t,y):
    """
    Valor promedio de una función (Valor DC)
    
    Esta función entrega el valor promedio de una función
    
    Donde:
        t: es el vector de tiempos
        y: es el es el vector con la magnitud asociada a cada t[i]        
    
    """
    T=np.array(t)
    Y=np.array(v)
    Periodo = T[-1]-T[0]
    I_Y = np.trapz(Y,T)
    vdc = I_Y/Periodo
    return vdc
def desf(t,v,i):
    """
    Desfase entre señales de tension y corriente
    
    Esta función permite hallar el desfase entre 2 señales en un periodo dado.
    
    Donde:
       t_desf <0 -> corriente en atrazo
       t_desf >0 -> corriente en adelanto
     
    Nota: 
       El angulo entregado por la función está en radianes
       
    Retorna:
        tiempo desface, angulo desface
    
    """
    
    tcv=[]#instantes de cruce de tension
    tci=[]#inst. de cruce de corriente
    for q in range(len(t)-1):
        if np.sign(v[q]*v[q+1])==-1 and np.sign(v[q+1]-v[q])==1:
            tcv.append(t[q])
        if np.sign(i[q]*i[q+1])==-1 and np.sign(i[q+1]-i[q])==1:
            tci.append(t[q])
    t_desf = tcv[0]-tci[0]
    a_desf = 2*np.pi*t_desf/(t[-1]-t[0])
    return t_desf,a_desf
def fourier(t,v,n=1):
    """
    Fourier
    
    Esta función entrega los coeficientes ao, A y B de la transformada de fourier
    
    Donde:
        ao: es el término independiente
        A: es el coeficiente del coseno
        B: es el coeficiente del seno
        
    Retorna:
        ao, A, B
    
    """
    T=np.array(t)
    Y=np.array(v)
    Periodo = T[-1]-T[0]
    fo = 1/Periodo
    wo = 2*np.pi*fo
    I_Y = np.trapz(Y,T)
    ao = 2*I_Y/Periodo
    
    A=[]
    for N in range(1,n+1):
        Fi = []
        for i,q in enumerate(T):
            d = np.cos(N*wo*q)*Y[i]
            Fi.append(d)
        I_Y = np.trapz(Fi,T)
        ai = 2*I_Y/Periodo
        A.append(ai)
        
    B=[]
    for N in range(1,n+1):
        Fi = []
        for i,q in enumerate(T):
            d = np.sin(N*wo*q)*Y[i]
            Fi.append(d)
        I_Y = np.trapz(Fi,T)
        bi = 2*I_Y/Periodo
        B.append(bi)
    return(ao,A,B)
    
    
            