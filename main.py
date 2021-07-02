import csv
from typing import List, Set

INPUT_FILENAME = 'test1.csv'


# Every Node has 3 skills, of which one is the main. These are represented by ints indexing an unreferenced list
class Node:
    def __init__(self, skills: List[int], main: int):
        assert len(skills) == 3
        self.skills = skills
        self.main = main

    def str_short(self) -> str:
        s = "[("
        s += str(self.main)
        s += ")"
        for skill in self.skills:
            if skill != self.main:
                s += " " + str(skill)
        s += "]"
        return s

    def str_long(self) -> str:
        s = "[("
        s += skill_names[self.main]
        s += ")"
        for skill in self.skills:
            if skill != self.main:
                s += " " + skill_names[skill]
        s += "]"
        return s

    def __str__(self) -> str:
        return self.str_long()


class NodeSet:  # arbitrary number of skills
    def __init__(self, num_skills: int):
        self.num_skills = num_skills
        self.nodes: List[Node] = []

    def add(self, node: Node):  # returns NodeSet; python 3.8 does not allow typing for this :O
        self.nodes.append(node)
        return self

    def validate(self) -> bool:
        # main skills cannot repeat
        main_nodes: Set[Node] = set()
        for node in self.nodes:
            if node in main_nodes:
                return False
            main_nodes.add(node)

        # every skill must be present twice
        skill_counts: List[int] = [0] * num_skills  # skill_count[skill index] = occurrences
        for node in self.nodes:
            for skill_no in node.skills:
                skill_counts[skill_no] += 1
        for skill_count in skill_counts:
            if skill_count != 2:
                return False
        return True

    def __str__(self) -> str:
        return ", ".join([str(node) for node in self.nodes])


def processRow(row: List[str]) -> Node:
    main: int
    skills: List[int] = []
    for i, c in enumerate(row):
        if c == 'm':
            main = i
        if c == 'x' or c == 'm':
            skills.append(i)
    assert len(skills) == 3
    return Node(skills, main)


if __name__ == '__main__':
    nodes: List[Node] = []
    with open('csvData/' + INPUT_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        skill_names: List[str] = []
        num_skills: int
        for row in csv_reader:
            if line_count == 0:
                skill_names = row
                num_skills = len(row)
                print(f'Skills are {", ".join(row)}')
                line_count += 1
            else:
                nodes.append(processRow(row))
                # print(f'{", ".join(row)}')
                line_count += 1
        print(f'Scanned {line_count - 1} nodes')

    # hardcoded for 4 nodes (ie 6 skills)
    valid_sets: List[NodeSet] = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            for k in range(j + 1, len(nodes)):
                for l in range(k + 1, len(nodes)):
                    NS = NodeSet(4).add(nodes[i]).add(nodes[j]).add(nodes[k]).add(nodes[l])
                    if NS.validate():
                        valid_sets.append(NS)
    print(valid_sets)
