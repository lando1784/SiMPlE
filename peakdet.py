import numpy as np
def peakdet(v, delta, x = None, show = False):
    """
    Converted from MATLAB script at

    Returns two arrays

    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

    """
    maxtab = []
    mintab = []

    if x is None:
        x = np.arange(len(v))

    v = np.asarray(v)

    if len(v) != len(x):
        exit('Input vectors v and x must have same length')

    if not np.isscalar(delta):
        exit('Input argument delta must be a scalar')

    if delta <= 0:
        delta = 1
        raise Exception('Input argument delta must be positive; value set to 1')

    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN

    lookformax = True

    for i in np.arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            #mxpos = x[i]
            mxpos = i
        if this < mn:
            mn = this
            #mnpos = x[i]
            mnpos = i

        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                #mnpos = x[i]
                mnpos = i
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = i
                #mxpos = x[i]
                lookformax = True

    maxi,mini = np.array(maxtab), np.array(mintab)
    if show:
        import pylab as py
        py.plot(x,v,'b-')
        py.plot(mini[:,0],mini[:,1],'og')
        py.plot(maxi[:,0],maxi[:,1],'or')
    return maxi,mini