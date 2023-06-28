
import numpy as np
from carg_io.abstracts import ParameterSet, Parameter, ureg

# ureg = UnitRegistry()
# m = ureg.meter
# mm = ureg.millimeter
# tonne = ureg.tonne
# deg = ureg.degree
# kN = ureg.kilonewton
# s = ureg.second
# Hz = ureg.hertz
# ureg.define(' ')
# dimensionless = ureg.dimensionless


class Taut(ParameterSet):
    NumberOfLines:Parameter = 3*ureg.dimensionless
    Diameter:Parameter = 254 * ureg.mm
    MassPerUnitLength:Parameter = 45 * ureg.kg / ureg.m
    E:Parameter = 57133000 * ureg.kPa # Youngs Modulus Dyneema = 57133000 kN according to FibreMax website
    RadiusAnchorPointWrtColumnAxis:Parameter = 430 * ureg.m
    PreTension:Parameter = 250 * ureg.MPa

class SemiTaut(ParameterSet):
    NumberOfLines:Parameter = 3*ureg.dimensionless
    RadiusAnchorPointWrtColumnAxis:Parameter = 790 * ureg.m
    MassPerUnitLength:Parameter = np.array([128, 473]) * ureg.kg / ureg.m
    E:Parameter = np.array([210, 210]) * ureg.GPa # Youngs Modulus Steel
    Diameter:Parameter = np.array([165, 147]) * ureg.mm

class CatenaryParameters(ParameterSet):
    NumberOfLines: Parameter = 3 * ureg.dimensionless
    RadiusAnchorPointWrtColumnAxis:Parameter = 790 * ureg.m
    MassPerUnitLength:Parameter = 473 * ureg.kg / ureg.m
    E:Parameter = 210 * ureg.GPa # Youngs Modulus Steel
    Diameter:Parameter = 165 * ureg.mm
    MooringHorizontaLForceAtFloater:Parameter = 2000 * ureg.kN