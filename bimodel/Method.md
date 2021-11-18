# Basic
$\delta T = \Delta T \times e^{-time/\tau}$

# Bimodel method

### Basic assumption
1. response time ($\tau$) is stable for all condition
2. 1 sec is the enough resolution to detect the sensor response time ($\tau$)
3. $\tau_{1}$ and $\tau_{2}$ has large enough different

|sec    |$T_{true}$ |$T_{obs1} (\tau_1)$    |$T_{obs2} (\tau_2)$    |
|-------|-----------|-----------------------|-----------------------|
|0      |$T_{t,0}$  |$T_{1,0}$              |$T_{2,0}$              |
|1      |$T_{t,1}$  |$T_{1,1}$              |$T_{2,1}$              |
|2      |$T_{t,2}$  |$T_{1,2}$              |$T_{2,2}$              |
|...    |...        |...                    |...                    |
|n      |$T_{t,n}$  |$T_{1,n}$              |$T_{2,n}$              |

thus.

>at 1 sec:
$T_{1,1}-T_{1,0}=(T_{t,1}-T_{1,0}) \times e^{-1/\tau_{1}}$
$T_{2,1}-T_{2,0}=(T_{t,1}-T_{2,0}) \times e^{-1/\tau_{2}}$

### Solution
1. (un)Known $\tau_{1}$
$T_{t,1}=\frac{(T_{1,1}-T_{1,0})}{(e^{-1/\tau_{1}})}+T_{1,0}$
$\tau_{2} = -1/log\frac{(T_{2,1}-T_{2,0})}{(T_{t,1}-T_{2,0})}$

> 可以假設任何$\tau_{1}$，透過基本假設1.，當得到的$\tau_{2}$隨時間變化為正斜率時，表示$\tau_{1}$太小，反之亦然。因此可透過疊代法進行收斂。

詳情可參閱simulation case。


### 資料後處理
1. 透過response time 增益後的資料，會同時將背景聲躁放大。因此需要針對反演後資料進行一定程度的濾波，降低聲躁值，可選擇使用
    - 移動平均(目前測試30秒資料較適合)
    - 巴特沃夫低通濾波器