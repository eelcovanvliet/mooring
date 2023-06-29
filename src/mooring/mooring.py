from __future__ import annotations
import OrcFxAPI
from abc import ABC, abstractmethod
import numpy as np
from scipy.optimize import fsolve
from .mooringdesigns import CatenaryParameters
from hivemind.abstracts import Base, State
from hivemind.site import Site
from typing import List, Dict, Tuple
from pathlib import Path

# class Mooring(ABC):

#     def __init__(self, site:Site, installation:InstallationDesign) -> None:
#         self.site = site
#         self.installation = installation

#     @abstractmethod
#     def create_ofx(self, model:OrcFxAPI.Model, connection_points, anchor_points):
#         ...


# class MooringTaut(Mooring):
#     InstallationDesign: Taut

#     def __init__(self, site:Site) -> None: #JvS: This is not correctI think, but it needs to get Site() info for WD.
#         super().__init__(site=site)

#     def create_ofx(self, model:OrcFxAPI.Model, connection_points, anchor_points):
#         return model

# class MooringSemiTaut(Mooring):
#     Installation: SemiTaut

#     def __init__(self, site:Site) -> None:
#         super().__init__(site=site)

#     def create_ofx(self, model:OrcFxAPI.Model, connection_points, anchor_points):
#         return model

class MooringCatenary(Base):
    

    def __init__(self, parameters:CatenaryParameters):
        self._parameters = parameters
        self._possible_states = {
            "InSitu" : CatenaryInSitu(self),
        }
        self._state = self._possible_states["InSitu"]
        self._previous_state = None

    @property   
    def state(self) -> CatenaryState:
        return self._state
    
    @property
    def parameters(self) -> CatenaryParameters:
        return self._parameters

    @property
    def possible_states(self) -> Dict[str, CatenaryState]:
        return self._possible_states
    
    def change_state(self, state:str) -> bool:
        self._previous_state = self._state
        self._state = self.possible_states[state]
        return True

    @property
    def state(self) -> CatenaryState:
        return self._state

    @property
    def previous_state(self) -> CatenaryState|None:
        raise NotImplementedError()

    def create_in_ofx(self, model, *args, **kwrags):
        self.state.create_in_ofx(model, *args, **kwrags)


class CatenaryState(State):
    pass

class CatenaryInSitu(CatenaryState):

    def create_in_ofx(self, model:OrcFxAPI.Model, connection_points, anchor_points) -> OrcFxAPI.Model:
        # create line type of chain first:
        chain_type = model.CreateObject(OrcFxAPI.ObjectType.LineType, 'CatenaryChain')
        chain_type.OD, chain_type.ID = self.base.parameters.Diameter['m'], 0
        
        A = np.pi/4*chain_type.OD**2
        chain_type.EA = self.base.parameters.E['kPa']*A
        chain_type.EIx = 0.001
        chain_type.Cdx = 2.0
        chain_type.MassPerUnitLength = self.base.parameters.MassPerUnitLength['t/m']

        # water_depth = self.site.water_depth['m']
        water_depth = model.environment.WaterDepth



        
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


            length, Fv = self.calc_length(draft=draft, hf=(ax**2+ay**2)**0.5, water_depth=water_depth)
            line.Length[0] = length
        return model

    def calc_length(self, draft, hf, water_depth):

        def length_equation(variables):
            OD = self.base.parameters.Diameter['m']
            A = np.pi / 4 * OD ** 2

            subm_force_ul = self.base.parameters.MassPerUnitLength['kg/m'] - A * 1.025
            EA = self.base.parameters.E['kPa'] * A
            Fh = self.base.parameters.MooringHorizontaLForceAtFloater['kN']

            length, Fv = variables

            eq1 = length - Fv / subm_force_ul + Fh / EA * length + Fh / subm_force_ul * np.arcsinh(Fv / Fh) - hf
            eq2 = 1 / subm_force_ul *((Fh ** 2 + Fv ** 2) ** 0.5 - Fh + Fv ** 2 / (2* EA)) - (water_depth - draft)
            return [eq1, eq2]

        solution = fsolve(func = length_equation, x0= [water_depth, water_depth*self.base.parameters.MassPerUnitLength['kg/m']])
        length, Fv = solution
        return length, Fv