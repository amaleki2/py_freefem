class FreeFemGeom:
    def __init__(self, name, **params):
        self.name = name
        self.header = '// %s' % self.name
        self.template = self.get_template()
        for k, v in params.items():
            self.__setattr__(k, v)

    def generate_epd_str(self):
        fillers = self.get_template_fillers()
        epd_str = '\n'.join([self.header] + [self.template % filler for filler in fillers])
        epd_str += '\n\n'
        return epd_str

    def get_template_fillers(self):
        raise NotImplementedError

    def compute_n_meshes(self, **kwargs):
        raise NotImplementedError

    def get_template(self):
        raise NotImplementedError


class FreeFemSquare(FreeFemGeom):
    def __init__(self, name, xc=None, yc=None, lx=None, ly=None):
        super().__init__(name, xc=xc, yc=yc, lx=lx, ly=ly)

    def __repr__(self):
        return "square center at (%0.5f, %0.5f) with width %0.5f and height %0.5f" \
               % (self.xc, self.yc, self.lx, self.ly)

    def get_template(self):
        return 'border %s%d(t=-1, 1){x=%0.5f * t + %0.5f; y=%0.5f * t + %0.5f;}'

    def get_template_fillers(self):
        xc, yc = self.xc, self.yc
        lx, ly = self.lx, self.ly
        template_fillers = [(self.name, 1, lx / 2, xc, 0, yc - ly / 2),
                            (self.name, 2, 0, xc + lx / 2, ly / 2, yc),
                            (self.name, 3, -lx / 2, xc, 0, yc + ly / 2),
                            (self.name, 4, 0, xc - lx / 2, -ly / 2, yc),
                            ]
        return template_fillers

    def compute_n_meshes(self, dx=None, dy=None, clockwise=False):
        Nx, Ny = round(self.lx / dx), round(self.ly / dy)
        if clockwise:
            Nx *= -1
            Ny *= -1
        return [Nx, Ny, Nx, Ny]


class FreeFemMultiGeom:
    def __init__(self, geometries=None, meshes=None):
        self.meshes = meshes
        self.geometries = [get_geom_class(name, **params) for (name, params) in geometries.items()]

    def __repr__(self):
        return ' AND '.join([g.__repr__() for g in self.geometries])

    def generate_epd_geom_str(self):
        epd_str = ''
        epd_str = epd_str.join([geom.generate_epd_str() for geom in self.geometries])
        return epd_str

    def generate_epd_mesh_str(self):
        str = []
        for name, params in self.meshes.items():
            geom = get_geom_by_name(self.geometries, name)
            n_meshes = geom.compute_n_meshes(**params)
            if isinstance(n_meshes, int):
                str.append("%s(%d)" % (name, n_meshes))
            elif isinstance(n_meshes, list):
                str += ["%s%d(%d)" % (name, i+1, n_mesh) for (i, n_mesh) in enumerate(n_meshes)]
            else:
                raise ValueError

        epd_str = ' + '
        epd_str = epd_str.join(str)
        epd_str = "// Mesh\n" \
                  "mesh Th=buildmesh(%s);\n\n" % epd_str
        return epd_str

    def generate_epd_str(self):
        return self.generate_epd_geom_str() + self.generate_epd_mesh_str()


def get_geom_class(name, shape=None, **kwargs):
    return GEOM_DICT[shape](name, **kwargs)


def get_geom_by_name(geometries, name):
    return [x for x in geometries if x.name == name][0]


GEOM_DICT = {'square': FreeFemSquare}






