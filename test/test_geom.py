from .utils import FreeFemTest
from src.geometry import *

PLOT_TEST = False


class FreeFemGeomTest(FreeFemTest):
    def test_square(self):
        geom = FreeFemSquare('test', lx=2, ly=1, xc=0., yc=0.2)
        geom_str = geom.generate_epd_str()
        mesh_str = "mesh Th=buildmesh(test1(10) + test2(20) + test3(5) + test4(40));\n"
        save_str = """savemesh(Th, "mesh.mesh");"""
        plot_str = self.add_plot_str()
        self.tmp_epd(geom_str, mesh_str, plot_str, save_str)
        self.run_epd()
        self.assertTrue(self.check_mesh_exists())
        self.assertTrue(self.check_log())
        self.delete_files()

    def test_multi(self):
        configs = self.load_config()
        geom = FreeFemMultiGeom(configs['geometry_params'], configs['mesh_params'])
        geom_str = geom.generate_epd_str()
        plot_str = self.add_plot_str()
        save_str = """savemesh(Th, "mesh.mesh");"""
        self.tmp_epd(geom_str, plot_str, save_str)
        self.run_epd()
        self.assertTrue(self.check_mesh_exists())
        self.assertTrue(self.check_log())
        self.delete_files()
