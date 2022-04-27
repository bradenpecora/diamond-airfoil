import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class Vertex:
    def __init__(self, x,y,z, global_i=None):
        self.x = x
        self.y = y
        self.z = z
        self.global_i = global_i
        self.theta = self.get_theta()
        self.r = np.sqrt(x**2 + y**2)
    def get_theta(self):
        return np.arctan2(self.y, self.x)
    def __str__(self):
        return '    ( {} {} {}) // {}'.format(self.x,self.y,self.z,self.global_i)
    def flip_z(self):
        return Vertex(self.x, self.y, -1*self.z, self.global_i + 16)
    def plot(self, vert2):
        plt.plot([self.x, vert2.x], [self.y, vert2.y], 'o-k')
    def rotate(self, alpha):
        alpha = np.deg2rad(alpha)
        rot = np.array([[np.cos(alpha),-1*np.sin(alpha)],[np.sin(alpha), np.cos(alpha)]])
        v = np.array([self.x, self.y])

        self.x, self.y = np.dot(rot, v)
        self.theta = self.get_theta() # update theta

class Face:
    def __init__(self, v0, v1, v2, v3):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    def local_node(self, i):
        if i == 0 or i == 4:
            return self.v0
        elif i == 1 or i == 5:
            return self.v1
        elif i == 2 or i == 6:
            return self.v2
        elif i == 3 or i == 7:
            return self.v3
    def generate_back_face(self):
        v4 = self.v0.flip_z()
        v5 = self.v1.flip_z()
        v6 = self.v2.flip_z()
        v7 = self.v3.flip_z()
        return Face(v4, v5, v6, v7)
    def nodes(self):
        return [self.v0, self.v1, self.v2, self.v3]
    def plot(self):
        nodes = self.nodes()
        [nodes[i].plot(nodes[i+1]) for i in range(len(nodes)-1)]
        nodes[-1].plot(nodes[0])
    def rotate(self,alpha):
        for node in self.nodes:
            node.rotate(alpha)

class Block:
    def __init__(self, front_face, i, nx1=1, nx2=1, nx3=1, ex1=1, ex2=1, ex3=1):
        self.front = front_face
        self.back = self.front.generate_back_face()
        self.index = i
        self.nx1 = int(nx1)
        self.nx2 = int(nx2)
        self.nx3 = int(nx3)
        self.ex1 = ex1
        self.ex2 = ex2
        self.ex3 = ex3
    def local_node(self,i):
        if i <= 3:
            return self.front.local_node(i)
        elif i >= 4:
            return self.back.local_node(i)
    def __str__(self):
        global_nodes = [int(self.local_node(i).global_i) for i in range(8)]
        global_nodes_str = ' '.join(str(n) for n in global_nodes)
        return '    // block {}\n   hex ({}) ({} {} {}) simpleGrading ( {} {} {})'.format(self.index, global_nodes_str, self.nx1, self.nx2, self.nx3, self.ex1, self.ex2, self.ex3)
    def rotate(self,alpha):
        self.front.rotate(alpha)
        self.back.rotate(alpha)

class Index:
    def __init__(self):
        self.current = 0
    def i(self):
        index = self.current
        self.current += 1
        return index

def generate_faces(n):
    faces = []
    append = lambda v0, v1, v2, v3: faces.append(Face(n[v0],n[v1],n[v2],n[v3]))

    append(0,4,5,6)
    append(0,6,7,1)
    append(1,7,8,2)
    append(2,8,9,10)
    append(2,10,11,12)
    append(2,12,13,3)
    append(3,13,14,0)
    append(0,14,15,4)

    return faces

def main(c,t,lf,lw,ht,hb,alpha, n_foil, n_north, n_east, n_south, n_west, e_foil, e_north, e_east, e_south, e_west, user_name=None):
    dz = 0.05
    if dz > 0:
        dz = -1*dz
    if lf > 0:
        lf = -1*lf
    if hb > 0:
        hb = -1*hb

    # generate front nodes
    nodes_index = Index()
    nodes = []
    create_node = lambda x,y,: nodes.append(Vertex(x,y,dz,nodes_index.i()))

    # generate airfoil and rotate by alpha
    create_node(c, 0)#0
    create_node(0,t)#1
    create_node(-c,0)#2
    create_node(0,-t)#3
    for node in nodes:
        node.rotate(alpha)

    # generate outer nodes
    create_node(lw, nodes[0].y) #4
    create_node(lw, ht) #5
    create_node(nodes[0].x, ht) #6
    create_node(nodes[1].x, ht) #7
    create_node(nodes[2].x, ht) #8
    create_node(lf, ht) #9
    create_node(lf, nodes[2].y) #10
    create_node(lf,hb) #11
    create_node(nodes[2].x, hb) #12
    create_node(nodes[3].x, hb) #13
    create_node(nodes[0].x, hb) #14
    create_node(lw,hb) #15

    nodes += [node.flip_z() for node in nodes]

    faces=generate_faces(nodes)
    [face.plot() for face in faces]
    plt.savefig('test.png')

    block_index = Index()
    blocks = [Block(face, block_index.i()) for face in faces]
    
    blocks[0].nx1 = n_east
    blocks[0].ex1 = e_east
    blocks[0].nx2 = n_north
    blocks[0].ex2 = e_north

    blocks[1].nx1 = n_north
    blocks[1].ex1 = e_north
    blocks[1].nx2 = n_foil
    blocks[1].ex2 = e_foil

    blocks[2].nx1 = n_north
    blocks[2].ex1 = e_north
    blocks[2].nx2 = n_foil
    blocks[2].ex2 = e_foil

    blocks[3].nx1 = n_north
    blocks[3].ex1 = e_north
    blocks[3].nx2 = n_west
    blocks[3].ex2 = e_west

    blocks[4].nx1 = n_west
    blocks[4].ex1 = e_west
    blocks[4].nx2 = n_south
    blocks[4].ex2 = e_south

    blocks[5].nx1 = n_south
    blocks[5].ex1 = e_south
    blocks[5].nx2 = n_foil
    blocks[5].ex2 = e_foil

    blocks[6].nx1 = n_south
    blocks[6].ex1 = e_south
    blocks[6].nx2 = n_foil
    blocks[6].ex2 = e_foil

    blocks[7].nx1 = n_south
    blocks[7].ex1 = e_south
    blocks[7].nx2 = n_east
    blocks[7].ex2 = e_east

    # Create output
    output = ['\n']
    a = lambda newline: output.append(newline + '\n') # short hand
    a('// User: {}'.format(user_name))
    a('// Mesh generated on {}'.format(datetime.now().strftime("%m/%d/%Y %H:%M:%S")))
    a('')
    a('// c = {}'.format(c))
    a('// t = {}'.format(t))
    a('// lf = {}'.format(lf))
    a('// lw = {}'.format(lw))
    a('// ht = {}'.format(ht))
    a('// hb = {}'.format(hb))
    a('// alpha = {}'.format(alpha))
    a('// n_foil = {}'.format(n_foil))
    a('// n_north = {}'.format(n_north))
    a('// n_east = {}'.format(n_east))
    a('// n_south = {}'.format(n_south))
    a('// n_west = {}'.format(n_west))
    a('// e_foil = {}'.format(e_foil))
    a('// e_north = {}'.format(e_north))
    a('// e_east = {}'.format(e_east))
    a('// e_south = {}'.format(e_south))
    a('// e_west = {}'.format(e_west))
    a('')
    a('FoamFile')
    a('{')
    a(' version 2.0;')
    a(' format  ascii;')
    a(' class   dictionary;')
    a(' object  blockMeshDict;')
    a('}')
    a('')
    a('convertToMeters  1.0;')
    a('')
    a('vertices')
    a('(')
    [a(str(v)) for v in nodes]
    a(');')
    a('')
    a('blocks')
    a('(')
    [a(str(b)) for b in blocks]
    a(');')
    a('')
    a('')
    # a('edges')
    # a('(')
    # a('')
    # [a(str(arc)) for arc in arcs]
    # a('')
    # a(');')
    a('')
    a('boundary')
    a('(')
    a(' inlet')
    a(' {')
    a('     type patch;')
    a('     faces')
    a('     (')
    a('         (9 25 26 10)')
    a('         (10 26 27 11)')
    a('     );')
    a(' }')
    a(' outlet')
    a(' {')
    a('     type patch;')
    a('     faces')
    a('     (')
    a('         (15 31 20 4)')
    a('         (4 20 21 5)')
    a('     );')
    a(' }')
    a(' airfoil')
    a(' {')
    a('     type wall;')
    a('     faces')
    a('     (')
    a('         (0 16 17 1)')
    a('         (1 17 18 2)')
    a('         (2 18 19 3)')
    a('         (3 19 16 0)')
    a('     );')
    a(' }')
    a(' top')
    a(' {')
    a('     type symmetryPlane;')
    a('     faces')
    a('     (')
    a('         (5 22 21 6)')
    a('         (6 23 22 7)')
    a('         (7 24 23 8)')
    a('         (8 25 24 9)')
    a('     );')
    a(' }')
    a(' bottom')
    a(' {')
    a('     type symmetryPlane;')
    a('     faces')
    a('     (')
    a('         (11 27 28 12)')
    a('         (12 28 29 13)')
    a('         (13 29 30 14)')
    a('         (14 30 31 15)')
    a('     );')
    a(' }')
    a('')
    a(');')

    return ''.join(output)

if __name__ == '__main__':
    output = main(
        c = 3,
        t = 1,
        lf = 6,
        lw = 6,
        ht = 6,
        hb = 6,
        alpha = -20,
        n_foil = 15,
        n_north = 15,
        n_east= 10,
        n_south= 20,
        n_west=10,
        e_foil=1,
        e_north=5,
        e_east=2,
        e_south=5,
        e_west=2,
        user_name='bsp'
    )

    file = open('blockMeshDict', 'w')
    file.write(output)