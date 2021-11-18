import numpy as np
from numpy.lib.arraysetops import isin

def V1_oldversion(resolution,x1,x2, guess_x1_response_time=1, defaut_delta=1):
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
        # sim_true = [np.min(x1[0]+x2[0])]
        sim_true = [np.nanmean(x1[0]+x2[0])]
        sim_tau = []
        for i in range(len(x1)-1):
            sim_true.append(x1[i]+(x1[i+1]-x1[i])/(1-np.exp(-resolution/guess_x1_response_time)))
        
        tau_dummy = []
        for i in range(len(sim_true)-1):
            tau_dummy.append(-resolution/(np.log(1-(x2[i+1]-x2[i])/(sim_true[i+1]-x2[i])))) 

        # first tau
        i=5
        sim_tau.append(-resolution/(np.log(1-(x2[i+1]-x2[i])/(sim_true[i+1]-x2[i]))))

        # last tau
        i=-6
        sim_tau.append(-resolution/(np.log(1-(x2[i+1]-x2[i])/(sim_true[i+1]-x2[i]))))


        tau_dummy = np.array(tau_dummy)
        x = np.arange(len(tau_dummy))
        mask = np.isfinite(tau_dummy)
        tau_dummy = np.interp(x,x[mask],tau_dummy[mask])
        num = int(0.25*len(tau_dummy))
        fp = np.polyfit(np.arange(len(tau_dummy[num:-num]))*resolution,tau_dummy[num:-num],1)


        # 決定收斂方向與增益
        # if sim_tau[1]-sim_tau[0]>0:
        if fp[0]>0:
            if flag<0:
                defaut_delta*=-0.5
                flag=1
            if flag==0: flag=1
        else:
            if flag>0:
                defaut_delta*=-0.5
                flag=-1
            if flag==0: flag=-1
        print(defaut_delta, guess_x1_response_time, fp, np.nanmean(tau_dummy[num:-num]))

        guess_x1_response_time+=defaut_delta

        if guess_x1_response_time>100: 
            guess_x1_response_time=np.nan
            break
    x1_response_time = guess_x1_response_time-defaut_delta


    # find x2 response time
    x2_response_time = np.nanmean(tau_dummy[num:-num])
    return x1_response_time, x2_response_time

def V2(resolution,x1,x2, guess_x1_response_time=1, defaut_delta=0.05):
    '''
    Get two list data
    resolution: @float, data sample resolution
    x1: @list
    x2: @list

    and x1 is referance
    Note. to make sure x1[0], x2[0] is the base value mesurement 
        under same condition with same base line
    '''
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=[10.24,7.68],dpi=100)
    ax = fig.add_subplot(1,1,1)
    flag = 0
    x1 = np.array(x1)
    x2 = np.array(x2)
    first_run_x2_response_time = None

    if np.nanmean(x1)>np.nanmean(x2):
        dummy = x1.copy()
        x1 = x2.copy()
        x2 = dummy

    # find x1 response time
    count = 0
    while abs(defaut_delta)>10e-10:
        sim_true = [np.nanmean(x1[0]+x2[0])]
        sim_tau = []
        for i in range(len(x1)-1):
            sim_true.append(x1[i]+(x1[i+1]-x1[i])/(1-np.exp(-resolution/guess_x1_response_time)))
        
        for i in range(len(sim_true)-1):
            sim_tau.append(-resolution/(np.log(1-(x2[i+1]-x2[i])/(sim_true[i+1]-x2[i])))) 

        sim_tau = np.array(sim_tau)
        x = np.arange(len(sim_tau))
        mask = np.isfinite(sim_tau)
        sim_tau = np.interp(x,x[mask],sim_tau[mask])

        num = int(0.25*len(sim_tau))
        fp = np.polyfit(np.arange(len(sim_tau[num:-num]))*resolution,sim_tau[num:-num],1)


        if isinstance(first_run_x2_response_time,type(None)): 
            first_run_x2_response_time=np.nanmean(sim_tau[num:-num])
            first_run_sim_tau = sim_tau[num:-num]
        # # 決定收斂方向與增益
        # if ((abs(pre_slop)-abs(fp[0]))<0): 
        #     guess_x1_response_time*=0.66
        #     defaut_delta*=-1.33
        # else:
        if fp[0]>0:
            if flag<0:
                defaut_delta*=-0.5
                flag=1
            if flag==0: flag=1
        else:
            if flag>0:
                defaut_delta*=-0.5
                flag=-1
            if flag==0: flag=-1

        guess_x1_response_time+=defaut_delta
        if guess_x1_response_time<0: 
            guess_x1_response_time=(guess_x1_response_time-defaut_delta)/2
        # pre_slop = fp[0].copy()

        count+=1
        if (guess_x1_response_time>50) | (count>1E3): 
            x1_response_time=-1
            x2_response_time=first_run_x2_response_time
            ax.plot(first_run_sim_tau)
            plt.savefig('./sim_tau.png')
            plt.show()
            return x1_response_time, x2_response_time
    x1_response_time = guess_x1_response_time-defaut_delta
    # find x2 response time
    x2_response_time = np.nanmean(sim_tau[num:-num])
    ax.plot(first_run_sim_tau)
    plt.savefig('./sim_tau.png')
    plt.show()
    return x1_response_time, x2_response_time, first_run_x2_response_time