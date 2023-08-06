%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Extraction of graph data from edge information.
%
% initial version:  24/03/2017   cfrioux
%
% Extract the connected components of the graph and provide seeds
% Input:
%       -
% Output (one model per connected component):
%       -
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% deprecated, see ~/wd/carnoules/predator for a working version


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%% Reachability definitions %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% compounds are reactants or products i.e. metabolites
compound(M) :- reactant(M,_).
compound(M) :- product(M,_).

% scope definition
reach(M) :- reaction(R) ; product(M,R);
            reach(N) : reactant(N,R).

% seeds
1{seed(M) : compound(M)}.

% seeds are reachable, they initiate the recursive reachability
reach(M) :- seed(M).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%% Connected components search %%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% compound A we look at is SC with X if both are reachable
allume(A,X) :- reach(A) ; reach(X).

% putative strongly connected component
put_scca(A,X) :- A<X ; allume(A,X) ; allume(X,A).

% we refer to a SCCA with the min lexicographic component
scca(A) :- put_scca(A,_) ; not put_scca(A,M) : M<A.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Yield what we want %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#show scca/1.
#show put_scca(A,_) : scca(A).
