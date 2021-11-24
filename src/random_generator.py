import os
import json
import random
from .simulation import FreeFemSimulation


class FreeFemRandomGenerator:
    def __init__(self,
                 name=None,
                 plot=False,
                 n_simulations=1,
                 save_folder=None,
                 save_name=None,
                 geometry_params=None,
                 mesh_params=None,
                 bc_params=None,
                 equation_params=None):
        self.name = name
        self.plot = plot
        self.n_simulations = n_simulations
        self.save_name = "example" if save_name is None else save_name
        self.save_folder = os.path.join(os.getcwd(), "data") if save_folder is None else save_folder
        self.json_save_folder = os.path.join(self.save_folder, "json")
        self.geometry_params = geometry_params
        self.mesh_params = mesh_params
        self.bc_params = bc_params
        self.equation_params = equation_params
        if not os.path.isdir(self.json_save_folder):
            os.makedirs(self.json_save_folder)

    @staticmethod
    def select_randomly(x):
        if isinstance(x, list):
            if isinstance(x[0], str):
                x_selected = random.choice(x)
            elif isinstance(x[0], (int, float)):
                if len(x) == 2:
                    x_selected = random.random() * (x[1] - x[0]) + x[0]
                else:
                    x_selected = x
            elif isinstance(x[0], list):
                x_selected = [random.random() * (xi[1] - xi[0]) + xi[0] for xi in x]
            else:
                raise ValueError
        else:
            x_selected = x
        return x_selected

    def generate_random_dict(self, template_dict):
        random_dict = {}
        for key, value in template_dict.items():
            if isinstance(value, dict):
                random_dict[key] = {k: self.select_randomly(v) for k, v in value.items()}
            elif isinstance(value, list):
                random_dict[key] = self.select_randomly(value)
            else:
                random_dict[key] = value
        return random_dict

    def generate_geometry_dict(self):
        return self.generate_random_dict(self.geometry_params)

    def generate_mesh_dict(self):
        return self.generate_random_dict(self.mesh_params)

    def generate_equation_dict(self):
        return self.generate_random_dict(self.equation_params)

    def generate_bc_dict(self):
        return self.generate_random_dict(self.bc_params)

    def generate_one_config(self, i):
        geometry_dict = self.generate_geometry_dict()
        mesh_dict = self.generate_mesh_dict()
        equation_dict = self.generate_equation_dict()
        bc_dict = self.generate_bc_dict()

        save_name = self.save_name + "_" + str(i)
        config_dict = {"name": save_name,
                       "plot": self.plot,
                       "save_folder": self.save_folder,
                       "save_name": save_name,
                       "geometry_params": geometry_dict,
                       "mesh_params": mesh_dict,
                       "equation_params": equation_dict,
                       "bc_params": bc_dict
                       }

        save_json_name = os.path.join(self.json_save_folder, save_name + ".json")
        with open(save_json_name, 'w') as fid:
            json.dump(config_dict, fid, indent=4)

        return save_json_name

    def generate(self):
        for i in range(self.n_simulations):
            self.generate_one_config(i)

    def generate_and_run(self):
        itr = 0
        while itr < self.n_simulations:
            save_json_name = self.generate_one_config(itr)

            with open(save_json_name, "r") as fid:
                configs = json.load(fid)
            sim = FreeFemSimulation(**configs)
            status = sim.run()
            if status == 0:  # successful
                itr += 1