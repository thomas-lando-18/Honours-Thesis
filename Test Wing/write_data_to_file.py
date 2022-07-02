# Import Packages

def write_2d_grid(fid, point_id, x, y, z):
    fid.write('GRID*' + ' '*(8-len('GRID')))
    fid.write('%s%s' % (str(int(point_id)), ' '*(8-len(str(int(point_id))))))
    fid.write(' '*16)
    fid.write('%s%s' % (str(round(float(x), 10)), ' '*(16-len(str(round(float(x), 10))))))
    fid.write('%s%s' % (str(round(float(y), 10)), ' '*(16-len(str(round(float(y), 10))))))
    fid.write('\n*' + ' '*7)
    fid.write('%s%s' % (str(round(float(z), 10)), ' '*(16-len(str(round(float(z), 10))))))
    fid.write('\n')
