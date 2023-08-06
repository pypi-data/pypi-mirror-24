#!/usr/bin/env python3

import executor
from blinker import signal

outs = []
def out(sender, content):
    outs.append(content)

errs = []
def err(sender, content):
    errs.append(content)

es = []
def except_cb(sender, exception):
    es.append(exception)

def input_cb(prompt):
    return prompt + 'xyz'

def matplotlib_cb(sender, mimetype, content):
    print(mimetype, content)

signal('plutoid::stdout').connect(out)
signal('plutoid::stderr').connect(err)
signal('plutoid::exception').connect(except_cb)
signal('plutoid::matplotlib').connect(matplotlib_cb)

code = '''
s = input('enter something: ')
print(s)
'''

executor.exec_code(code, input_cb)
print('out:')
print(''.join(outs))
print('err:')
print(''.join(errs))
print('exeception:')
print(es)

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2*np.pi*t)
plt.plot(t, s)

plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')
plt.title('About as simple as it gets, folks')
plt.grid(True)
plt.show()