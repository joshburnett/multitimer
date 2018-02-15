import multitimer
from time import clock, sleep
from pprint import pprint

#%%
a = []
def test_func():
    a.append(clock()-rpt.starttime)


rpt = multitimer.RepeatingTimer(interval=.05, ontimeout=test_func, count=10)
rpt.start()

sleep(1.5)

pprint(a)


#%%
def output_func(output):
    print('{.3f}: {}'.format(clock()-rpt.starttime, output))


output_dict = {'output': 'original'}
rpt = multitimer.RepeatingTimer(interval=1, ontimeout=output_func, params=output_dict, count=5, runonstart=False)
rpt.start()

sleep(2.5)
output_dict['output'] = 'modified'

#%%
sleep(3)

#%%
a = []
def test_func():
    a.append(clock()-rpt._timer.starttime)


rpt = multitimer.MultiTimer(interval=.05, ontimeout=test_func, count=10)
rpt.start()
sleep(1)
pprint(a)

print('\n')
a = []
rpt.start()
sleep(1)
pprint(a)


#%%
def output_func(output):
    print(f'{time.clock()-rpt._timer.starttime:.3f}: {output}')


output_dict = {'output': 'original'}
rpt = multitimer.MultiTimer(interval=1, ontimeout=output_func, params=output_dict, count=5, runonstart=True)
rpt.start()

sleep(2.5)
output_dict['output'] = 'modified'

sleep(3)

output_dict['output'] = 'changed to something else for another try'
rpt.start()

sleep(2.5)
output_dict['output'] = 'modified yet again'




#%%
def output_func(output):
    print(f'{clock()-rpt._timer.starttime:.3f}: {output}')


output_dict = {'output': 'original'}
rpt = multitimer.MultiTimer(interval=1, ontimeout=output_func, params=output_dict, count=8, runonstart=True)
rpt.start()

sleep(2.5)
output_dict['output'] = 'modified'
sleep(1)
rpt.start()
