# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:42:04 2020

@author: julie
"""

import simpy
import networkx as nx
import numpy as np
from random import random


# =============================================================================
# Graph de connexions sociales (une personne est représentée par un noeud)
# =============================================================================
nb_individus = 100
nb_moyen_connexions = 2

def buildGraph(n,p):
    '''
    Build a rondom Graph with n nodes and a probability p to connect edges
    Return  the percentage of the nodes in the largest component 
    '''
    G = nx.Graph()
    for i in range(1, n+1):
        G.add_node(i)
        G.node[i]['tps_malade']=-1
        G.node[i]['immunite']=0
    
    nodes = np.array(G.nodes)
    while len(nodes)!=0:
        current_node = nodes[0]
        for node in nodes[1:]:
            probability = random()
            if probability <= p/n : # probabilité de connexion = nb_moyen_connexions / nb_individus
                G.add_edge(current_node, node)
        nodes = nodes[1:]
    
    return G

graph = buildGraph(nb_individus, nb_moyen_connexions)
print(graph.nodes)
print(graph.node[1])


# =============================================================================
# Environnement de simulation
# =============================================================================
# Paramètres variables
tps_contagiosite = 3 # temps pendant lequel une personne portant le virus est contagieuse
tx_transmission = 0.5 # une personne a x% de chances d'être contamminée par une personne contagieuse
qualite_immunite = 1 # qualité de l immunité conférée par un vaccin / le fait d avoir eu la maladie

# initialement, une seule personne est contaminee
graph.node[1]['tps_malade']=0
graph.node[1]['immunite']=qualite_immunite

#def personne(env):
#    while True:
#        print('Personne isolée à %d' % env.now)
#        duree_isolement = 14 #en heures
#        yield env.timeout(duree_isolement)
#        
#        print('Personne connectée à %d' % env.now)
#        duree_connexion = 10 #en heures
#        yield env.timeout(duree_connexion)
        
        
def epidemie(env, G):
    while True:
        # pour 1 journée
        print('\nDébut de la journée %d' % env.now)
        for n in G.nodes:
            
            if G.node[n]['tps_malade'] == tps_contagiosite: # si l'individu est en fin de contagion
                G.node[n]['tps_malade'] = -1 # il n'est plus malade
                G.node[n]['immunite'] = qualite_immunite # et acquiert une immunité
                print(n, "n'est plus contagieux")
            
            if G.node[n]['tps_malade']>=0: # si l'individu est atteind
                G.node[n]['tps_malade'] += 1 # il passe un jour de plus malade
                
                for voisin in list(G.neighbors(n)): # il rencontre ses amis
                    proba_transmission = random()
                    proba_immunite = random()
                    # pour un voisin non malade, et dont les proba sont contre lui...
                    if proba_transmission > tx_transmission and G.node[voisin]['tps_malade'] == -1 and proba_immunite > G.node[voisin]['immunite']: 
                        G.node[voisin]['tps_malade'] = 0 # il contamine son ami
                        print(n, " a contaminé ", voisin)
                        
                    
            
        yield env.timeout(1) #en jours



env = simpy.Environment()
#print(env.process(personne(env)))
#print(env.run(until=49))

print(env.process(epidemie(env, graph)))
print(env.run(until=4))