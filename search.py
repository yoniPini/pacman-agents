# yonatan pinchas 315538074
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

"""
This class is for assistant for building the searchAgents
so that each node is able to return its solution if asked
and its cost.
moreover, there are 2 get state methods:
    1. getState - the familiar method
    2. getOnlyState - in case the getState includes nore tuples it
                        returns the first tuple in it, i.e, the packman position.
"""


class Node:
    def __init__(self, state: tuple, direction=None, cost=0, source_node=None):
        self.state = state
        self.direction = direction
        self.source_node = source_node
        self.cost = cost
        if self.source_node:
            self.cost += source_node.cost

    def __eq__(self, other) -> bool:
        if other != None:
            return self.state == other.state
        return False

    def getState(self): return self.state
    def getDirection(self): return self.direction

    def solution(self) -> list:
        if self.source_node == None:
            return []
        solutions = [self.direction]
        return self.source_node.solution() + solutions

    def path_cost(self) -> int: return self.cost

    def getOnlyState(self):
        if isinstance(self.state[0], int):
            return self.state
        return self.state[0]


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    frontier = util.Stack()
    frontier.push(Node(problem.getStartState()))
    close_list = {()}
    close_list.clear()
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.getState()):
            return node.solution()
        close_list.add(node.getState())
        succ = problem.getSuccessors(node.getState())
        for i in range(len(succ)):
            if succ[i][0] not in close_list and Node(succ[i][0]) not in frontier.list:
                frontier.push(Node(succ[i][0], succ[i][1], succ[i][2], node))
    return None
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    frontier.push(Node(problem.getStartState()))
    close_list = {()}
    close_list.clear()
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.getState()):
            return node.solution()
        close_list.add(node.getState())
        succ = problem.getSuccessors(node.getState())
        for i in range(len(succ)):
            if succ[i][0] not in close_list and Node(succ[i][0]) not in frontier.list:
                frontier.push(Node(succ[i][0], succ[i][1], succ[i][2], node))
    return None
    util.raiseNotDefined()


def isNodeInHeap(n: Node, l: list) -> bool:
    for e in l:
        if n == e[2]:
            return True
    return False


def best_first_graph_search(problem, f):
    frontier = util.PriorityQueue()  # Priority Queue
    temp = Node(problem.getStartState())
    frontier.push(temp, f(temp))
    closed_list = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.getState()):
            return node.solution()
        closed_list.add(node.getState())
        succ = problem.getSuccessors(node.getState())
        for i in range(len(succ)):
            if succ[i][0] not in closed_list and not isNodeInHeap(Node(succ[i][0]), frontier.heap):
                temp = Node(succ[i][0], succ[i][1], succ[i][2], node)
                frontier.push(temp, f(temp))
            elif succ[i][0] in frontier.heap:
                t = Node(succ[i][0], succ[i][1], succ[i][2], node)
                index = frontier.heap.index(Node(succ[i][0]))
                if f(t) < f((frontier.heap)[index]):
                    frontier.update(t, f(t))
    return None


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    def g(node):
        return node.path_cost()
    return best_first_graph_search(problem, f=g)
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    def g(node): return node.path_cost()

    return best_first_graph_search(problem, f=lambda n: g(n)+heuristic(n, problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
