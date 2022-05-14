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
    "*** YOUR CODE HERE ***"

    # run: python pacman.py -l bigMaze -z .5 -p SearchAgent
    # python pacman.py -l tinyMaze/mediumMaze/bigMaze (-z 0.5<->.5, 1, 1.5, ... : tỉ lệ) -p SearchAgent

    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []

    exploredStates = []
    frontier = util.Stack()
    frontier.push((startState, []))  # tuple: (state/node, list actions: 'action' is the action required to get there)

    while not frontier.isEmpty():
        currentState, actions = frontier.pop()
        if currentState not in exploredStates:
            exploredStates.append(currentState)

            if problem.isGoalState(currentState):
                return actions

            for successor, action, stepCost in problem.getSuccessors(currentState):
                newAction = actions + [action]
                frontier.push((successor, newAction))

    util.raiseNotDefined()

    # frontier.push((startState, []))
    # exploredStates.append(startState)
    #
    # while not frontier.isEmpty():
    #     currentState, actions = frontier.pop()
    #
    #     if problem.isGoalState(currentState):
    #         return actions
    #
    #     for successor, action, stepCost in problem.getSuccessors(currentState):
    #         if successor not in exploredStates:
    #             frontier.push((successor, actions + [action]))
    #             exploredStates.append(successor)
    #
    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []

    exploredStates = []
    frontier = util.Queue()
    frontier.push((startState, []))

    while not frontier.isEmpty():
        currentState, actions = frontier.pop()
        if currentState not in exploredStates:
            exploredStates.append(currentState)

            if problem.isGoalState(currentState):
                return actions

            for successor, action, stepCost in problem.getSuccessors(currentState):
                newAction = actions + [action]
                frontier.push((successor, newAction))

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []

    exploredStates = []
    frontier = util.PriorityQueue()

    # func param <-> elementPQ: (item: <state, actions, cost>, priority)
    # -> heapq.heappush(self.heap, entry: (priority, self.count, item))
    frontier.push((startState, [], 0), 0)

    while not frontier.isEmpty():
        currentState, actions, pathCost = frontier.pop()  # pop return only item

        if currentState not in exploredStates:
            exploredStates.append(currentState)

            if problem.isGoalState(currentState):
                return actions

            for successor, action, stepCost in problem.getSuccessors(currentState):
                frontier.update((successor, actions + [action], pathCost + stepCost), pathCost + stepCost)  # push or update

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []

    exploredStates = []
    frontier = util.PriorityQueue()

    # func param <-> elementPQ: (item: <state, actions, cost>, priority)
    # -> heapq.heappush(self.heap, entry: (priority, self.count, item))
    frontier.push((startState, [], 0), 0)

    while not frontier.isEmpty():
        currentState, actions, pathCost = frontier.pop()
        if currentState not in exploredStates:
            exploredStates.append(currentState)

            if problem.isGoalState(currentState):
                return actions

            for successor, action, stepCost in problem.getSuccessors(currentState):
                pathCostToSuc = pathCost + stepCost
                heuristicCost = pathCostToSuc + heuristic(successor, problem)
                frontier.push((successor, actions + [action], pathCostToSuc), heuristicCost)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
