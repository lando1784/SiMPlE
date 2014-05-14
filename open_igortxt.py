import segment
import logging

EXT = 'dat'    
        
def mvOpen(fname):
    """
    Open Igor exported TXT files
    """
    parameters={}
    info={}
    segments=[]
        
    parameters['k'] = 1.0               

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
        logging.error('File {0} is not an ascii file'.format(fname))
    
    y1=[]
    y2=[]
    x1=[]
    x2=[]
    
    speed = 0.0
    for rigo in righe:
        r = rigo.strip(newline)
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

    for p in segments:
        p.speed = speed
        
    return parameters,info,segments
