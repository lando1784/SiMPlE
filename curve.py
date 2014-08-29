import mvobject
import segment
import logging
import importlib
import os
import glob

class curve(mvobject.mvobject):
    def __init__(self,  fname = None):
        defaults = {'fzfd':False,'k':1.0, 'relevant':True, 'sensitivity': 50.0}
        #internal units
        #  sensitivity nm/V
        #  k pN/nm
        #  speed nm/s
        #  Z nm
        #  F pN
        self.parseConfig(defaults,'Curve')

        self.filename = ''
        self.basename = ''
        self.segments=[]
        self.info={}

        if fname != None:
            self.filename = fname
            self.basename = os.path.basename(fname)
            self.open(fname)
        return
    def __iter__(self):
        return self.segments.__iter__()
    def __nonzero__(self):
        return self.relevant
    def __len__(self):
        return len(self.segments)
    def __getitem__(self, index):
        if index=='up':
            index = -1
        if index == 'down':
            index = 0
        return self.segments[index]

    def append(self,seg):
        if isinstance(seg,segment.segment):
            self.segments.append(seg)
        else:
            logging.error('You need to append a full instance of segment')
        
    def open(self,fname,driver=None):
        if not os.path.isfile(fname):
            logging.error("The file {0} does not exist".format(fname))
            return False

        #search for the specific driver
        import open_all as opa
        op = opa.opener(fname)
        try:
            parameters,info,segments=op.getOpener(driver)
        except:
            raise

        if len(segments)==0:
            logging.error("Empty File {0} not appended".format(fname))
            return False
            
        for k,v in parameters.items():
            setattr(self,k,v)
        self.info = info
        for s in segments:
            self.append(s)

    def save(self,fname=None,driver='jpktxt'):
        if fname == None:
            return False

        try:
            iname = 'save_{0}'.format(driver)
            sv = importlib.import_module(iname)
        except ImportError:
            logging.error("Save Driver {0} NOT found".format(driver))
            return False
        return sv.mvSave(self)


    def look(self):
        import pylab
        pylab.figure()
        i=0
        for p in self.segments:
            i+=1
            if p.show:
                pylab.plot(p.z,p.f,label='{0}.{1}'.format(i,p.direction))

        fragments = self[-1].getPLA()
        if(len(fragments)>=2):
            pylab.plot((fragments[0][0],fragments[0][2]),(fragments[0][1],fragments[0][3]),'k--',label='Lin')
            pylab.plot((fragments[-1][0],fragments[-1][2]),(fragments[-1][1],fragments[-1][3]),'k--',label='Flat')
        else:
            print "No PLA available"

        pylab.legend(loc=4)
        pylab.title(self.basename)
        pylab.xlabel('Displacement [nm]')
        pylab.ylabel('Force [pN]')
        pylab.show()

    def preLook(self):        
        import pylab
        pylab.figure()
        
        pylab.plot(self[-1].z,self[-1].f,label='Data')
        
        fragments = self[0].getPLA()
        if(len(fragments)>=2):
            pylab.plot((fragments[0][0],fragments[0][2]),(fragments[0][1],fragments[0][3]),'g--',label='Lin')
            pylab.plot((fragments[-1][0],fragments[-1][2]),(fragments[-1][1],fragments[-1][3]),'r--',label='Flat')
        else:
            print "No PLA available"
        pylab.title(self.basename)          
        pylab.legend(loc=4)
        pylab.xlabel('Displacement [nm]')
        pylab.ylabel('Force [pN]')
        pylab.show()
        