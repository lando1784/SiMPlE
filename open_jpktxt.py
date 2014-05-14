import segment
import logging
import string

EXT = 'txt' 

def parseConfigLine(cline,newline='\r\n'):
    line = cline[2:-len(newline)]
    # columns: vDeflection strainGaugeHeight
    # fancyNames: "Vertical deflection" "Height (measured)"
    if line.find(':')==-1:
        return False
    fragments = line.split(':')
    name = fragments[0]
    post = string.join(fragments[1:],':').strip()
    if post.find('"')==-1:
        val = post.split(' ')
    else:
        val = post[1:-1].split('" "')
    if len(val)==1:
        val = val[0]
    return name,val
    

def mvOpen(fname):
    """
    Open JPK exported TXT files
    """
    parameters={}
    info={}
    segments=[]
    
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
        return False
    x=[]
    y=[]
    
    direction = None
    channels = 2
    chNames = ['Displacement','Force']
    chZ = 0
    chF = 1
    k = 1.0
    invOls = 50 #sensitivity in nm/V
    
    #try:
    if True:
        speed = 0.0
        for rigo in righe:
            if rigo[0] != '#' and len(rigo) > len(newline):
                separator = ' '
                if rigo.find(separator)==-1:
                    separator='\t'
                    invert = True        
                datas = rigo[:-len(newline)].split(separator)
                xi = datas[chZ]
                yi = datas[chF]            
                x.append(float(xi)*1e9)
                y.append(-1.0*float(yi)*1e12)
                
            else:
                ex = parseConfigLine(rigo,newline)
                if ex != False:
                    name,val = ex
                    if name == 'units':
                        units = val
                    elif name == 'segmentIndex':
                        if len(x)>0 and len(y)>0:
                            segments.append(segment.segment(x,y))
                            segments[-1].speed = speed
                            segments[-1].k = k
                            if direction != None:
                                segments[-1].direction = direction
                        direction = None
                        speed = 1.0
                        x = []
                        y = []
                    elif name == 'springConstant':
                        parameters['k'] = 1000.0*float(val) #internally k is in pN/nm
                        k = parameters['k']
                    elif name=='segment':
                        direction = val
                        if val == 'extend':
                            direction='near'
                        elif val == 'retract':
                            direction = 'far'
                    elif name == 'columns':
                        i = 0
                        channels = len(val)
                        for v in val:
                            if v == 'strainGaugeHeight':
                                chZ = i
                            elif v == 'capacitiveSensorHeight':
                                chZ = i
                            elif v == 'vDeflection':
                                chF = i
                            i+=1                            
                    elif name == 'fzfd':
                        if val == '1' or val == 'True':
                            parameters['fzfd'] = True
                    elif name == 'fancyNames':
                        chNames = val
                    elif name == 'sensitivity':
                        parameters['sensitivity'] = 1.0e9*float(val) #internally in nm/V
                    elif name == 'speed':
                        speed = 1.0e9*float(val) #internally in nm/s 
                    
        if x[len(x)-1]<x[0]:
            x.reverse()
            y.reverse()
    #except:
    #    logging.error('File cannot be interpreted as JPK FD curve')
    #    return False
    if len(x)>0 and len(y)>0:
        segments.append(segment.segment(x,y))
        segments[-1].speed = speed
        segments[-1].k = k
        if direction != None:
            segments[-1].direction = direction
    return parameters,info,segments
