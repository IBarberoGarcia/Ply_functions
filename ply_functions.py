import numpy as np

def read_ply(ply_file):
    '''Gets an ASCII ply file and returns a dictionary with x,y,z,nx,ny,nz,red,green,blue, faces (the ones that are presented
    in the file. If some value is missed (eg. no normals) the dict will not have that value.'''
    properties=[]#List of property names
    with open(ply_file, 'r') as f:
        lines = f.readlines()
    j=0
    faces_num=0
    for line in lines:
        if line.startswith('element vertex'):
            verts_num = int(line.split(' ')[-1])
        elif line.startswith('element face'):
            faces_num = int(line.split(' ')[-1])
        elif line.startswith('property'):
            properties.append(line.split(' ')[-1].strip('\n'))
        elif line.startswith('end_header'):
            start_line=j+1
            break
        j+=1
    
    ply_dict={}    
    verts_lines = lines[start_line:start_line + verts_num]
    
    verts = np.array([list(map(float, l.strip().split(' '))) for l in verts_lines])
    if faces_num>0:
        faces_lines = lines[start_line + verts_num:]
        faces = np.array([list(map(int, l.strip().split(' '))) for l in faces_lines])[:,1:]
        ply_dict['faces'] = faces
        
    i=0
    while i<len(properties):
        attr=properties[i]
        if attr == "x":
            ply_dict['x'] = verts.transpose()[i]
        elif attr == "y":
            ply_dict['y'] = verts.transpose()[i]
        elif attr == "z":
            ply_dict['z'] = verts.transpose()[i]
        elif attr == "nx":
            ply_dict['nx'] = verts.transpose()[i]
        elif attr == "ny":
            ply_dict['ny'] = verts.transpose()[i]
        elif attr == "nz":
            ply_dict['nz'] = verts.transpose()[i]
        elif attr == "red":
            ply_dict['red'] = [int(num) for num in verts.transpose()[i]]
        elif attr == "green":
            ply_dict['green'] = [int(num) for num in verts.transpose()[i]]
        if attr == "blue":
            ply_dict['blue'] = [int(num) for num in verts.transpose()[i]]
        i+=1
    return ply_dict


def write_ply(ply_dict, out_file):
    '''Receives a dictionary with x,y,z (needed) and nx,ny,nz, red, green, blue, faces (optional) and creates an
    ASCII ply file'''
    f = open(out_file, "w")
    f.write('ply\nformat ascii 1.0\n')
    f.write('element vertex ' + str(len(ply_dict['x'])) + '\n')
    f.write('property float x\nproperty float y\nproperty float z\n')
    vertex=[]
    vertex.append(ply_dict['x'])
    vertex.append(ply_dict['y'])
    vertex.append(ply_dict['z'])
    color=False
    colors=[]#Colors are int, so they need to be separated
    if 'nx' in ply_dict:
        f.write('property float nx\nproperty float ny\nproperty float nz\n')
        vertex.append(ply_dict['nx'])
        vertex.append(ply_dict['ny'])
        vertex.append(ply_dict['nz'])
    if 'red' in ply_dict:
        color=True
        f.write('property uchar red\nproperty uchar green\nproperty uchar blue\n')
        colors.append(ply_dict['red'])
        colors.append(ply_dict['green'])
        colors.append(ply_dict['blue'])
        
    if 'faces' in ply_dict:
        f.write('element face ' + str(len(ply_dict['faces'])) + '\nproperty list uchar int vertex_indices\n')
    else:    
        f.write('element face 0\n')
    f.write('end_header')    
    
    vertex=np.array(vertex).transpose()
    colors=np.array(colors).transpose()
    i=0
    while i<len(vertex):
        point=vertex[i]
        f.write('\n')
        for value in point:
            f.write(str(value)+ ' ')
        if color:
            f.write(str(colors[i][0])+ ' ')
            f.write(str(colors[i][1])+ ' ')
            f.write(str(colors[i][2])+ ' ')
        i+=1
        
    if 'faces' in ply_dict:
        for face in ply_dict['faces']:
            f.write('\n3 ' + str(face[0]) + ' ' + str(face[1]) + ' ' + str(face[2]))
        f.write('\n')
    f.close()
    