
import pytest
from mooring.mooring import MooringCatenary
from mooring.mooringdesigns import CatenaryParameters
from hivemind.site import Site, SiteParameters
import OrcFxAPI
import math
import subprocess
from pathlib import Path
import os

TEMP = Path(__file__).parent / 'temp'
TEMP.mkdir(exist_ok=True)

def test_OC4_Deepwind():
    parameters = CatenaryParameters()
    parameters.MooringHorizontaLForceAtFloater['kN'] = 963
    # parameters.RadiusAnchorPointWrtColumnAxis
    cat = MooringCatenary(parameters=parameters)

    model = OrcFxAPI.Model()
    _ = model.CreateObject(OrcFxAPI.otVesselType)
    _ = model.CreateObject(OrcFxAPI.otVessel)
    model['Vessel1'].IncludedInStatics = "6 DOF"
    model['Vessel1'].PrimaryMotion = "Calculated (6 DOF)"
    model.environment.WaterDepth = 200
    model.SaveData(str(TEMP / 'test_oc4_deepwind.dat'))

    
    anchor_point_radius = 837.6
    fairlead_point_radius = 40.9
    loc_on_floater = -14.0
    connection_points = MooringCatenary.distribute_connection_points(x=fairlead_point_radius, y=0, z=loc_on_floater,
                                                                     angles=[0, 120, 240])

    anchor_points = MooringCatenary.distribute_connection_points(x=anchor_point_radius, y=0, z=0, angles=[0, 120, 240])

    cat.create_in_ofx(model, connection_points, anchor_points)
    model.SaveData(str(TEMP / 'test_oc4_deepwind.dat'))
    

    model.CalculateStatics()
    model.SaveData(str(TEMP / 'test_oc4_deepwind.dat'))

    line = model['Line1']
    GX_force = line.StaticResult('End GX force', OrcFxAPI.oeEndA) # kN
    assert math.isclose(GX_force, parameters.MooringHorizontaLForceAtFloater['kN'], rel_tol = 0.05)
def test_OC4_Deepwind_low():
    parameters = CatenaryParameters()
    parameters.MooringHorizontaLForceAtFloater['kN'] = 500
    # parameters.RadiusAnchorPointWrtColumnAxis
    cat = MooringCatenary(parameters=parameters)

    model = OrcFxAPI.Model()
    _ = model.CreateObject(OrcFxAPI.otVesselType)
    _ = model.CreateObject(OrcFxAPI.otVessel)
    model['Vessel1'].IncludedInStatics = "6 DOF"
    model['Vessel1'].PrimaryMotion = "Calculated (6 DOF)"
    model.environment.WaterDepth = 200
    model.SaveData(str(TEMP / 'test_oc4_deepwind_low.dat'))

    anchor_point_radius = 837.6
    fairlead_point_radius = 40.9
    loc_on_floater = -14.0
    connection_points = MooringCatenary.distribute_connection_points(x=fairlead_point_radius, y=0, z=loc_on_floater,
                                                                     angles=[0, 120, 240])

    anchor_points = MooringCatenary.distribute_connection_points(x=anchor_point_radius, y=0, z=0, angles=[0, 120, 240])

    cat.create_in_ofx(model, connection_points, anchor_points)
    model.SaveData(str(TEMP / 'test_oc4_deepwind_low.dat'))

    model.CalculateStatics()
    model.SaveData(str(TEMP / 'test_oc4_deepwind_low.dat'))

    line = model['Line1']
    GX_force = line.StaticResult('End GX force', OrcFxAPI.oeEndA)  # kN
    assert math.isclose(GX_force, parameters.MooringHorizontaLForceAtFloater['kN'], rel_tol = 0.05)
def test_OC4_Deepwind_high():
    parameters = CatenaryParameters()
    parameters.MooringHorizontaLForceAtFloater['kN'] = 1200
    # parameters.RadiusAnchorPointWrtColumnAxis
    cat = MooringCatenary(parameters=parameters)

    model = OrcFxAPI.Model()
    _ = model.CreateObject(OrcFxAPI.otVesselType)
    _ = model.CreateObject(OrcFxAPI.otVessel)
    model['Vessel1'].IncludedInStatics = "6 DOF"
    model['Vessel1'].PrimaryMotion = "Calculated (6 DOF)"
    model.environment.WaterDepth = 200
    model.SaveData(str(TEMP / 'test_oc4_deepwind_high.dat'))

    anchor_point_radius = 837.6
    fairlead_point_radius = 40.9
    loc_on_floater = -14.0
    connection_points = MooringCatenary.distribute_connection_points(x=fairlead_point_radius, y=0, z=loc_on_floater,
                                                                     angles=[0, 120, 240])

    anchor_points = MooringCatenary.distribute_connection_points(x=anchor_point_radius, y=0, z=0, angles=[0, 120, 240])

    cat.create_in_ofx(model, connection_points, anchor_points)
    model.SaveData(str(TEMP / 'test_oc4_deepwind_high.dat'))

    model.CalculateStatics()
    model.SaveData(str(TEMP / 'test_oc4_deepwind_high.dat'))

    line = model['Line1']
    GX_force = line.StaticResult('End GX force', OrcFxAPI.oeEndA)  # kN
    assert math.isclose(GX_force, parameters.MooringHorizontaLForceAtFloater['kN'], rel_tol = 0.05)


def test_OC4_Deepwind_ultradeep():
    parameters = CatenaryParameters()
    parameters.MooringHorizontaLForceAtFloater['kN'] = 963
    # parameters.RadiusAnchorPointWrtColumnAxis
    cat = MooringCatenary(parameters=parameters)

    model = OrcFxAPI.Model()
    _ = model.CreateObject(OrcFxAPI.otVesselType)
    _ = model.CreateObject(OrcFxAPI.otVessel)
    model['Vessel1'].IncludedInStatics = "6 DOF"
    model['Vessel1'].PrimaryMotion = "Calculated (6 DOF)"
    model.environment.WaterDepth = 1000
    model.SaveData(str(TEMP / 'test_oc4_deepwind_1000m.dat'))

    anchor_point_radius = 2000
    fairlead_point_radius = 40.9
    loc_on_floater = -14.0
    connection_points = MooringCatenary.distribute_connection_points(x=fairlead_point_radius, y=0, z=loc_on_floater,
                                                                     angles=[0, 120, 240])

    anchor_points = MooringCatenary.distribute_connection_points(x=anchor_point_radius, y=0, z=0, angles=[0, 120, 240])

    cat.create_in_ofx(model, connection_points, anchor_points)
    model.SaveData(str(TEMP / 'test_oc4_deepwind_1000m.dat'))

    model.CalculateStatics()
    model.SaveData(str(TEMP / 'test_oc4_deepwind_1000m.dat'))

    line = model['Line1']
    GX_force = line.StaticResult('End GX force', OrcFxAPI.oeEndA)  # kN
    assert math.isclose(GX_force, parameters.MooringHorizontaLForceAtFloater['kN'], rel_tol=0.05)

def test_OC4_Deepwind_ultradeep_increasedradius():
    parameters = CatenaryParameters()
    parameters.MooringHorizontaLForceAtFloater['kN'] = 963
    # parameters.RadiusAnchorPointWrtColumnAxis
    cat = MooringCatenary(parameters=parameters)

    model = OrcFxAPI.Model()
    _ = model.CreateObject(OrcFxAPI.otVesselType)
    _ = model.CreateObject(OrcFxAPI.otVessel)
    model['Vessel1'].IncludedInStatics = "6 DOF"
    model['Vessel1'].PrimaryMotion = "Calculated (6 DOF)"
    model.environment.WaterDepth = 1000
    model.SaveData(str(TEMP / 'test_oc4_deepwind_1000m_increasedradius.dat'))

    anchor_point_radius = 4000
    fairlead_point_radius = 40.9
    loc_on_floater = -14.0
    connection_points = MooringCatenary.distribute_connection_points(x=fairlead_point_radius, y=0, z=loc_on_floater,
                                                                     angles=[0, 120, 240])

    anchor_points = MooringCatenary.distribute_connection_points(x=anchor_point_radius, y=0, z=0, angles=[0, 120, 240])

    cat.create_in_ofx(model, connection_points, anchor_points)
    model.SaveData(str(TEMP / 'test_oc4_deepwind_1000m_increasedradius.dat'))

    model.CalculateStatics()
    model.SaveData(str(TEMP / 'test_oc4_deepwind_1000m_increasedradius.dat'))

    line = model['Line1']
    GX_force = line.StaticResult('End GX force', OrcFxAPI.oeEndA)  # kN
    assert math.isclose(GX_force, parameters.MooringHorizontaLForceAtFloater['kN'], rel_tol=0.05)
def test_VolturnUS_S_200m():
    parameters = CatenaryParameters()
    parameters.MooringHorizontaLForceAtFloater['kN'] = 1340.0
    parameters.MassPerUnitLength['kg/m'] = 685
    parameters.Diameter['m'] = 0.33332
    parameters.EA['kN'] = 3.27e6
    # parameters.RadiusAnchorPointWrtColumnAxis
    cat = MooringCatenary(parameters=parameters)

    model = OrcFxAPI.Model()
    _ = model.CreateObject(OrcFxAPI.otVesselType)
    _ = model.CreateObject(OrcFxAPI.otVessel)
    model['Vessel1'].IncludedInStatics = "6 DOF"
    model['Vessel1'].PrimaryMotion = "Calculated (6 DOF)"
    model.environment.WaterDepth = 200.0
    model.SaveData(str(TEMP / 'test_volturnuss_200m.dat'))

    anchor_point_radius = 837.7
    fairlead_point_radius = 58
    loc_on_floater = -14.0
    connection_points = MooringCatenary.distribute_connection_points(x = fairlead_point_radius, y = 0, z=loc_on_floater, angles=[0,120,240])
    # connection_points = [
    #                     [0, fairlead_point_radius, 0],
    #                      [90, 0, fairlead_point_radius],
    #                      [180, -fairlead_point_radius, 0],
    #                      [270, 0, -fairlead_point_radius]
    #                     ]

    anchor_points = MooringCatenary.distribute_connection_points(x = anchor_point_radius,y=0,z=0, angles=[0,120,240])
    # anchor_points = [
    #     [0, anchor_point_radius, 0],
    #     [90, 0, anchor_point_radius],
    #     [180, -anchor_point_radius, 0],
    #     [270, 0, -anchor_point_radius],
    # ]

    cat.create_in_ofx(model, connection_points, anchor_points)
    model.SaveData(str(TEMP / 'test_volturnuss_200m.dat'))

    model.CalculateStatics()
    model.SaveData(str(TEMP / 'test_volturnuss_200m.dat'))

    line = model['Line1']
    GX_force = line.StaticResult('End GX force', OrcFxAPI.oeEndA)  # kN
    print('GX_force = ', GX_force)
    assert math.isclose(GX_force, parameters.MooringHorizontaLForceAtFloater['kN'], rel_tol = 0.05)

def test_VolturnUS_S_500m():
    parameters = CatenaryParameters()
    parameters.MooringHorizontaLForceAtFloater['kN'] = 1340.0
    parameters.MassPerUnitLength['t/m'] = 0.685
    parameters.Diameter['m'] = 0.33332
    parameters.EA['kN'] = 3.27e6
    # parameters.RadiusAnchorPointWrtColumnAxis
    cat = MooringCatenary(parameters=parameters)

    model = OrcFxAPI.Model()
    _ = model.CreateObject(OrcFxAPI.otVesselType)
    _ = model.CreateObject(OrcFxAPI.otVessel)
    model['Vessel1'].IncludedInStatics = "6 DOF"
    model['Vessel1'].PrimaryMotion = "Calculated (6 DOF)"
    model.environment.WaterDepth = 500.0
    model.SaveData(str(TEMP / 'test_volturnuss_500m.dat'))

    anchor_point_radius = 1500.0
    fairlead_point_radius = 58
    loc_on_floater = -14.0
    connection_points = MooringCatenary.distribute_connection_points(x = fairlead_point_radius, y = 0, z=loc_on_floater, angles=[0,120,240])

    anchor_points = MooringCatenary.distribute_connection_points(x = anchor_point_radius,y=0,z=0, angles=[0,120,240])


    cat.create_in_ofx(model, connection_points, anchor_points)
    model.SaveData(str(TEMP / 'test_volturnuss_500m.dat'))

    model.CalculateStatics()
    model.SaveData(str(TEMP / 'test_volturnuss_500m.dat'))

    line = model['Line1']
    GX_force = line.StaticResult('End GX force', OrcFxAPI.oeEndA)  # kN
    print('GX_force = ', GX_force)
    assert math.isclose(GX_force, parameters.MooringHorizontaLForceAtFloater['kN'], rel_tol = 0.05)


def test_VolturnUS_S_500m_higherpretension():
    parameters = CatenaryParameters()
    parameters.MooringHorizontaLForceAtFloater['kN'] = 20000
    parameters.MassPerUnitLength['t/m'] = 0.685
    parameters.Diameter['m'] = 0.33332
    parameters.EA['kN'] = 3.27e6
    # parameters.RadiusAnchorPointWrtColumnAxis
    cat = MooringCatenary(parameters=parameters)

    model = OrcFxAPI.Model()
    _ = model.CreateObject(OrcFxAPI.otVesselType)
    _ = model.CreateObject(OrcFxAPI.otVessel)
    model['Vessel1'].IncludedInStatics = "6 DOF"
    model['Vessel1'].PrimaryMotion = "Calculated (6 DOF)"
    model.environment.WaterDepth = 500.0
    model.SaveData(str(TEMP / 'test_volturnuss_500m_incr_Fh.dat'))

    anchor_point_radius = 2500.0
    fairlead_point_radius = 58
    loc_on_floater = -14.0
    connection_points = MooringCatenary.distribute_connection_points(x=fairlead_point_radius, y=0, z=loc_on_floater,
                                                                     angles=[0, 120, 240])

    anchor_points = MooringCatenary.distribute_connection_points(x=anchor_point_radius, y=0, z=0, angles=[0, 120, 240])

    cat.create_in_ofx(model, connection_points, anchor_points)
    model.SaveData(str(TEMP / 'test_volturnuss_500m_incr_Fh.dat'))

    model.CalculateStatics()
    model.SaveData(str(TEMP / 'test_volturnuss_500m_incr_Fh.dat'))

    line = model['Line1']
    GX_force = line.StaticResult('End GX force', OrcFxAPI.oeEndA)  # kN
    print('GX_force = ', GX_force)
    assert math.isclose(GX_force, parameters.MooringHorizontaLForceAtFloater['kN'], rel_tol=0.05)

if __name__ == '__main__':
    pytest.main(['-v'])