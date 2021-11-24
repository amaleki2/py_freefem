import os
import json
import shutil
from .utils import FreeFemTest
from src.random_generator import FreeFemRandomGenerator
from src.simulation import FreeFemSimulation


class FreeFemRandomGeneratorTest(FreeFemTest):
    def test_freefem_random_generator1(self):
        configs = self.load_config()
        random_generator = FreeFemRandomGenerator(**configs)
        random_generator.generate()
        self.assertTrue(os.path.isfile("data/json/test_0.json"))
        shutil.rmtree("data")

    def test_freefem_random_generator2(self):
        configs = self.load_config()
        configs['n_simulations'] = 3
        random_generator = FreeFemRandomGenerator(**configs)
        random_generator.generate()
        self.assertTrue(os.path.isfile("data/json/test_2.json"))
        shutil.rmtree("data")

    def test_freefem_random_generator3(self):
        configs = self.load_config()
        configs['n_simulations'] = 3
        configs["geometry_params"]["boundary"]["lx"] = [1, 2]
        configs["equation_params"]["name"] = ["Laplace", "Poisson"]
        configs["bc_params"]["boundary"]["kind"] = ["Dirichlet", "Neumann"]
        random_generator = FreeFemRandomGenerator(**configs)
        random_generator.generate()
        self.assertTrue(os.path.isfile("data/json/test_2.json"))
        shutil.rmtree("data")

    def test_freefem_random_generator4(self):
        configs = self.load_config()
        configs['n_simulations'] = 10
        configs["geometry_params"]["hole"]["lx"] = [0.25, 0.8]
        configs["geometry_params"]["hole"]["ly"] = [0.1, 0.3]
        configs["geometry_params"]["hole"]["xc"] = [-0.5, 0.5]
        configs["geometry_params"]["hole"]["yc"] = [-0.8, 0.8]
        random_generator = FreeFemRandomGenerator(**configs)
        random_generator.generate()
        for i in range(10):
            sim_configs_file = "data/json/test_%d.json" % i
            with open(sim_configs_file, "r") as fid:
                configs = json.load(fid)
            sim = FreeFemSimulation(**configs)
            sim.run()

        for i in range(10):
            self.check_mesh_exists(os.path.isfile("data/mesh/test_%d.mesh" % i))
            self.check_sol_exists(os.path.isfile("data/solution/test_%d.txt" % i))
        shutil.rmtree("data")

    def test_freefem_random_generator5(self):
        configs = self.load_config()
        configs['n_simulations'] = 250
        configs["geometry_params"]["hole"]["lx"] = [0.4, 1.4]
        configs["geometry_params"]["hole"]["ly"] = [0.4, 1.4]
        configs["geometry_params"]["hole"]["xc"] = [-0.75, 0.75]
        configs["geometry_params"]["hole"]["yc"] = [-0.75, 0.75]
        random_generator = FreeFemRandomGenerator(**configs)
        random_generator.generate_and_run()
        for i in range(10):
            self.check_mesh_exists(os.path.isfile("data/mesh/test_%d.mesh" % i))
            self.check_sol_exists(os.path.isfile("data/solution/test_%d.txt" % i))
        shutil.rmtree("data")
