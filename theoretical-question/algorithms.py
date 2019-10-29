#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 15:38:36 2019

@author: marco
"""
import time
import matplotlib.pyplot as plt
import numpy as np

def splitSwap(a, i, n):

    if n <= 1:
        return 
    n_half = int(n/2)
    splitSwap(a, i, n_half)
    splitSwap(a, i+n_half, n_half)
    
    swapList(a, i, n)

def swapList(a, l, n):

    n_half = int(n/2)
    for i in range(0, n_half):
        tmp = a[l + i]
        a[l + i] = a[l + n_half + i]
        a[l + n_half + i] = tmp        

if __name__ == '__main__':
    
    array_sizes = []
    times = []
    x_squared = []
    log = []

    for i in range(1,2):
        n = 20
        array = list(range(1, n+1))
        #print(' Input: ', array)
        start_time = time.time()
        splitSwap(array, 0, n)
        end_time = time.time() - start_time
        
        array_sizes.append(str(n))
        times.append(end_time)
        x_squared.append(n ** 2)
        log.append(n * np.log2(n))
    
    
    ''' Execution time '''
    plt.figure(figsize=(10, 5))
    plt.plot(times, color='orange')  
    plt.xlabel('n')
    plt.ylabel('execution time')
    plt.xticks(np.arange(0, len(array_sizes)), array_sizes, rotation='vertical')
    plt.show()
    
    ''' f(x) = n log2(n) '''
    plt.figure(figsize=(10, 5))
    plt.plot(log, color='blue')  
    plt.xlabel('n')
    plt.ylabel('f(n) = n * log(n) base 2')
    plt.xticks(np.arange(0, len(array_sizes)), array_sizes, rotation='vertical')
    #plt.yticks([])
    plt.show()
    
    ''' f(x) = x ^ 2 '''
    plt.figure(figsize=(10, 5))
    plt.plot(x_squared, color='blue')  
    plt.xlabel('n')
    plt.ylabel('f(n) = x^2')
    plt.xticks(np.arange(0, len(array_sizes)), array_sizes, rotation='vertical')
    #plt.yticks([])
    plt.show()  
    
    