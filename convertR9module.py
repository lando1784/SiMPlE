from os import listdir, makedirs
from os.path import join, isfile, splitext, exists
import sys
import numpy as np

if len(sys.argv)>1:
    dir = sys.argv[1]
else:
    dir = '/home/ettore/Dati/txt'
    dir2 = '/home/ettore/Dati/txt/jpk'

def headerWriter(k,nmV,x,y,speed):
    
    header1 = str('# TEXT EXPORT\n' +
                 '# \n' +
                 '# Software version: N.A.\n' +
                 '# \n' +
                 '# xpos: ' + str(x) + '\n' +
                 '# ypos: ' + str(y) + '\n' +
                 '# fzfd: 1\n' +
                 '# \n' +
                 '# \n' +
                 '# segmentIndex: 0\n' +
                 '# segment: extend\n' +
                 '# columns: strainGaugeHeight vDeflection\n' +
                 '# fancyNames: distance[m], force[N]\n' +
                 '# springConstant: ' + str(k) + '\n' +
                 '# sensitivity: ' + str(nmV*1e-9) + '\n' +
                 '# units: m N\n' +
                 '# speed: ' + str(speed*1e-9) + '\n' +
                 '# \n' +
                 '# \n'
                 )
    
    header2 = str(' \n' +
                 '# \n' +
                 '# segmentIndex: 1\n' +
                 '# segment: retract\n' +
                 '# columns: strainGaugeHeight vDeflection\n' +
                 '# fancyNames: distance[m], force[N]\n' +
                 '# springConstant: ' + str(k) + '\n' +
                 '# sensitivity: ' + str(nmV*1e-9) + '\n' +
                 '# units: m N\n' +
                 '# speed: ' + str(speed*1e-9) + '\n' +
                 '# \n' +
                 '# \n'
                 )
    
    return header1,header2


def tabulate2Darray(a,separator='\t'):
    
    tab = ''
    
    for i in xrange(a.shape[0]):
        for j in xrange(a.shape[1]):
            tab+=str(a[i,j])+(separator if j<a.shape[1]-1 else '\n')
            
    return tab


def chopR9file(filePath):
    temp = open(filePath,'r')
    h = True
    header = ''
    data = []
    for l in temp:
        cols = []
        if h:
            header += (l)
        else:
            chopped = np.array([float(d) for d in l.split('\t')[1:]])
            if chopped.shape[0]>0:
                data.append(chopped)
        if l.find(';')!=-1:
            chopped1 = l.replace(';','')
            chopped2 = chopped1.split('involts=')
            k = float(chopped2[0].replace('kappa=',''))
            nmV = float(chopped2[1])
        if l.find('X_pixel')!=-1:
            xs = np.array([float(d) for d in l.split('\t')[2:]])
        if l.find('Y_pixel')!=-1:
            ys = np.array([float(d) for d in l.split('\t')[2:]])
            h = False
    params = [k,nmV]
    columns = data[0].shape[0]
    rows = len(data)
    data = np.array(data)
    np.reshape(data, [rows,columns])
    Z = data[:,0]
    Dapps = data[:,1:-1:2]
    Drets = data[:,2::2]
    xs = xs[::2]
    ys = ys[::2]
    toNewton = k*nmV*1e-9
    curves = []
    for i in xrange((columns-1)/2):
        tempApp = np.array([Z,Dapps[:,i]*toNewton])
        tempRec = np.array([Z[::-1],Drets[::-1,i]*toNewton])
        tempH1,tempH2 = headerWriter(k,nmV,xs[i],ys[i],1)
        tempAppT = tabulate2Darray(tempApp.transpose())
        tempRecT = tabulate2Darray(tempRec.transpose())
        tempCurve = tempH1 + tempAppT + tempH2 + tempRecT
        curves.append(tempCurve)
    temp.close()
    
    return curves
    
    
def batchR9conversion(dirIn,dirOut=''): 
    files = [f for f in listdir(dirIn) if (isfile(join(dirIn,f)) and splitext(join(dirIn,f))[1]=='.txt')]
    headers = []
    datas = []
    params = []
    if not exists(dirOut):
        makedirs(dirOut)
    for f in files:
        fileTexts = chopR9file(join(dirIn,f))
        counter = 1
        for t in fileTexts: 
            newf = 'jpkEquiv_'+str(counter)+'_'+f
            if not exists(join(dirOut,splitext(f)[0])):
                makedirs(join(dirOut,splitext(f)[0]))
            w = open(join(join(dirOut,splitext(f)[0]),newf),'w')
            w.write(t)
            w.close()
            counter+=1

if __name__ == '__main__':
    batchR9conversion(dir,dir2)
