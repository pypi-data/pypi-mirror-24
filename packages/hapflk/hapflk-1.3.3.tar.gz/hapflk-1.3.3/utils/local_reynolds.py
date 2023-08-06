#!/usr/bin/env python
import sys
import re
import bz2
from os import listdir
import numpy as np
import argparse
np.seterr(all='ignore')

def reynolds_multi_allelic(Mf,nloc,decompose=False):
    '''
    Compute Reynolds distances from multiallelic loci

    Parameters:
    -----------
    
    Mf : numpy array of allele frequencies in populations
         rows are populations
         columns are allele frequencies, by loci
    nloc : number of loci

    Returns:
    --------

    dist : numpy array (n x n) of reynolds genetic distances
    numerator    : numerator of the Reynolds Distance
    denominator  : denominator of the Reynolds Distance
    '''
    npop=Mf.shape[0]
    A=np.dot(Mf,Mf.T)
    dist=np.zeros((npop,npop))
    if decompose:
        numerator=np.zeros((npop,npop))
        denominator=np.zeros((npop,npop))
    else:
        numerator=None
        denominator=None
    for i in range(npop-1):
        for j in range(i+1,npop):
            dist[i,j]=0.5*(A[i,i]+A[j,j]-2*A[i,j])/(nloc-A[i,j])
            if decompose:
                numerator[i,j]=A[i,i]+A[j,j]-2*A[i,j]
                denominator[i,j]=2*(nloc-A[i,j])
    dist=dist+dist.T
    numerator=numerator+numerator.T
    denominator=denominator+denominator.T
    return dist,numerator,denominator
   
def reynolds(Mf):
    '''
    Compute Reynolds distances from SNP allele frequencies

    Parameters:
    ----------------

    Mf : numpy array of allele frequencies in populations
          rows are populations (n), columns are markers (p).

    Returns:
    -----------

    dist : numpy array (n x n) of reynolds genetic distances
    '''
    npop,nloc=Mf.shape
    dist=np.zeros((npop,npop))
    A=np.dot(Mf,Mf.T)+np.dot((1-Mf),(1-Mf).T)
    for i in range(npop-1):
        for j in range(i+1,npop):
            dist[i,j]=0.5*(A[i,i]+A[j,j]-2*A[i,j])/(nloc-A[i,j])
    dist=dist+dist.T
    return dist

def get_pop_names(fname):
    thepop=None
    popnames=[]
    with bz2.BZ2File(fname,'r') as f:
        for i,ligne  in enumerate(f):
            if i==0:
                continue
            buf=ligne.split()
            if thepop==None:
                thepop=buf[0]
                popnames.append(buf[0])
                continue
            if buf[0]==popnames[-1]:
                continue
            else:
                popnames.append(buf[0])
    return popnames

def get_file_list(prefix=None):
    ## find all files with cluster frequencies in current directory
    if prefix is None:
        mysearch=re.compile("\w*\.kfrq\.fit_[0-9]*\.bz2$")
    else:
        mysearch=re.compile(prefix+"\.kfrq\.fit_[0-9]*\.bz2$")
    myfic=[x for x in listdir('.') if mysearch.match(x)]
    return myfic

def get_opt():
    parser=argparse.ArgumentParser()
    parser.add_argument('-p',dest='prefix',help='Work on files with prefix PREFIX',metavar='PREFIX',default=None)
    parser.add_argument('-l',dest='left',help='Leftmost coordinate to consider',default=0,type=float)
    parser.add_argument('-r',dest='right',help='rightmost coordinate to consider',default=np.inf,type=float)
    parser.add_argument('-o',dest='oprefix',help='prefix for output files',default='')
    return parser
def main():
    myparser=get_opt()
    myopts=myparser.parse_args()
    myfic=get_file_list(myopts.prefix)
    if myopts.prefix is None:
        myopts.prefix=myfic[0].split('.')[0]
    if myopts.oprefix!='':
        myopts.oprefix=myopts.oprefix+'_'
    ## SNP Reynolds
    print "Calculating Reynolds from SNP frequencies"
    with open(myopts.prefix+'.frq') as f_frq:
        head=f_frq.readline()
        my_pops=head.split()[5:]
    a=np.genfromtxt(myopts.prefix+'.frq',skip_header=1,usecols=tuple([2]+range(5,5+len(my_pops))))
    condl=a[:,0]>myopts.left
    condr=a[:,0]<myopts.right
    a=a[condl&condr,1:]
    sDR=reynolds(a.T)
    fout=open(myopts.oprefix+'hapflk_snp_reynolds.txt','w')
    print>>fout,' '.join(my_pops)
    for i in range(len(my_pops)):
        print>>fout,my_pops[i],
        print>>fout,' '.join([str(x) for x in sDR[i,]])
    ### Haplotype Reynolds
    my_pops=get_pop_names(myfic[0])
    DR_em={}
    get_EM=re.compile('_\d+.b')
    print 'Reading haplotype cluster frequencies from',len(myfic),'files'
    ## get names of loci
    locnames=np.genfromtxt(myfic[0],skip_header=1,usecols=(1),dtype=str)
    for fname in myfic:
        sys.stdout.write(fname+'\r')
        sys.stdout.flush()
        myEM=int(get_EM.findall(fname)[0][1:-2])
        a=np.genfromtxt(fname,skip_header=1,usecols=(2,3,4))
        ## subset a by position
        condl=a[:,0]>myopts.left
        condr=a[:,0]<myopts.right
        a=a[condl&condr,]
        nloc=len(set(locnames[condl&condr,]))
        nclus=len(set(a[:,1]))
        npop=a.shape[0]/(nclus*nloc)
        start_pop=range(0,a.shape[0],nclus*nloc)
        print a.shape[0],nloc,nclus,npop,start_pop
        mf=np.vstack([a[x:(x+(nclus*nloc)),2] for x in start_pop])
        DR,num,den=reynolds_multi_allelic(mf,nloc,decompose=True)
        try:
            myres=DR_em[myEM]
        except KeyError:
            myres={'dist':[],'num':[],'den':[]}
            DR_em[myEM]=myres
        myres['dist'].append(DR)
        myres['num'].append(num)
        myres['den'].append(den)
    ##D1=[]
    D2=[]
    for em,val in DR_em.items():
        ##D1.append(np.mean(val['dist'],axis=0))
        D2.append(np.sum(val['num'],axis=0)/np.sum(val['den'],axis=0))
    ## by chromosome averaged over EMs
    DRm=np.mean(D2,axis=0)
    np.fill_diagonal(DRm,0)
    DRs=np.std(D2,axis=0)
    np.fill_diagonal(DRs,0)
    fout=open(myopts.oprefix+'hapflk_hap_reynolds.txt','w')
    print>>fout,' '.join(my_pops)
    for i in range(len(my_pops)):
        print>>fout,my_pops[i],
        print>>fout,' '.join([str(x) for x in DRm[i,]])

if __name__=='__main__':
    main()
