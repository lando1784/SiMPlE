import numpy as np

def gauss(x, *p):
        A, mu, sigma = p
        return A*np.exp(-(x-mu)**2/(2.*sigma**2))

def gfit(all,p0=None):
    hist = all[0]
    bin_centres=[]
    
    for i in range(len(hist)):
        bin_centres.append((all[1][i]+all[1][i+1])/2.0)
        
    if p0 == None:
        p0 = [max(hist)/1.5, bin_centres[np.argmax(hist)], 1.]
    
    from scipy.optimize import curve_fit
    coeff, var_matrix = curve_fit(gauss, bin_centres, hist, p0=p0)
    print coeff
    
    xfit = np.linspace(min(bin_centres),max(bin_centres),300)
    hist_fit = gauss(xfit, *coeff)
    
    return [coeff,(xfit, hist_fit)]    
    
def g2fit(all,p0=None):
    
    hist = all[0]
    bin_centres=[]
    
    for i in range(len(hist)):
        bin_centres.append((all[1][i]+all[1][i+1])/2.0)
    
    def gauss2(x, *p):        
        A1, mu1, sigma1, A2, mu2, sigma2 = p
        
        return gauss(x,*[A1,mu1,sigma1])+gauss(x,*[A2,mu2,sigma2])
    
    if p0 == None:
        p0 = [max(hist)/3.0, bin_centres[0], 1., max(hist)/3.0,bin_centres[-1],1.0]
    else:
        p0 = [max(hist)/3.0, p0[0], 1., max(hist)/3.0,p0[1],1.0]
    
    from scipy.optimize import curve_fit
    coeff, var_matrix = curve_fit(gauss2, bin_centres, hist, p0=p0)
    print coeff
    
    xfit = np.linspace(min(bin_centres),max(bin_centres),300)
    hist_fit = gauss2(xfit, *coeff)
    
    return [coeff,(xfit, hist_fit)]    
    
    
