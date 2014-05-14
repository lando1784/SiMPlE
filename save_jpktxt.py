import logging
def mvSave(self, fname):
    """
    Save the curve in a TXT format compatible with the text export format of JPK IP and DP programs
    """
    if fname == '':
        return False
    out_file = open(str(fname),"w")
    out_file.write("# TEXT EXPORT\n")
    out_file.write("# springConstant: {0}\n".format(self.k))
    out_file.write("# units: m N\n")    
    if self.fzfd:
        out_file.write("# fzfd: 1\n")
    else:
        out_file.write("# fzfd: 0\n")
    out_file.write("#\n")
    i=0
    for p in self.pieces:
        if i != 0:
            out_file.write("\n")
        out_file.write("#\n")
        out_file.write("# segmentIndex: {0}\n".format(i))
        ts = 'extend'
        if p.direction == 'B':
            ts = 'retract'
        out_file.write("# segment: {0}\n".format(ts))
        out_file.write("# columns: distance force\n")
        out_file.write("# speed: {0}\n".format(p.speed))
        for i in range(len(p.x)):
            out_file.write("{0} {1}\n".format(p.x[i]*1e-9, -1.0*p.y[i]*1e-12))
        i+=1
    out_file.close()
    return True