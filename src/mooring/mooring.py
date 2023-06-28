import OrcFxAPI
from abc import ABC, abstractmethod

import numpy as np
from scipy.optimize import fsolve

from .mooringdesigns import Taut, SemiTaut, InstallationDesign, Catenary
from tlp.designs import Site


class Mooring(ABC):

    def __init__(self, site:Site, installation:InstallationDesign) -> None:
        self.site = site
        self.installation = installation

    @abstractmethod
    def create_ofx(self, model:OrcFxAPI.Model, connection_points, anchor_points):
        ...


class MooringTaut(Mooring):
    InstallationDesign: Taut

    def __init__(self, site:Site) -> None: #JvS: This is not correctI think, but it needs to get Site() info for WD.
        super().__init__(site=site)

    def create_ofx(self, model:OrcFxAPI.Model, connection_points, anchor_points):
        return model

class MooringSemiTaut(Mooring):
    Installation: SemiTaut

    def __init__(self, site:Site) -> None:
        super().__init__(site=site)

    def create_ofx(self, model:OrcFxAPI.Model, connection_points, anchor_points):
        return model

class MooringCatenary(Mooring):
    

    def __init__(self, site:Site, installation:Catenary) -> None:
        super().__init__(site=site, installation=installation)

    def create_ofx(self, model:OrcFxAPI.Model, connection_points, anchor_points):
        # create line type of chain first:
        chain_type = model.CreateObject(OrcFxAPI.ObjectType.LineType, 'CatenaryChain')
        chain_type.OD, chain_type.ID = self.installation.Diameter['m'], 0
        A = np.pi/4*chain_type.OD**2
        chain_type.EA = self.installation.E['kPa']*A
        chain_type.EIx = 0.001
        chain_type.Cdx = 2.0
        chain_type.MassPerUnitLength = self.installation.MassPerUnitLength['t/m']

        water_depth = self.site.WaterDepth['m']


        
        # for obj in model.objects:
        #     if int(obj.type) == OrcFxAPI.otVessel: # FIXME: could get this statement to work..
        #         vessel = model[obj.name]
        #         draft = vessel.InitialZ
        #     else:
        #         raise TypeError("No vessel found in OrcaFlex model")

        vessel = model["Vessel1"]
        draft = vessel.InitialZ


        for (angle, x, y), (_, ax, ay) in zip(connection_points, anchor_points):
            line = model.CreateObject(OrcFxAPI.ObjectType.Line)
            line.EndAConnection = vessel.name

            line.EndAyBendingStiffness = 0.0
            line.EndAX = x
            line.EndAY = y
            line.EndAZ = 0

            line.EndBConnection = "Anchored"
            line.EndBX = ax
            line.EndBY = ay
            line.EndBHeightAboveSeabed = 0
            line.TargetSegmentLength[0] = 5.0 # target at 5 meter length

            # line.StaticsSeabedFrictionPolicy = 'None'

            begin = np.array([x,y,draft])
            end = np.array([ax,ay,-water_depth])

            diff = begin-end


            length, Fv = self.calc_length(draft=draft, hf=(ax**2+ay**2)**0.5)
            line.Length[0] = length
        return model

    def calc_length(self, draft, hf):

        def length_equation(variables):
            OD = self.installation.Diameter['m']
            A = np.pi / 4 * OD ** 2

            subm_force_ul = self.installation.MassPerUnitLength['kg/m'] - A * 1.025
            EA = self.installation.E['kPa'] * A
            Fh = self.installation.MooringHorizontaLForceAtFloater['kN']

            length, Fv = variables

            eq1 = length - Fv / subm_force_ul + Fh / EA * length + Fh / subm_force_ul * np.arcsinh(Fv / Fh) - hf
            eq2 = 1 / subm_force_ul *((Fh ** 2 + Fv ** 2) ** 0.5 - Fh + Fv ** 2 / (2* EA)) - (self.site.WaterDepth['m'] - draft)
            return [eq1, eq2]

        solution = fsolve(func = length_equation, x0= [self.site.WaterDepth['m'], self.site.WaterDepth['m']*self.installation.MassPerUnitLength['kg/m']])
        length, Fv = solution
        return length, Fv