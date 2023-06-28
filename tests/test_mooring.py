
import pytest
from mooring.mooring import MooringCatenary
from mooring.mooringdesigns import Catenary
from tlp.designs import Site
import OrcFxAPI

def test_mooring():
    site = Site()
    installation = Catenary()
    installation.MooringHorizontaLForceAtFloater['MN'] = 10
    cat = MooringCatenary(site=site, installation=installation)

    model = OrcFxAPI.Model()
    _ = model.CreateObject(OrcFxAPI.otVesselType)
    _ = model.CreateObject(OrcFxAPI.otVessel)
    model.SaveData('test_mooring.dat')

    
    connection_points = [[0,5,0], [90,0,5], [180,-5,0], [270,0,-5]]
    anchor_points = [[0,100,0], [90,0,100], [180,-100,0], [270,0,-100]]
    cat.create_ofx(model, connection_points, anchor_points)

    model.SaveData('test_mooring.dat')
    




