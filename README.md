# Euro-Flow
##### By Amy Reichhold

## Overview and Goal of Project
Everyone loves to travel, especially young adults, and especially to Europe. 
The main considerations are where to visit and the cost of the entire trip. 
Ideally, a traveler would like to visit all of their desired destinations for 
as little cost as possible (transportation, lodging, food, etc.). The problem
of finding the minimum cost for visiting a set of destinations conceivably
could be represented as a max-flow problem. So, the resulting problem is how
to transform the desired places to visit into a graph and then find the
minimum cost path and create an itinerary from the path found.


### Initial Idea: Use the Ford-Fulkerson max-flow algorithm
Initially, I thought the problem of visiting destinations in Europe, for the 
lowest cost possible, could be represented as a flow network and then I could
run the max-flow algorithm on the network. 

I planned on setting up the graph with the countries as the vertices and the 
costs of traveling between countries as the edges. Each country vertex is 
split into two nodes (for entering and leaving the country) to account for
ensuring the traveler visits the country and for the cost of staying in that
country. I would use Dijkstra's shortest path algorithm and a cost function to
find the shortest path that goes to every vertex, and use flow conservation to
ensure that the traveler does not go to a country (pair of vertices) more than
once.

The first issue I ran into was that the minimum-cost flow from the traveler's
origin, through a selection of countries, and then back to the origin,
actually resulted in a flow that was only going through one country. The other
issue I ran into was that max-flow algorithm requires an acyclic graph, which
is not the case for the graph we must construct for this problem. That is, we
essentially want to have the option of starting the traveler's tour with any
of the countries, and be able to go to any unvisited country from any other
country, which necessarily includes cycles.

I then decided to talk to one of my past professors who confirmed that it is
not possible to set up this problem as a max-flow problem and that this
problem is closely related to the traveling sales problem, which is NP-
complete. In other words, this problem is equivalent to a well-known problem
that requires a computationally intensive algorithm for solving optimally.
My professor said that under certain conditions there is an efficient
heuristic for solving the problem, which we describe in the next section.


### New Idea: Use Prim's minimum spanning tree algorithm
The main concern with representing my problem as the traveling sales problem 
is that the triangle inequality has to hold for the graph in question. After
discussing my problem with my professor, we agreed that the triangle
inequality will most likely hold.

In this case, we still have the graph described previously, which has the
countries as the vertices and the cost of traveling between countries as the
weights on the edges, but the vertices are not split into two vertices. Every
vertex connects with all of the other vertices because as mentioned
previously, the traveler can go to any country from any other country. After
creating the graph, the next step was implementing Prim's algorithm, which
returns a minimum spanning tree, which is a version of the graph which only
includes the minimum weight edges for connecting all the vertices. We then
traverse the minimim spanning tree using preorder traversal to get the minimum
cost path (Europe trip).

### Correctness
Because we are using a heuristic and do not know in general whether a graph
constructed from countries and traveling costs will maintain the triangle
inequality, I wanted to implement a validator function which exhaustively
tries every possible path and returns the minimum cost path. The path returned
from the validator function was equal to the path returned from the heuristic-
based implementation (using Prim's and preorder traversal) on four test
examples that I tried. Thus, the triangle equality held for these test
examples. But in the case that a particular graph does not satisfy the
heuristic, then the validator function will reveal this quality and show what
is truly the minimum cost trip.


### Future work
This project is a proof of concept for creating a Euro-Trip app, which
focuses on the problem of computing the minimum cost for visiting a set of
destinations and given traveling costs. It currently uses manually-chosen
destinations and costs, but we would like to have the project automatically
gather available countries and the current travel costs for those countries,
using sockets for accessing a database of some sort over the Internet. It
would also likely work well as a mobile app and/or Web site, which would
require user interface design and submission to app stores and/or Web hosting.
This would ideally include implementing the project in Swift and HTML. It
would still be called Euro-Flow even though it can't be solved using the max-
flow approach, because Euro-Flow sounds better than Euro-MST (or Euro-Prim).

Additionally, it may be possible to avoid running the validator every time by
implementing a triangle-inequality checker to see if we need to run the
validator. This may be as computationally expensive as simply running the
validator, but more investigation is needed.
