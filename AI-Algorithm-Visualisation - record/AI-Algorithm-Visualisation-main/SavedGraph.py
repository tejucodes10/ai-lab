
from Node import Node

def G1():
    graph = {'A' : Node('A',(360 , 466)), 'B' : Node('B', (509, 463), 7), 'C' : Node('C', (500, 331), 6),\
        'D' : Node('D', (487, 186), 7), 'E' : Node('E', (650, 170)),'F' : Node('F', (686, 467)),\
            'G' : Node('G', (789, 309)) }
    graph['A'].children = {'B' : 3, 'C' : 5}
    graph['B'].children = {'A' : 3, 'C' : 4, 'F' : 3}
    graph['C'].children = {'A' : 5, 'B' : 4, 'D' : 4}
    graph['D'].children = {'C' : 4, 'E' : 6}
    graph['E'].children = {'D' : 1}
    graph['F'].children = {'B' : 3, 'G' : 5}
    graph['G'].children = {'F' : 5} 

    return graph, 7


def G2():
    graph = {'A' : Node('A',(322 , 471), 11), 'P' : Node('P', (625, 335), 10), 'R' : Node('R', (468, 336), 8),\
        'C' : Node('C', (508, 250), 6), 'M' : Node('M', (479, 474), 9),'L' : Node('L', (316, 332), 9),\
            'E' : Node('E', (647, 316), 3), 'U' : Node('U', (655, 472), 4),\
            'N' : Node('N', (340, ), 6), 'S' : Node('S', (620, 330), 0)}      
    graph['A'].children = {'P' : 4, 'M' : 3}
    graph['P'].children = {'A' : 4, 'C' : 4, 'R' : 4}
    graph['R'].children = {'P' : 4, 'C' : 2, 'E' : 5}
    graph['C'].children = {'P' : 4, 'R' : 2, 'U' : 3,'M':6}
    graph['M'].children = {'A' : 3, 'C' : 6, 'L' : 2}
    graph['L'].children = {'M' : 2, 'N' : 5}
    graph['E'].children = {'R' : 5,'U':5,'S':1}
    graph['U'].children = {'c' : 3,'E':5,'S':4,'N':5}
    graph['N'].children = {'U' : 5,'S':6,'L':5}
    graph['S'].children = {'U' : 4,'E':1,'N':6}                                              

    return graph, 8
