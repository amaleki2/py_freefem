from .utils import FreeFemTest
from src.simulation import FreeFemSimulation

PLOT_TEST = False


class FreeFemSimulationTest(FreeFemTest):
    def test_freefem_simulation(self):
        configs = self.load_config()
        sim = FreeFemSimulation(**configs)
        sim.run(log="tmp.log")
        self.assertTrue(self.check_log())
        self.assertTrue(self.check_mesh_exists(sim.get_saving_path()[1]))
        self.assertTrue(self.check_sol_exists(sim.get_saving_path()[2]))
        self.delete_files()

