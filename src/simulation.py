import os
import platform
from .geometry import *
from .bc import *
from .equation import *


class FreeFemSimulation:
    def __init__(self,
                 name=None,
                 plot=False,
                 save_folder=None,
                 save_name=None,
                 geometry_params=None,
                 mesh_params=None,
                 bc_params=None,
                 equation_params=None):
        self.name = name
        self.plot = plot
        self.save_name = "test" if save_name is None else save_name
        self.save_folder = os.getcwd() if save_folder is None else save_folder
        self.geometry = FreeFemMultiGeom(geometries=geometry_params, meshes=mesh_params)
        self.bc = FreeFemMultiBC(bc_params)
        self.equation = get_equation_class(**equation_params)
        self.create_folders()
        self.freefem_command = self.get_freefem_command()

    @staticmethod
    def get_freefem_command():
        if platform.system().lower() == "windows":
            return "freefem++"
        elif platform.system().lower() == "linux":
            return "FreeFem++"
        else:
            raise ValueError("only works in windows or linux operating systems.")

    def get_saving_path(self):
        edp_save_name = os.path.join(self.save_folder, "edp", self.save_name + ".edp")
        mesh_save_name = os.path.join(self.save_folder, "mesh", self.save_name + ".mesh")
        mesh_save_name = mesh_save_name.replace('\\', '/')
        sol_save_name = os.path.join(self.save_folder, "solution", self.save_name + ".txt")
        sol_save_name = sol_save_name.replace('\\', '/')
        return edp_save_name, mesh_save_name, sol_save_name

    def create_folders(self):
        edp_save_name, mesh_save_name, sol_save_name = self.get_saving_path()
        epd_folder = os.path.split(edp_save_name)[0]
        mesh_folder = os.path.split(mesh_save_name)[0]
        sol_folder = os.path.split(sol_save_name)[0]
        for folder in [mesh_folder, sol_folder, epd_folder]:
            if not os.path.isdir(folder):
                os.makedirs(folder)

    def add_plot_to_epd(self):
        header_str = "\n// Plot\n"
        if self.plot:
            plot_str_mesh = 'plot(Th, wait=1, ps="Th.ps");\n'
            plot_str_sol = "plot(u, value=true, wait=1, fill=true);\n"
        else:
            plot_str_mesh = '// plot(Th, wait=1, ps="Th.ps");\n'
            plot_str_sol = "// plot(u, value=true, wait=1, fill=true);\n"
        return header_str + plot_str_mesh + plot_str_sol

    def add_save_to_epd(self):
        _, mesh_save_name, sol_save_name = self.get_saving_path()
        save_str = '\n// Save \n ' \
                   'savemesh(Th, "%s"); \n\n' \
                   'ofstream ff("%s"); \n' \
                   'for (int i=0; i < Th.nt; i++) \n' \
                   '    for (int j=0; j < 3; j++) \n' \
                   '         ff << Th[i][j].x << " " << Th[i][j].y << " " << u[][Vh(i, j)] << endl;' \
                   % (mesh_save_name, sol_save_name)
        return save_str

    def generate_epd_file(self):
        epd_str = ''
        epd_str += self.geometry.generate_epd_str()
        epd_str += self.equation.generate_epd_str()
        epd_str += self.bc.generate_epd_str()
        epd_str += self.add_plot_to_epd()
        epd_str += self.add_save_to_epd()

        edp_save_name = self.get_saving_path()[0]
        with open(edp_save_name, 'w') as fid:
            fid.write(epd_str)

    def run(self, log=None):
        self.generate_epd_file()
        edp_save_name = self.get_saving_path()[0]
        if log is None:
            run_command = '%s "%s"' % (self.freefem_command, edp_save_name)
        else:
            run_command = '%s "%s" > %s' % (self.freefem_command, edp_save_name, log)
        status = os.system(run_command)
        return status


