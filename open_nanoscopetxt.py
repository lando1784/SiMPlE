import segment
import logging

EXT = 'nano'    

import numpy as np

def mvOpen(fname):
    """
    Open exported text files from nanoscope (versions ? Implementation is not robust)
    """
    parameters={}
    info={}
    segments=[]
    
    parameters['k'] = 1.0
    speed = 0.0
    
    in_file = open(str(fname),"r")
    righe = in_file.readlines()
    in_file.close()
    newline = '\n'

    try:
        if righe[10][-2:]=='\r\n':
            newline = '\r\n'
        elif righe[10][-1:]=='\r':
            newline = '\r'
    except:
        logging.error('File is not an ascii file')

    o = 0
    i = 0
    
    r = righe[0].strip(newline)
    r = r.strip('"')
    r = r.strip('\\')
    
    while r != '*File list end':
        r = righe[i].strip(newline)
        r = r.strip('"')
        r = r.strip('\\')

        if o==0 and r=='*Scanner list':
            o+=1
        elif o==1 and r=='*Ciao scan list':
            o+=1
        elif o==2 and r=='*Ciao force list':
            o+=1
        elif o==3 and r=='*Ciao force image list':
            o+=1
        
        if r.find(':') > 0:
            g = r.split(':')
            if len(g)==2:
                (pre,post) = g 
            else:
                pre=g[0]+':'+g[1]
                post=g[2]  
            pre = pre.strip()
            post=post.strip()
                                
            if o == 1:
                if pre == '@Sens. Zsens':
                    post=post.split()
                    zsens = float(post[-2])
                    info['zsens']=zsens
            elif o==2:
                if pre=='@Sens. DeflSens':
                    post=post.split()
                    deflsens = float(post[-2])
                    info['deflsens']=deflsens
            elif o==3:
                if pre == 'Scan rate':
                    scanrate = float(post)
                    info['scanrate']=scanrate                        
                elif pre=='@4:Ramp size Zsweep':
                    post=post.split()
                    rampsize = float(post[-2])
                elif pre=='@Z scan start':
                    post=post.split()
                    zstart = float(post[-2])
                    info['zstart']=zstart
                elif pre=='@Z scan size':
                    post=post.split()
                    zsize = float(post[-2])
                    info['zsize']=zsize
                if pre == 'Forward vel.':
                    fspeed = float(post)
                    info['fspeed']=fspeed
                if pre == 'Reverse vel.':
                    bspeed = float(post)
                    info['bspeed']=bspeed
            elif o==4:
                if pre=='Samps/line':
                    post=post.split()
                    sampline = int(post[-1])
                elif pre=='Spring Constant':
                    parameters['k'] = 1000.0*float(post)                        
                elif pre=='@4:Z scale':
                    post=post.split()
                    zscale = float(post[-2])
                    info['zscale']=zscale
        i+=1
    y1=[]
    y2=[]
    x=[]
            
    for j in range(i+2,len(righe)):
        rigo = righe[j].split()
        x.append((j-i-2)*zsens*rampsize/float(sampline))            
        y1.append(-parameters['k']*float(rigo[0]))
        y2.append(-parameters['k']*float(rigo[1]))
    
    x = np.array(x)
    y1.reverse()
    y1 = np.array(y1)
    y2 = np.array(y2)
    
    #test whether some points at the end/beginning of the curves are saturating
    if y1[0]==y1[1]:
        a = y1[0]
        i=0
        for yy in y1:
            i+=1
            if yy!=a:
                break
        y1 = y1[i:]
        y2 = y2[i:]
        x = x[i:]
    
    
    segments.append(segment.segment(x, y1))
    segments.append(segment.segment(x, y2))

    segments[0].speed = fspeed
    segments[1].speed = bspeed
        
    return parameters,info,segments