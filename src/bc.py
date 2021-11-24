class FreeFemBC:
    def __init__(self, name, values=None):
        self.name = name
        self.values = values


class FreeFemDirichletBC(FreeFemBC):
    def generate_epd_str(self):
        if isinstance(self.values, (int, float)):
            epd_str = "on(%s, u=%0.5f)\n" % (self.name, self.values)
        elif isinstance(self.values, list):
            epd_str = ' + '.join(["on(%s%d, u=%0.5f)\n" % (self.name, i+1, v) for (i, v) in enumerate(self.values)])
        else:
            raise ValueError

        return epd_str


class FreeFemMultiBC:
    def __init__(self, bc_params):
        self.bcs = [get_bc_class(name, **params) for (name, params) in bc_params.items()]

    def generate_epd_str(self):
        epd_str = ' + '.join([bc.generate_epd_str() for bc in self.bcs])
        epd_str = epd_str[:-1]  # remove \n
        epd_str = ' + ' + epd_str + ';\n'
        return epd_str

def get_bc_class(name, kind=None, values=None):
    return BC_DICT[kind](name, values=values)


BC_DICT = {"Dirichlet": FreeFemDirichletBC}