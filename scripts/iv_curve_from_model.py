import subprocess, os

if os.path.basename(os.getcwd()) != 'scripts':
    print("Run this from the scripts directory")
    exit()

#make a "sandox" for the large number of files being generated
try:
    os.mkdir('simfiles')
except OSError:
    pass

os.chdir('simfiles')

subprocess.call(['pynml-channelanalysis', '-temperature', '34',  '-minV', '-55',  '-maxV', '80', '-duration', '600', '-clampBaseVoltage', '-55', '-clampDuration', '580', '-stepTargetVoltage', '10', '-erev', '50', '-caConc', '0.001', '-clampDuration', '600', '-stepTargetVoltage', '5', '-ivCurve', '../../models/Cav1.channel.nml'])

