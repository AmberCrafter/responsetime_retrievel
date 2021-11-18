import numpy as np

def main(resolution,x1,x2, guess_x1_response_time=1, defaut_delta=1):
    '''
    Get two list data
    resolution: @float, data sample resolution
    x1: @list
    x2: @list

    and x1 is referance
    Note. to make sure x1[0], x2[0] is the base value mesurement 
        under same condition with same base line
    '''
    flag = 0
    x1 = np.array(x1)
    x2 = np.array(x2)


    # find x1 response time
    while abs(defaut_delta)>10e-10:
        sim_true = [(x1[0]+x2[0])/2]
        sim_tau = []
        for i in range(len(x1)-1):
            sim_true.append(x1[i]+(x1[i+1]-x1[i])/(1-np.exp(-resolution/guess_x1_response_time)))
        
        # first tau
        i=0
        sim_tau.append(-resolution/(np.log(1-(x2[i+1]-x2[i])/(sim_true[i+1]-x2[i]))))

        # last tau
        i=-2
        sim_tau.append(-resolution/(np.log(1-(x2[i+1]-x2[i])/(sim_true[i+1]-x2[i]))))

        # 決定收斂方向與增益
        if sim_tau[1]-sim_tau[0]>0:
            if flag<0:
                defaut_delta*=-0.5
                flag=1
            if flag==0: flag=1
        else:
            if flag>0:
                defaut_delta*=-0.5
                flag=-1
            if flag==0: flag=-1
        print(defaut_delta)

        guess_x1_response_time+=defaut_delta
    x1_response_time = guess_x1_response_time-defaut_delta


    # find x2 response time
    x2_response_time = sim_tau[-1]
    return x1_response_time, x2_response_time

import numpy as np

def tester(resolution,x1,x2, guess_x1_response_time=0.1, defaut_delta=0.1):
    '''
    Get two list data
    resolution: @float, data sample resolution
    x1: @list
    x2: @list

    and x1 is referance
    Note. to make sure x1[0], x2[0] is the base value mesurement 
        under same condition with same base line
    '''
    # import matplotlib.pyplot as plt
    flag = 0
    x1 = np.array(x1)
    x2 = np.array(x2)
    # fig = plt.figure(figsize=[10.24,7.68],dpi=100)
    # ax = fig.add_subplot(1,1,1)

    if np.nanmean(x1)>np.nanmean(x2):
        dummy = x1.copy()
        x1 = x2.copy()
        x2 = dummy

    # find x1 response time
    while abs(defaut_delta)>10e-10:
        # sim_true = [np.min(x1[0]+x2[0])]
        sim_true = [np.nanmean(x1[0]+x2[0])]
        sim_tau = []
        for i in range(len(x1)-1):
            sim_true.append(x1[i]+(x1[i+1]-x1[i])/(1-np.exp(-resolution/guess_x1_response_time)))
        
        tau_dummy = []
        for i in range(len(sim_true)-1):
            tau_dummy.append(-resolution/(np.log(1-(x2[i+1]-x2[i])/(sim_true[i+1]-x2[i])))) 

        tau_dummy = np.array(tau_dummy)
        x = np.arange(len(tau_dummy))
        mask = np.isfinite(tau_dummy)
        tau_dummy = np.interp(x,x[mask],tau_dummy[mask])

        # first tau
        i=1
        sim_tau.append(-resolution/(np.log(1-(x2[i+1]-x2[i])/(sim_true[i+1]-x2[i]))))

        # last tau
        i=-2
        sim_tau.append(-resolution/(np.log(1-(x2[i+1]-x2[i])/(sim_true[i+1]-x2[i]))))
        fp = np.polyfit(np.arange(len(tau_dummy))*resolution,tau_dummy,1)

        # 決定收斂方向與增益
        # if sim_tau[1]-sim_tau[0]>0:
        if fp[0]>0:
            if flag<0:
                defaut_delta*=-0.5
                flag=1
            if flag==0: flag=1
            # if flag==1: defaut_delta*=1.2
        else:
            if flag>0:
                defaut_delta*=-0.5
                flag=-1
            if flag==0: flag=-1
            # if flag==-1: defaut_delta*=1.2
        # if defaut_delta>5: defaut_delta=5
        print(defaut_delta,guess_x1_response_time, sim_tau, np.diff(sim_tau))

        guess_x1_response_time+=defaut_delta

        # if guess_x1_response_time>1000: 
        #     # plt.show()
        #     guess_x1_response_time=np.nan
        #     break
    x1_response_time = guess_x1_response_time-defaut_delta
    # plt.show()


    # find x2 response time
    x2_response_time = np.nanmean(tau_dummy)
    return x1_response_time, x2_response_time