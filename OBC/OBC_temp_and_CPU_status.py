import subprocess

def GetCPUTemps():
	process = subprocess.Popen(['sensors'], stdout=subprocess.PIPE)
	out, err = process.communicate()
	outspl = str(out).split('\n')
	temps = []
	for line in outspl:
		#parse the stdout output of the 'sensors' command which returns system temperatures
		if 'crit = ' in line and '\xc2' in line:
			linespl = line.replace('\xc2',' ').replace('Physical id ','Physicalid').replace('Core ','Core').replace('+','').split()
			temps.append(float(linespl[1]))
			#print(linespl)
	return temps

def GetCPUfrequencySettings():
	process = subprocess.Popen(['cpufreq-info'], stdout=subprocess.PIPE)
	out, err = process.communicate()
	outspl = str(out).split('\n')
	freqsLo = []
	freqsHi = []
	governors = []
	for line in outspl:
		#parse the stdout output of the 'cpufreq-info' command which returns cpu clock settings
		if 'current policy: frequency should be within' in line:
			linespl = line.split()
			if linespl[7] == 'MHz':
				freqsLo.append(int(linespl[6]))
			else:
				freqsLo.append(int(float(linespl[6])*1000.0))
			if linespl[10] == 'MHz.':
				freqsHi.append(int(linespl[9]))
			else:
				freqsHi.append(int(float(linespl[9])*1000.0))
			#print(linespl)
		if 'The governor' in line and 'may decide which speed to use' in line:
			linespl = line.replace('\"',' ').split()
			governors.append(linespl[2])
			#print(linespl)
	return (freqsLo, freqsHi, governors)

#temps = GetCPUfrequencySettings()
#print(str(temps))
