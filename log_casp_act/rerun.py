import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]
rerun_files = []
dont_rerun = []
for f in files:
    if f[-4:] == '.out':
        # print f
        rerun = True
        with open(f) as op:
            lines = op.readlines()
            for line in lines:
                if line[:7] == ' ln(ev)':
                    # print line
                    rerun = False
        if rerun:
            rerun_files.append(f)
        else:
            dont_rerun.append(f)

rerun_index = []
for each in rerun_files:    
    rerun_index.append(int((each.split('_')[-1].split('.')[0])))
rerun_index.sort()

dont_rerun_index = []
for each in dont_rerun:
    dont_rerun_index.append(int((each.split('_')[-1].split('.')[0])))
dont_rerun_index.sort()

new_rerun = []
for each in rerun_index:
    if each not in dont_rerun_index:
        new_rerun.append(each)
rerun_index = new_rerun
len_rerun = len(rerun_index)
for i, each in enumerate(rerun_index):
    rerun_index[i] = str(rerun_index[i])
rerun_list = ','.join(rerun_index)
print rerun_list
print len_rerun
