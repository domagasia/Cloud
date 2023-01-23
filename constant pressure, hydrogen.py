import cantera as ct
import matplotlib.pyplot as plt

gas = ct.Solution('gri30.xml')

def IgnitionDelay(gas):
      
    r = ct.Reactor(gas)
    sim = ct.ReactorNet([r])
    
    OH_fraction_prev = 0
    OH_fraction_now = 0
    
    while OH_fraction_prev <= OH_fraction_now:
        t =sim.step()
        OH_fraction_prev = OH_fraction_now
        OH_fraction_now = r.thermo['OH'].X
    
    return 1e6*t  


P=101325*5 # constant initial pressure

for phi in range(50,175,25):
    T=[]
    X = 'O2:0.5, N2:1.88, H2:'+str(phi/100)
    ign_delay = []
    for i in range(1500,4000,100):
        T.append(i)
        gas.TPX = i, P, X
        ign_delay.append(IgnitionDelay(gas))
    plt.plot(T, ign_delay, label="phi=%.2f" % (phi/100))

plt.legend()
plt.xlabel('Temperature [Kelvins]')
plt.ylabel('Ignition delay time [microsecons]')
#plt.yscale('log')
plt.title('Ignition delay of hydrogen-air mixture I', fontweight='bold')
plt.grid()
plt.savefig('hydrogen-const-press.png', dpi=1000)
plt.show()
