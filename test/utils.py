import os
import json
import shutil
import unittest


def safe_remove_file(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        pass


class FreeFemTest(unittest.TestCase):
    plot = False
    os.chdir(os.path.split(__file__)[0])

    @staticmethod
    def load_config():
        with open('config.json', "rb") as fid:
            configs = json.load(fid)
        return configs

    @staticmethod
    def tmp_epd(*str):
        with open("tmp.edp", "w") as fid:
            for s in str:
                fid.write(s + '\n')

    @staticmethod
    def run_epd():
        os.system("freefem++ tmp.edp > tmp.log")

    @staticmethod
    def check_log():
        with open("tmp.log", "r") as fid:
            s = fid.read()
        return "Ok: Normal End" in s

    @staticmethod
    def check_mesh_exists(file=None):
        if file is None:
            return os.path.isfile("mesh.mesh") and os.path.isfile("mesh.mesh.gmsh")
        else:
            return os.path.isfile(file)

    @staticmethod
    def check_sol_exists(file=None):
        if file is None:
            return os.path.isfile("sol.txt")
        else:
            return os.path.isfile(file)

    @staticmethod
    def delete_files():
        safe_remove_file("Th.ps")
        safe_remove_file("mesh.mesh")
        safe_remove_file("mesh.mesh.gmsh")
        safe_remove_file("tmp.edp")
        safe_remove_file("tmp.log")
        safe_remove_file("Th.ps")
        shutil.rmtree("mesh", ignore_errors=True)
        shutil.rmtree("edp", ignore_errors=True)
        shutil.rmtree("solution", ignore_errors=True)

    def add_plot_str(self):
        return "plot(Th, wait=1);" if self.plot else ""
