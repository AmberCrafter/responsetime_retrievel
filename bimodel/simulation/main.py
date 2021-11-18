import numpy as np
import matplotlib.pyplot as plt

import find_responseTime

def true_case(number,sp,ep):
    res = np.linspace(sp,ep,number,True)
    # res = np.cos(res)
    return res

def response(sp,ep,time,tau):
    return sp + (ep-sp)*(1-np.exp(-time/tau))

def main():
    resp1 = 12.03
    resp2 = 1.015
    true_value = true_case(101,25,20)
    case1 = [true_value[0]]
    case2 = [true_value[0]]


    for val in true_value[1::]:
        case1.append(response(case1[-1],val,1,resp1))
        case2.append(response(case2[-1],val,1,resp2))


    sim_true = [true_value[0]]
    sim_tau = []
    for i in range(len(case1)-1):
        sim_true.append(case1[i]+(case1[i+1]-case1[i])/(1-np.exp(-1/2.013)))
        sim_tau.append(-1/(np.log(1-(case2[i+1]-case2[i])/(sim_true[i+1]-case2[i]))))


    case1_responseTime,case2_responseTime = find_responseTime.tester(1,case1[20:40:],case2[20:40:])
    print(case1_responseTime)
    print(case2_responseTime)


    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(true_value,label='true')
    ax.plot(case1,label='case1')
    ax.plot(case2,label='case2')
    ax.legend()


    axr = plt.gca().twinx()
    # axr.plot(sim_tau, color='k')
    # axr.plot(np.diff(case2)/np.array([x1-x2 for x1,x2 in zip(case1[1:],case2[:-1])]),'k',label='case2-case1')
    # axr.plot(np.diff(case1)/np.array([x1-x2 for x1,x2 in zip(true_value[1:],case1[:-1])]),color='C3',label='case1-true')
    # axr.plot(np.diff(case2)/np.array([x1-x2 for x1,x2 in zip(true_value[1:],case2[:-1])]),color='C4',label='case2-true')
    # axr.set_ylim([0,1])

    axr.plot(np.diff(case1),'--')
    axr.plot(np.diff(case2),'--')
    axr.legend()
    plt.show()
    pass


if __name__=='__main__':
    main()