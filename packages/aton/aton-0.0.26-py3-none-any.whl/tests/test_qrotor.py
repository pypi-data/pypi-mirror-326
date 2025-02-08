import aton.qrotor as qr
import aton.interface as interface
import aton.txt.extract as extract
import aton.st.file as file


folder = 'tests/samples/'
structure = folder + 'CH3NH3.in'
structure_120 = folder + 'CH3NH3_120.in'
structure_60 = folder + 'CH3NH3_60.in'


def test_rotate():
    CH3 = [
        '0.100   0.183   0.316',
        '0.151   0.532   0.842',
        '0.118   0.816   0.277',
    ]
    # 120 degrees (it should remain the same)
    qr.rotate.structure_qe(filepath=structure, positions=CH3, angle=120, precision=2)
    for coord in CH3:
        rotated_coord = interface.qe.get_atom(filepath=structure_120, position=coord, precision=2)
        rotated_coord = extract.coords(rotated_coord)
        coord = extract.coords(coord)
        rotated_coord_rounded = []
        coord_rounded = []
        for i in rotated_coord:
            rotated_coord_rounded.append(round(i, 2))
        for i in coord:
            coord_rounded.append(round(i, 2))
        assert coord_rounded == rotated_coord_rounded
    file.remove(structure_120)

    # 60 degrees (it should change quite a lot)
    ideal = [
        '0.146468644022416   0.837865866372631   0.641449758215011',
        '0.095062781582172   0.488975944606740   0.115053787468686',
        '0.128156574395412   0.205890189020629   0.680672454316303',
    ]
    qr.rotate.structure_qe(filepath=structure, positions=CH3, angle=60, precision=2)
    for coord in ideal:
        rotated_coord = interface.qe.get_atom(filepath=structure_60, position=coord, precision=3)
        rotated_coord = extract.coords(rotated_coord)
        coord = extract.coords(coord)
        rotated_coord_rounded = []
        coord_rounded = []
        for i in rotated_coord:
            rotated_coord_rounded.append(round(i, 2))
        for i in coord:
            coord_rounded.append(round(i, 2))
        assert coord_rounded == rotated_coord_rounded
    file.remove(structure_60)


def test_solve_zero():
    system = qr.System()
    system.gridsize = 50000
    system.potential_name = 'zero'
    system.B = 1
    system.solve()
    assert round(system.eigenvalues[0], 2) == 0.0
    assert round(system.eigenvalues[1], 2) == 1.0
    assert round(system.eigenvalues[2], 2) == 1.0
    assert round(system.eigenvalues[3], 2) == 4.0
    assert round(system.eigenvalues[4], 2) == 4.0
    assert round(system.eigenvalues[5], 2) == 9.0
    assert round(system.eigenvalues[6], 2) == 9.0
    assert round(system.eigenvalues[7], 2) == 16.0
    assert round(system.eigenvalues[8], 2) == 16.0

