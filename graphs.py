# WARNING!  Do not edit this file!  The original graphs.py will be used when marking your code.

def assertIsUndirectedGraph(V, E):
   edgesSymmetric = all( {(v, u) in E for (u,v) in E} )
   if not edgesSymmetric:
      raise(ValueError('Edge set is not symmetric.  Not an undirected graph.'))

def N(V, E, u):
   """Returns the set of vertices in V that are adjacent to u given edges E.

   If (V,E) is the entire graph, returns the neighbourhood of vertex u."""
   assertIsUndirectedGraph(V, E)
   return { v for v in V if (u,v) in E }

def NS(V, E, S):
   """Returns the set of vertices in V that are adjacent to a vertex in S given edges E.

   If (V,E) is the entire graph, returns the neighbourhood of S."""
   assertIsUndirectedGraph(V, E)
   return { v for v in V for u in S if (u,v) in E }

def degree(V, E, u):
   """Return the degree of the vertex u in the graph (V, E), i.e. the size of its neighbourhood."""
   assertIsUndirectedGraph(V, E)
   return len(N(V, E, u))

def distanceClasses(V, E, u, D = None):
   """Given a graph (V,E) and a starting vertex u, outputs a list of distances classes.  That is, returns a partition of the vertices into sets of fixed distances from u, where u is in the distance class for distance 0.  Behaviour is undefined if the graph is disconnected."""
   if D is None:                             # j = 0 case
      assertIsUndirectedGraph(V, E)
      D = [ {u} ]                            # D[0] = D_0 = {u}
      return distanceClasses(V, E, None, D)  # recurse to get remaining distance classes
   
   Vnew = V - D[-1]                          # V_{j} = V_{j-1} / D_{j-1}
   Dnew = D + [ NS(Vnew, E, D[-1]) ]         # D_{j} = N_{V_j}(D_{j-1})
   if len(Dnew[-1]) == 0: return D           # Didn't find any more vertices.  All done or G is disconnected.
   return distanceClasses(Vnew, E, None, Dnew)

def distance(V, E, u, v):
   """Given two vertices u,v in the graph (V,E) return the length of the shortest path from u to v, or float('inf') if no path exists.  float('inf') is used as it can be compared with other numbers and is >= any integer."""
   D = distanceClasses(V, E, u)
   for j, Dj in enumerate(D):
      if v in Dj:
         return j
   return float('inf')

def arbitrary(S):
   """Return an arbitrary element of the set S"""
   if S:
      return next(iter(S))
   return None

def connected(V, E):
   """Given a graph (V,E) return True if it is connected, otherwise False."""
   v = arbitrary(V)
   D = distanceClasses(V, E, v)
   return V == set.union(*D)

def spanningTree(V, E, r):
   """Find a spanning tree in graph (V,E) rooted on r where all paths from vertex r to other vertices are shortest.  If the graph is disconnected then the spanning tree only covers the component containing r.
   
   The tree is returned as a dictionary where keys are vertices and values are the parent of that vertex in the spanning tree.  The root has parent None."""

   D = distanceClasses(V, E, r)        # 
   Dpairs = zip(D[:-1], D[1:])         # iterator over pairs (D_j-1, D_j)

   parents = { 
      v: arbitrary(N(Dprev, E, v)) 
      for Dprev, Dj in Dpairs 
      for v in Dj 
   }
   parents[r] = None

   return parents

def pathFromTree(parents, v):
   """Find a shortest path from the root to vertex v in a tree.  The tree must be given as a dictionary where keys are vertices and values are the parent verticex of the key.  The path is returned as a list of vertices starting from the root and ending at v (inclusive).  If v is not in the tree then None is returned."""
   if v not in parents: return None        # vertex not in the tree, no path.
   u = parents[v]
   if u == None: return [v]                # at root? Stop
   return pathFromTree(parents, u) + [v]   # go to parent, then to v

def shortestPath(V, E, start, end, D=None):
   """Solve the shortest path problem in graph (V,E) from vertex start to vertex end.  Path is returned as a list of vertices.  If there is no such path then None is returned."""

   if start is end: return [ start ]  # base case

   # Get the distance classes in the outer function call
   if D is None:
      D = distanceClasses(V, E, end)

   j = next( (j for j, Dj in enumerate(D) if start in Dj), None)  # find start's distance class
   if j is None: return None                                      # no path from start to end
   v = arbitrary(N(V, E, start) & D[j - 1])                       # take one step towards end 
   return [ start ] + shortestPath(V, E, v, end, D)               # take remaining steps


def isIndependentSet(U, E):
   """Returns True when there are no edges between any two vertices in U given edge set E"""
   assertIsUndirectedGraph(U, E)
   return all( (u,v) not in E for u in U for v in U )

def bipartition(V, E):
   """If the graph (V, E) is bipartite then returns a pair (A,B) which is a bipartition.  Otherwise returns None."""
   v = arbitrary(V)
   if v is None: return set(), set()       # Empty vertex set, trivial bipartition.

   # A,B will be even and odd distances from v
   D = distanceClasses(V, E, v)
   
   # check that there are no edges within each distance class
   if not all( isIndependentSet(Dj, E) for Dj in D ):
      return None                          # Not bipartite
   
   A = set.union( *D[0::2] )               # Slice starting at 0 to the end, step 2.  even indices
   B = set.union( *D[1::2], set() )        # Slice odd indices.  Set() argument deals with case of single vertex in V.
   if A | B == V: return A, B              # Check whether we have found all vertices
   
   # There are some vertices left.  Partition them up and union the partitions.
   r = bipartition(V - ( A | B), E)
   if r is None: return None               # Not bipartite
   A2, B2 = r
   return A | A2, B | B2                   # The graph was disconnected, so no edges between A and A2 or between B and B2 

def colourClassesFromColouring(C):
   """Given a graph colouring in the form of a dictionary C with keys being vertices and values being colours, return a partition of the vertices where each set in the partition has the same colour.
   """
   
   return [
      { v for v, v_colour in C.items() if v_colour == colour }
      for colour in set(C.values())
   ]


def minColouring(V,E, k=None, C=None, kbest=None, Cbest=None):
   """Given a graph (V,E) determines the chromatic number of the graph.  Returns (k, C) where k is an integer giving the chromatic number and C is a dictionary with keys V and values in 0, ..., k-1 giving the colour for each vertex.
   
   Note that the return type here does not match the lecture's definition, which is a partition into k sets.  If the partition is desired then it can be obtained from the returned C with colourClassesFromColouring(C).

   If the graph has a loop then no colouring exists. float('inf'), dict() returned. """
   
   # Set up variables for base case
   if k is None:
      assertIsUndirectedGraph(V, E)
      if any((v, v) in E for v in V): return float('inf'), dict()    # found a loop.  No colourings.

      C = { v: None for v in V }  # empty colouring
      kbest = float('inf')        # no colouring found, initial best will be infinity
      k = 1                       # start with only one colour

   # Check if any vertices left to colour
   if None not in C.values():
      # Check to see if what we have is better than the previous best
      if k < kbest:
         return k, dict(C)        # make a copy since C is also held by our caller
      return kbest, Cbest
   
   # Choose a next vertex to colour
   v = next( v for v in V if C[v] is None )
   badcolours = { C[u] for u in N(V, E, v) } - { None }
   
   if len(badcolours) >= kbest:
      # already used up all colours and have more to colour. Can't improve, so return
      return kbest, Cbest
   
   if len(badcolours) >= k:
      # used up all colours, add a new one
      k = k + 1
   
   # Try all possible colours
   for c in range(k):
      if c in badcolours: continue     # a neighbour has this colour, skip.
      C[v] = c                         # Try to assign this colour 
      kret, Cret = minColouring(V, E, k, C, kbest, Cbest)   # Find the best colouring that extends C
      
      # If we found a better colouring, keep it.
      if kret < kbest:
         kbest = kret
         Cbest = Cret

   # Undo what we did for the caller who shares C.
   C[v] = None
   return kbest, Cbest