import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

NUMBER_OF_NODES_ON_Z_PLANE = 24
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
        return Vertex(self.x, self.y, -1*self.z, self.global_i + NUMBER_OF_NODES_ON_Z_PLANE)
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
    a = lambda v0, v1, v2, v3: faces.append(Face(n[v0],n[v1],n[v2],n[v3])) #append

    a(0,8,9,10)
    a(0,10,11,1)
    a(12,2,1,11)
    a(2,12,13,3)
    a(14,4,3,13)
    a(14,15,16,4)
    a(4,16,17,18)
    a(4,18,19,5)
    a(20,6,5,19)
    a(6,20,21,7)
    a(22,0,7,21)
    a(22,23,8,0)

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
    cn = lambda x,y,: nodes.append(Vertex(x,y,dz,nodes_index.i())) # "create node"

    # generate airfoil, rotate by alpha
    cn(c,0)
    cn(c/2,t/2)
    cn(0,t)
    cn(-c/2,t/2)
    cn(-c,0)
    cn(-c/2,-t/2)
    cn(0,-t)
    cn(c/2,-t/2)
    for node in nodes:
        node.rotate(alpha)

    cn(lw,nodes[0].y)
    cn(lw,ht)
    cn(nodes[0].x,ht)
    cn(nodes[1].x,ht)
    cn(nodes[2].x,ht)
    cn(nodes[3].x,ht)
    cn(nodes[4].x,ht)
    cn(lf,ht)
    cn(lf,nodes[4].y)
    cn(lf,hb)
    cn(nodes[4].x,hb)
    cn(nodes[5].x,hb)
    cn(nodes[6].x,hb)
    cn(nodes[7].x,hb)
    cn(nodes[0].x,hb)
    cn(lw,hb)

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
    blocks[2].ex1 = 1/e_north
    blocks[2].nx2 = n_foil
    blocks[2].ex2 = e_foil

    blocks[3].nx1 = n_north
    blocks[3].ex1 = e_north
    blocks[3].nx2 = n_foil
    blocks[3].ex2 = e_foil

    blocks[4].nx1 = n_north
    blocks[4].ex1 = 1/e_north
    blocks[4].nx2 = n_foil
    blocks[4].ex2 = e_foil

    blocks[5].nx1 = n_west
    blocks[5].ex1 = e_west
    blocks[5].nx2 = n_south
    blocks[5].ex2 = 1/e_south

    blocks[6].nx1 = n_west
    blocks[6].ex1 = e_west
    blocks[6].nx2 = n_south
    blocks[6].ex2 = e_south

    blocks[7].nx1 = n_south
    blocks[7].ex1 = e_south
    blocks[7].nx2 = n_foil
    blocks[7].ex2 = e_foil

    blocks[8].nx1 = n_south
    blocks[8].ex1 = 1/e_south
    blocks[8].nx2 = n_foil
    blocks[8].ex2 = e_foil
    
    blocks[9].nx1 = n_south
    blocks[9].ex1 = e_south
    blocks[9].nx2 = n_foil
    blocks[9].ex2 = e_foil

    blocks[10].nx1 = n_south
    blocks[10].ex1 = 1/e_south
    blocks[10].nx2 = n_foil
    blocks[10].ex2 = e_foil

    blocks[11].nx1 = n_east
    blocks[11].ex1 = e_east
    blocks[11].nx2 = n_south
    blocks[11].ex2 = 1/e_south

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
    a('         (15 39 40 16)')
    a('         (16 40 41 17)')
    a('     );')
    a(' }')
    a(' outlet')
    a(' {')
    a('     type patch;')
    a('     faces')
    a('     (')
    a('         (23 47 32 8)')
    a('         (8 32 33 9)')
    a('     );')
    a(' }')
    a(' airfoil')
    a(' {')
    a('     type wall;')
    a('     faces')
    a('     (')
    a('         (0 24 25 1)')
    a('         (1 25 26 2)')
    a('         (2 26 27 3)')
    a('         (3 27 28 4)')
    a('         (4 28 29 5)')
    a('         (5 29 30 6)')
    a('         (6 30 31 7)')
    a('         (7 31 24 0)')
    a('     );')
    a(' }')
    a(' top')
    a(' {')
    a('     type wall;')
    a('     faces')
    a('     (')
    a('         (9 34 33 10)')
    a('         (10 35 34 11)')
    a('         (11 36 35 12)')
    a('         (12 37 36 13)')
    a('         (13 38 37 14)')
    a('         (14 39 38 15)')
    a('     );')
    a(' }')
    a(' bottom')
    a(' {')
    a('     type wall;')
    a('     faces')
    a('     (')
    a('         (17 41 42 18)')
    a('         (18 42 43 19)')
    a('         (19 43 44 20)')
    a('         (20 44 45 21)')
    a('         (21 45 46 22)')
    a('         (22 46 47 23)')
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
        n_foil = 250,
        n_north = 150,
        n_east= 80,
        n_south= 150,
        n_west=160,
        e_foil=20,
        e_north=200,
        e_east=200,
        e_south=200,
        e_west=50,
        user_name='bsp'
    )

    file = open('blockMeshDict', 'w')
    file.write(output)