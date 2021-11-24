class FreeFemEquation:
    def __init__(self, element=None, **params):
        self.element = element
        for k, v in params.items():
            self.__setattr__(k, v)


class FreeFemLaplace(FreeFemEquation):
    def generate_fespace(self):
        str = "// Problem \n" \
              "fespace Vh(Th, %s); \n" \
              "Vh u, v;\n\n" % self.element
        return str

    def generate_equation(self):
        str = "solve a(u, v)\n" \
              " = int2d(Th)(dx(u) * dx(v) + dy(u) * dy(v)) \n"
        return str

    def generate_epd_str(self):
        fe_space = self.generate_fespace()
        equation = self.generate_equation()
        return fe_space + equation


def get_equation_class(name=None, **kwargs):
    return EQ_DICT[name](**kwargs)


EQ_DICT = {'Laplace': FreeFemLaplace}
