import segment
import logging

EXT = 'itx'    

def mvOpen(fname):
    """
    Open internal Igor Text File ITX
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
    
    y1=[]
    y2=[]
    x1=[]
    x2=[]
    
    speed = 0.0
    del righe[0:3]
    for rigo in righe:
        r = rigo.strip(newline)
        if r.strip() =='END':
            break
        (ffb,eeb,fff,eef)= r.split()
        if ffb.strip()=='ffb':
            continue
        if eef.strip() != 'NAN':
            x1.append(float(eef))
            y1.append(float(fff))
        if eeb.strip() != 'NAN':
            x2.append(float(eeb))            
            y2.append(float(ffb))

    segments.append(segment.segment(x1, y1))
    segments.append(segment.segment(x2, y2))
    
    r = righe[-1].strip(newline)
    r = r[r.find('"')+1:-1]
    sl = r.split(';')
    for var in sl:
        nm,val = var.split('=')
        if nm.strip() =='SC(pN/nm)':
            parameters['k'] = float(val)
        if nm.strip() == 'PullingRate(nm/s)':
            speed = float(val)/1.0e9
    
    for p in segments:
        p.speed = speed
    return parameters,info,segments