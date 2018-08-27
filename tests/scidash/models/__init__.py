import os
from neuronunit.models.channel import ChannelModel

path = os.path.realpath(__file__)
for i in range(4):
    path = os.path.split(path)[0]
CW_HOME = path

def make_model(channel_model_name):
    channel_file_path = os.path.join(CW_HOME,
                                     'models','%s.nml' % channel_model_name)
    model = ChannelModel(channel_file_path,channel_index=0,
                         name=channel_model_name.split('.')[0])
    return model

# Instantiate the models
egl19_model = make_model('EGL-19.channel')
slo2_channel = make_model('SLO-2.channel')

models = [egl19_model,slo2_channel]
