import numpy as np

def read_ply(ply_file):
    '''Gets an ASCII ply file and returns a dictionary with x,y,z,nx,ny,nz,red,green,blue, faces (the ones that are presented
    in the file. If some value is missed (eg no normals) the function will work and the dict will not have that value.'''
    properties=[]#List of property names
    with open(ply_file, 'r') as f:
        lines = f.readlines()
    j=0
    faces_num=0
    for line in lines:
        if line.startswith('element vertex'):
            verts_num = int(line.split(' ')[-1])
        if line.startswith('element face'):
            faces_num = int(line.split(' ')[-1])
        if line.startswith('property'):
            properties.append(line.split(' ')[-1].strip('\n'))
        if line.startswith('end_header'):
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
        if attr == "y":
            ply_dict['y'] = verts.transpose()[i]
        if attr == "z":
            ply_dict['z'] = verts.transpose()[i]
        if attr == "nx":
            ply_dict['nx'] = verts.transpose()[i]
        if attr == "ny":
            ply_dict['ny'] = verts.transpose()[i]
        if attr == "nz":
            ply_dict['nz'] = verts.transpose()[i]
        if attr == "red":
            ply_dict['red'] = [int(num) for num in verts.transpose()[i]]
        if attr == "green":
            ply_dict['green'] = [int(num) for num in verts.transpose()[i]]
        if attr == "blue":
            ply_dict['blue'] = [int(num) for num in verts.transpose()[i]]
        i+=1
    return ply_dict