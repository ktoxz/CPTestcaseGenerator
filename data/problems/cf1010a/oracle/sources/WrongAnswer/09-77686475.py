def function(NPlanetas,MasaCohete,CoeficientesDespegue,CoeficientesLanding):
    landing=-1
    takeoff=1
    NPlanetas=int(NPlanetas)
    MasaCohete=int(MasaCohete)
    try:
        W=float(MasaCohete)
        W=W*(1/(1-1/float(CoeficientesLanding[0])))
        for i in range(1,NPlanetas):
            if landing==1:
                W=W*(1/(1-1/float(CoeficientesLanding[NPlanetas-i])))
            if takeoff==1:
                W=W*(1/(1-1/float(CoeficientesDespegue[NPlanetas-i])))
            landing=landing*(-1)
            takeoff=takeoff*(-1)
            if landing==1:
                W=W*(1/(1-1/float(CoeficientesLanding[NPlanetas-i])))
            if takeoff==1:
                W=W*(1/(1-1/float(CoeficientesDespegue[NPlanetas-i])))
            landing=landing*(-1)
            takeoff=takeoff*(-1)
        W=W*(1/(1-1/float(CoeficientesDespegue[0])))
        W=W-MasaCohete
        return (W)
    except:
        return ('-1')
NPlanetas=int(input('Planetas'))
MasaCohete=int(input('Masa Cohete'))
CoeficientesDespegue1=input('Coeficientes D')
CoeficientesLanding1=input('Coeficientes L')
CoeficientesDespegue = [float(i) for i in CoeficientesDespegue1.split(" ")]
CoeficientesLanding = [float(i) for i in CoeficientesLanding1.split(" ")]

function(NPlanetas,MasaCohete,CoeficientesDespegue,CoeficientesLanding)