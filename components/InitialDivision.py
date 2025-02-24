from collections import deque
from typing import List, Dict, Any
from utils.student import Student
from random import shuffle

class Node:
    __slots__ = ['data', 'neighbors', 'd', 'f', 'pie', 'color', 'student']

    def __init__(self, data=None, student=None):
        self.data = data
        self.student = student
        self.neighbors = []
        self.d = None
        self.f = None
        self.pie = None
        self.color = None  # "White", "Gray", "Black", or "Red" (when assigned)
    
    def __repr__(self):
        return f"Node({self.data})"
    
    def __gt__(self, other):
        return self.data > other.data
        
    def __lt__(self, other):
        return self.data < other.data
    
    def __eq__(self, other):
        return self.data == other.data
        
    def __hash__(self):
        return hash(self.data)

def DFS(nodes: Dict[Any, Node]) -> None:
    time = 0

    def DFS_VISIT(u: Node):
        nonlocal time
        u.color = "Gray"
        time += 1
        u.d = time
        for v in u.neighbors:
            if v.color == "White":
                v.pie = u
                DFS_VISIT(v)
        time += 1
        u.f = time
        u.color = "Black"

    # Initialize all nodes for DFS
    for node in nodes.values():
        node.pie = None
        node.color = "White"
    # Run DFS from each unvisited node
    for node in nodes.values():
        if node.color == "White":
            DFS_VISIT(node)

def is_valid_group(group: List[Node]) -> bool:
    """
    Check that for every node in the group, at least one neighbor (preference) is also in the group.
    """
    s = set(group)
    for node in group:
        if not any(n in s for n in node.neighbors):
            return False
    return True

def get_group(node: Node, group_size: int, partial: List[Node] = None, depth: int = 0, limit: int = 100) -> List[Node]:
    """
    Recursively attempt to build a group starting at 'node'.
    The group must be of size group_size and satisfy the preference condition.
    Added depth parameter to limit excessive recursion.
    """
    if depth > limit:
        return []
        
    if partial is None:
        partial = []
    current_group = partial + [node]
    
    # If we reached the target group size, check if the group is valid
    if len(current_group) == group_size:
        return current_group if is_valid_group(current_group) else []
    
    # Then try each neighbor that is not yet assigned and not already in the group.
    for nbr in node.neighbors:
        if nbr.color != "Red" and nbr not in current_group:
            result = get_group(nbr, group_size, current_group, depth + 1, limit)
            if result:
                return result
    return []

def group_ungrouped_nodes(ungrouped: List[Node], group_size: int) -> List[List[Node]]:
    """
    For nodes that were not grouped by get_group, create groups of group_size.
    This fallback method does not re-check the preference condition.
    """
    groups = []
    while ungrouped:
        # Take the first group_size nodes (or whatever remains)
        group = ungrouped[:group_size]
        for node in group:
            node.color = "Red"
        groups.append(group)
        ungrouped = ungrouped[group_size:]
    return groups

def dfs_grouping(students: List[Student], num_groups: int) -> List[List[Node]]:
    # Create nodes for each student
    nodes: Dict[Any, Node] = {student.id: Node(student.id, student) for student in students}
    # Build a dictionary of student preferences
    preferences: Dict[Any, List[Any]] = {student.id: student.preferences for student in students}
    # Build the graph: for each student, add neighbors based on preferences
    for student in students:
        for pref in preferences[student.id]:
            if pref in nodes:
                nodes[student.id].neighbors.append(nodes[pref])
    # Run DFS over the nodes to set discovery times and parent pointers
    DFS(nodes)

    # Create a deque sorted by discovery time (largest d first)
    Q = deque(sorted(nodes.keys(), key=lambda key: nodes[key].d if nodes[key].d is not None else 0, reverse=True))
    groups = []
    n = len(students)
    target_size = n // num_groups

    # Build groups by attempting to form a valid group starting from each node
    while Q:
        current = nodes[Q.popleft()]
        if current.color != "Red":
            group = get_group(current, target_size, limit=n)
            if group:
                for node in group:
                    node.color = "Red"
                groups.append(group)
    
    # Process any nodes that have not been assigned
    ungrouped_nodes = [node for node in nodes.values() if node.color != "Red"]
    # Calculate maximum group size (if not perfectly divisible)
    max_group_size = target_size + (1 if n % num_groups != 0 else 0)
    groups += group_ungrouped_nodes(ungrouped_nodes, max_group_size)

    return groups

def initialize_groups(students: List[Student], num_groups: int) -> List[List[Student]]:
    """
    Shuffle the students and create initial groups based on their preferences.
    """
    print(1)
    shuffle(students)
    node_groups = dfs_grouping(students, num_groups)
    # Convert groups of Nodes back to groups of Student objects
    student_groups = [[node.student for node in group] for group in node_groups]
    return student_groups
