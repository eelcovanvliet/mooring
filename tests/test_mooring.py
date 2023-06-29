
import pytest
from mooring.mooring import MooringCatenary
from mooring.mooringdesigns import CatenaryParameters
from hivemind.site import Site, SiteParameters
import OrcFxAPI

def test_mooring():
    parameters = CatenaryParameters()
    parameters.MooringHorizontaLForceAtFloater['MN'] = 25
    parameters.RadiusAnchorPointWrtColumnAxis
    cat = MooringCatenary(parameters=parameters)

    model = OrcFxAPI.Model()
    _ = model.CreateObject(OrcFxAPI.otVesselType)
    _ = model.CreateObject(OrcFxAPI.otVessel)
    model.SaveData('test_mooring.dat')

    
    anchor_point_radius = 300
    connection_points = [[0,5,0], [90,0,5], [180,-5,0], [270,0,-5]]
    anchor_points = [
        [0,anchor_point_radius,0], 
        [90,0,anchor_point_radius], 
        [180,-anchor_point_radius,0], 
        [270,0,-anchor_point_radius],
        ]
    cat.create_in_ofx(model, connection_points, anchor_points)

    model.SaveData('test_mooring.dat')

    model.CalculateStatics()
    line = model['Line1']
    GX_force = line.StaticResult('End GX force', OrcFxAPI.oeEndA) # kN
    assert GX_force == 25e3
    




