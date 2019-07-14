
from os import walk, getcwd, listdir
import re

models = []
current_path = getcwd()
for each in listdir(current_path):
    if re.match(r'model.[0-9]+.py\Z', each):
        models.append(each)

for each in models:

    filename = 'run_' + each
    f = open(filename, 'w+')
    f.write('\nimport numpy as np\n')
    f.write('from math import *\n')
    f.write('import pymultinest\n')
    f.write('import sys\n')
    f.write('sys.path.insert(0, \'/path/to/pysb\')\n')
    f.write('from pysb.integrate import Solver\n')
    f.write('import csv\n')
    f.write('import time as tm\n')
    f.write('from ' + each[:-3] + ' import model\n')
    f.write('from pysb.pathfinder import set_path\n')
    f.write('set_path(\'bng\', \'/path/to/BioNetGen\')\n\n')
    f.write('\n')

    f.write('data_object = []\n')
    f.write('with open(\'earm_data.csv\') as data_file:\n')
    f.write('	reader = csv.reader(data_file)\n')
    f.write('	line = list(reader)\n')
    f.write('	for each in line:\n')
    f.write('		data_object.append(each)\n')
    f.write('for i, each in enumerate(data_object):\n')
    f.write('	if i > 0:\n')
    f.write('		for j, item in enumerate(each):\n')
    f.write('			data_object[i][j] = float(data_object[i][j])\n')
    f.write('data_object = data_object[1:]\n\n')

    f.write('time = []\n')
    f.write('for each in data_object:\n')
    f.write('	time.append(float(each[0]))\n\n')

    f.write('model_solver = Solver(model, time, integrator=\'vode\', integrator_options={\'atol\': 1e-12, \'rtol\': 1e-12})\n\n\n')

    f.write('def prior(cube, ndim, nparams):\n\n')

    f.write('	for k, every in enumerate(model.parameters):\n')
    f.write('		if every.name[-3:] == \'1kf\':\n')
    f.write('			cube[k] = cube[k]*4 - 4\n')
    f.write('		if every.name[-3:] == \'2kf\':\n')
    f.write('			cube[k] = cube[k]*4 - 8\n')
    f.write('		if every.name[-3:] == \'1kr\':\n')
    f.write('			cube[k] = cube[k]*4 - 4\n')
    f.write('		if every.name[-3:] == \'1kc\':\n')
    f.write('			cube[k] = cube[k]*4 - 1\n\n\n')

    f.write('postfixes = [\'1kf\', \'2kf\', \'1kr\', \'1kc\']\n\n\n')

    f.write('def loglike(cube, ndim, nparams):\n\n')

    f.write('	point = []\n')
    f.write('	cube_index = 0\n')
    f.write('	for k, every in enumerate(model.parameters):\n')
    f.write('		if every.name[-3:] in postfixes:\n')
    f.write('			point.append(10**cube[cube_index])\n')
    f.write('			cube_index += 1\n')
    f.write('		else:\n')
    f.write('			point.append(model.parameters[k].value)\n')
    f.write('	model_solver.run(point)\n')
    f.write('	failed = False\n')
    f.write('	for every in model_solver.yobs:\n')
    f.write('		for thing in every:\n')
    f.write('			if thing <= -0.00000001 or np.isnan(thing):\n')
    f.write('				failed = True\n')
    f.write('	if failed:\n')
    f.write('		return [\'fail\', -10000.0]\n')
    f.write('	else:\n')
    f.write('		parpc = model_solver.yobs[-1][8]/(model_solver.yobs[-1][1] + model_solver.yobs[-1][8])\n')
    f.write('		if (parpc > 0.0) and (parpc < 1.00000001):\n')
    f.write('			print log(parpc), point\n')
    f.write('			return [\'sim\', log(parpc)]\n\n\n')
    f.write('		else:\n')
    f.write('			return [\'fail\', -10000.0]\n')
    f.write('n_params = 0\n')
    f.write('for m, lotsa in enumerate(model.parameters):\n')
    f.write('	if lotsa.name[-3:] == \'1kf\':\n')
    f.write('		n_params += 1\n')
    f.write('	if lotsa.name[-3:] == \'2kf\':\n')
    f.write('		n_params += 1\n')
    f.write('	if lotsa.name[-3:] == \'1kr\':\n')
    f.write('		n_params += 1\n')
    f.write('	if lotsa.name[-3:] == \'1kc\':\n')
    f.write('		n_params += 1\n\n')
    
    f.write('start_time = tm.clock()\n')
    f.write('counts = [0, 0]\n')
    f.write('pymultinest.run(loglike, prior, n_params, evidence_tolerance=0.0001, n_live_points=16000, log_zero=-1e3, sampling_efficiency=0.3, outputfiles_basename=\'/path/to/log_mito_bcl2/output/' + each.split('_')[1][:-3] +  '/\', resume = False, verbose = False, counts=counts)\n\n')
    f.write('print counts\n')
    f.write('print \'start time\', start_time\n')
    f.write('print \'end time\', tm.clock()')

    f.close()

