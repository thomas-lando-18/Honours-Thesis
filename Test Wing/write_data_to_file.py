# Import Packages

def write_2d_grid(fid, point_id: int, x: float, y: float, z:float):
    """
    Function that writes a Nastran GRID Card for a BDF File
    :param fid: file to be written to
    :param point_id: Grid point number
    :param x: x coord.
    :param y: y coord.
    :param z: z coord.
    """
    fid.write('GRID*' + ' '*(8-len('GRID')))
    fid.write('%s%s' % (str(int(point_id)), ' '*(16-len(str(int(point_id))))))
    fid.write(' '*16)
    fid.write('%s%s' % (str(round(float(x), 10)), ' '*(16-len(str(round(float(x), 10))))))
    fid.write('%s%s' % (str(round(float(y), 10)), ' '*(16-len(str(round(float(y), 10))))))
    fid.write('\n*' + ' '*7)
    fid.write('%s%s' % (str(round(float(z), 10)), ' '*(16-len(str(round(float(z), 10))))))
    fid.write('\n')


def write_cquad4(fid, panel_id, point_no, point_thickness):
    fid.write('CQUAD4' + ' '*3)
    fid.write('%s%s' % (str(panel_id), ' '*(8-len(str(panel_id)))))
    fid.write('1' + ' '*7)

    # Grid Numbers
    fid.write('%s%s' % (str(point_no[0]), ' ' * (8 - len(str(point_no[0])))))
    fid.write('%s%s' % (str(point_no[1]), ' ' * (8 - len(str(point_no[1])))))
    fid.write('%s%s' % (str(point_no[2]), ' ' * (8 - len(str(point_no[2])))))
    fid.write('%s%s' % (str(point_no[3]), ' ' * (8 - len(str(point_no[3])))))

    # In Between Card
    fid.write(' '*8)
    fid.write(' '*8)
    fid.write('+EL%s\n' % (str(panel_id)))

    fid.write('+EL%s%s' % (str(panel_id), ' '*(8-len(str(panel_id))-2)))
    fid.write(' '*8)
    fid.write(' '*8)

    # Grid Thicknesses
    fid.write('%s%s' % (str(point_thickness[0]), ' ' * (8 - len(str(point_thickness[0])))))
    fid.write('%s%s' % (str(point_thickness[1]), ' ' * (8 - len(str(point_thickness[1])))))
    fid.write('%s%s' % (str(point_thickness[2]), ' ' * (8 - len(str(point_thickness[2])))))
    fid.write('%s%s\n' % (str(point_thickness[3]), ' ' * (8 - len(str(point_thickness[3])))))
