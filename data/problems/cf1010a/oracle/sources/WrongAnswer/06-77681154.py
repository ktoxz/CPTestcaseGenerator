def function(NPlanetas,MasaCohete,CoeficientesDespegue,CoeficientesLanding):
    landing=-1
    takeoff=1
    try:
        W=MasaCohete
        #print ('Landing on Earth','Peso: ',W)
        #print ('CoefLanding',CoeficientesLanding[0])
        W=W*(1/(1-1/float(CoeficientesLanding[0])))
        for i in range(1,NPlanetas):
            if landing==1:
                W=W*(1/(1-1/float(CoeficientesLanding[NPlanetas-i])))
                #print ("Aterrizando en el planeta ",NPlanetas-i,'Peso: ',W)
                #print ('CoefLanding',CoeficientesLanding[NPlanetas-i])
            if takeoff==1:
                W=W*(1/(1-1/float(CoeficientesDespegue[NPlanetas-i])))
                #print ("Despegando en el planeta ",NPlanetas-i,'Peso: ',W)
                #print ('CoefTakingOff',CoeficientesDespegue[NPlanetas-i])
                
            landing=landing*(-1)
            takeoff=takeoff*(-1)
            
            if landing==1:
                W=W*(1/(1-1/float(CoeficientesLanding[NPlanetas-i])))
                #print ("Aterrizando en el planeta ",NPlanetas-i,'Peso: ',W)
                #print ('CoefLanding',CoeficientesLanding[NPlanetas-i])
            if takeoff==1:
                W=W*(1/(1-1/float(CoeficientesDespegue[NPlanetas-i])))
                #print ("Despegando en el planeta ",NPlanetas-i,'Peso: ',W)
                #print ('CoefTakingOff',CoeficientesDespegue[NPlanetas-i])

            landing=landing*(-1)
            takeoff=takeoff*(-1)

            
        W=W*(1/(1-1/float(CoeficientesDespegue[0])))
        W=W-MasaCohete
        #print ('CoefTakingOff',CoeficientesDespegue[0])
        #print ('Taking off from Earth','Peso: ',W+MasaCohete)
        return W
    except:
        return ('-1')