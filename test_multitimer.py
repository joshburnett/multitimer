import multitimer
from time import perf_counter, sleep
from pprint import pprint


#%%
def test_func():
    raw_times.append(perf_counter() - rpt.starttime)


raw_times = []
interval = 0.1
rpt = multitimer.RepeatingTimer(interval=interval, ontimeout=test_func, count=10)
rpt.start()

sleep(1.5)

a0 = raw_times[0]
intervals = [t - a0 for t in raw_times]
offsets = [t % interval for t in intervals]

print('Intervals:')
pprint(intervals)

print('\nOffsets from ideal intervals:')
pprint(offsets)


#%%
def output_func(output):
    print('{:.3f}: {}'.format(perf_counter()-rpt.starttime, output))


output_dict = {'output': 'original'}
rpt = multitimer.RepeatingTimer(interval=1, function=output_func, kwargs=output_dict, count=5, runonstart=False)
rpt.start()

sleep(2.5)
output_dict['output'] = 'modified'

#%%
sleep(3)


#%%
def test_func():
    raw_times.append(perf_counter() - rpt.starttime)


raw_times = []
rpt = multitimer.MultiTimer(interval=.05, function=test_func, count=10)
rpt.start()
sleep(1)
pprint(raw_times)

print('\n')
raw_times = []
rpt.start()
sleep(1)
pprint(raw_times)


#%%
def output_func(output):
    print(f'{perf_counter()-rpt.starttime:.3f}: {output}')


output_dict = {'output': 'original'}
rpt = multitimer.MultiTimer(interval=1, function=output_func, kwargs=output_dict, count=5, runonstart=True)
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
    print(f'{perf_counter()-rpt.starttime:.3f}: {output}')


output_dict = {'output': 'original'}
rpt = multitimer.MultiTimer(interval=1, function=output_func, kwargs=output_dict, count=8, runonstart=True)
rpt.start()

sleep(2.5)
output_dict['output'] = 'modified'
sleep(1)
rpt.start()  # should re-start the MultiTimer
