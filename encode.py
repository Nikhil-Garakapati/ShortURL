import math
import string
from flask import Flask, request, render_template, redirect
import sqlite3
from urlparse import urlparse


def base62(num):
    
    '''Using Base62 enconding as it gives 3.5 trillion combinations'''
    
    base = string.digits + string.lowercase + string.uppercase
    hashed_string = ''
    while num > 0:
        hashed_string = base[num % 62] + hashed_string
        num = num/62
    return hashed_string


#print(base62(23232344))

def base10(num):
    
    base = string.digits + string.lowercase + string.uppercase
    limit = len(num)
    dec = 0
    for i in xrange(limit):
        dec = 62 * dec + base.find(num[i])
    return dec