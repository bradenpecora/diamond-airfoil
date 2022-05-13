import pandas as pd
import numpy as np
import json
import os

def to_radian(n):
    return n*np.pi/180

def to_degree(n):
    return n*180/np.pi

def find_theta(c, t, alpha, **kwargs):
    # not robust on signs
    c= float(c)
    t = float(t)
    alpha = float(alpha)

    delta = np.arctan2(t,c)
    delta = to_degree(delta)

    theta = alpha-delta
    return -1 * theta

def delta(x):
    return np.append(x[0:-1]-x[1:],0)

def find_beta(yshock, theta, c,alpha,dxa, **kwargs):
    
    alpha = abs(to_radian(alpha))
    x0 = c*np.cos(alpha)
    y0 = c*np.sin(alpha)
    x1 = abs(dxa)
    y1 = abs(yshock)

    dy = y0-y1
    dx = x0-x1
    beta = np.arctan2(dy,dx)
    beta = to_degree(beta)
    return beta

def main(mach = 5):
    mach_dir = 'mach{}/'.format(mach)

    thetabeta = pd.DataFrame(columns=['theta','beta'])

    for wd in [ f.path for f in os.scandir(mach_dir) if f.is_dir() ]:
        param_f = open(wd+'/parameters.json')
        params = json.load(param_f)
        params = {key: float(value) for key, value in params.items()}
        theta = find_theta(**params)

        stop_time = int(params['stop_time'])
        line = pd.read_csv("{}/postProcessing/singleGraph/{}/line_U.csv".format(wd,stop_time))
        line['umag'] = line.apply(lambda x: np.sqrt(x.U_0**2 + x.U_1**2 + x.U_2**2),axis=1)

        y = np.array(line['y'])
        umag = np.array(line['umag'])
        dy = delta(y)
        du = delta(umag)
        
        y = y + dy/2 #can comment out?
        dudy = du/dy

        df = pd.DataFrame({'y':y,'umgag':umag,'dudy':dudy})
        yshock = df.iloc[df['dudy'].idxmin()+1]['y'] #can remove '+1'?

        beta = find_beta(yshock=yshock,theta=theta,**params)
        this_thetabeta = pd.DataFrame({'theta':[theta],'beta':[beta]})
        thetabeta = pd.concat([thetabeta,this_thetabeta],ignore_index=True)

    thetabeta.to_csv(mach_dir+'thetabeta.csv')


if __name__ == '__main__':
    main()