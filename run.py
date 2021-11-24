import os
import json
from optparse import OptionParser
from src.random_generator import FreeFemRandomGenerator
from src.simulation import FreeFemSimulation


def parse_args():
    parser = OptionParser()
    parser.add_option('-e', '--experiment_folder', dest='experiment_folder')
    parser.add_option('-a', '--action', dest='action')
    parser.add_option('-n', '--network', dest='network')
    args = parser.parse_args()[0]
    return args


args = parse_args()
experiment_folder = args.experiment_folder
os.chdir(experiment_folder)
with open("data_configs.json", "rb") as fid:
    configs = json.load(fid)
random_generator = FreeFemRandomGenerator(**configs)
random_generator.generate_and_run()
# for i in range(250):
#     sim_configs_file = "data/json/case_%d.json" % i
#     with open(sim_configs_file, "r") as fid:
#         configs = json.load(fid)
#     sim = FreeFemSimulation(**configs)
#     sim.run()
