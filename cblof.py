# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:24:15 2016

@author: MayankAgrawal
"""

import pandas as pd
import time
import numpy as np

def toFloat(x):
    return float(x)

def mutate_dict(f,d):
    for k, v in d.iteritems():
        d[k] = f( v )

def newCluster(key,currentTuple):   
    summary = []
    clusterStructure = []
    #ls = []
    for k in currentTuple:
        VS = {}                
        VS[currentTuple[k]] = 1
        summary.append([VS])

    clusterStructure.append([key])
    clusterStructure.append(summary)
    return clusterStructure

def addSame(cluster,currentTuple):
                 
    for k in currentTuple:
        if currentTuple[k] in cluster[k][0]:
            cluster[k][0][currentTuple[k]] = cluster[k][0][currentTuple[k]] + 1
        else:
            cluster[k][0][currentTuple[k]] = 1        
       

def sim(c,current):
   
    sim = 0
    for k in current:
        if current[k] in c[k][0]:
                    sup = c[k][0][current[k]]
        else: sup = 0                
        sim += (sup/float(sum(c[k][0].itervalues())))
                      
    return sim
    
    
dn = pd.read_csv("fsd.csv")    
#ds = pd.DataFrame(np.random.normal(size=(10000,20)))
ds = np.array(dn)
#df = ds[:,2]
values={}
for d in dn:
    dm = np.array(dn[d])
    for key in dm:
        if values.has_key(key):
            values[key] +=1
        else: values[key] = 1
    break

print "1"
D = {}
N = 0
t3=time.time()
while N < len(ds):
    m = 0
    D[N] = {}
    for key in ds[N]:        
        #print x
        D[N][m] = key
        m += 1
    mutate_dict(toFloat, D[N])    
    N += 1
t4=time.time()-t3
    
#SQUEEZER ALGORITHM
CS = []
t5=time.time()
for key in D:
    currentTuple = D[key]
    print "2",key
    if key == 0:
        #t1 =time.time()
        CS.append(newCluster(key,currentTuple))
        #t2 = float(time.time())-t1
    else: 
        allClusters = []            
        for c in CS:
            #print c
            #exit()
            allClusters.append(sim(c[1],currentTuple))
        
        maxSim = max(allClusters)
        index = allClusters.index(max(allClusters))
   
        # Sth is threshold value
        Sth = 5
        
        if maxSim >= Sth:            
            #add the sample to the existing cluster
            CS[index][0].append(key)
            cluster = CS[index]
            addSame(cluster[1],currentTuple)
        
        else:            
            #create new cluster
            CS.append(newCluster(key,currentTuple))
            print key
t6=time.time()-t5
#CS.append(1)
#FIND CBLOF
C = {}
for cl in CS:
    C[len(cl[0])] = cl

S = (sorted(C.keys()))
a = 0.1 #parameter alpha
sumOfCl = 0
LC = []
SC = []
for l in S:
    sumOfCl = sumOfCl + l
    if sumOfCl <= a*len(D):
        SC.append(l)
    else: LC.append(l)
t7=time.time()

CBLOF = {}
for key in D:
    current = D[key]
    
    for k in C:
        if key in C[k][0]:
            cluster = k
            break
    print "2"
    if cluster in LC:        
        s = sim(C[cluster][1],current)            
        lof = cluster*s
        CBLOF[key] = round(lof, 6)
        print "yes"
    else:
        allClusters = []
        for c in LC:
            allClusters.append(sim(C[c][1],current))
            
        maxSim = min(allClusters)            
        lof = cluster*maxSim
        CBLOF[key] = round(lof, 6)
        print "no"
    print "4"
t8=time.time()-t7
sortCblof = sorted(CBLOF, key = CBLOF.get, reverse = True)
n = 5
num = int((n/100.0)*len(sortCblof))
outliers = sortCblof[:num]
#outData = ds.ix[outliers, :]