

#convert all ip addresses to binary
#create treenode with children
from collections import deque
binaryIPs = []

LIMIT = 50

class TrieNode:
    def __init__(self, depth: int, path: str) -> None:
        self.leftNode = None
        self.rightNode = None
        self.depth = depth
        self.path = path

with open('./res.txt', 'rt') as file:
    for line in file:
        parts = line.rstrip('\n').split('.')
        sub1, sub2, sub3, sub4 = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
        binaryIPs.append('' + format(sub1, '08b') + format(sub2, '08b') + format(sub3, '08b') + format(sub4, '08b'))

def getNumberOfLeafNodes(node: TrieNode):
    if not node:
        return 0
    if node.leftNode == None and node.rightNode == None:
        return 1
    return getNumberOfLeafNodes(node.leftNode) + getNumberOfLeafNodes(node.rightNode)
    
def binToSubnetMask(ipStr, depth):
    ipStr = ipStr.strip()
    if len(ipStr) != 32:
        ipStr += ('0' * (32 - len(ipStr)))

    part1 = ipStr[:8]
    part2 = ipStr[8:16]
    part3 = ipStr[16:24]
    part4 = ipStr[24:]
    assert len(part1) == 8, f"Length of part 1 is {len(part1)}"
    assert len(part2) == 8, f"Length of part 2 is {len(part2)}"
    assert len(part3) == 8, f"Length of part 3 is {len(part3)}"
    assert len(part4) == 8, f"Length of part 4 is {len(part4)}"

    return str(int(part1, 2)) + '.' + str(int(part2, 2)) + '.' + str(int(part3, 2)) + '.' + str(int(part4, 2)) + '/' + str(depth)

root = TrieNode(0, "")
for binip in binaryIPs:
    curr = root
    depth = 1
    for c in binip:
        if c == '0':
            if curr.leftNode == None:
                curr.leftNode = TrieNode(depth, curr.path + "0")
            curr = curr.leftNode
        elif c == '1':
            if curr.rightNode == None:
                curr.rightNode = TrieNode(depth, curr.path + "1")
            curr = curr.rightNode
        else:
            print("wtf is c ", c)
        depth += 1

results = []
for i in range(33):
    results.append({})


q = deque()
q.append(root)
while len(q) != 0:
    curr = q.popleft()
    leaf = getNumberOfLeafNodes(curr)
    totalPossible = 2**(32 - curr.depth)
    results[curr.depth][curr.path] = leaf
    if leaf/totalPossible > LIMIT/100:
        continue
    if curr.leftNode != None:
        q.append(curr.leftNode)
    if curr.rightNode != None:
        q.append(curr.rightNode)

with open('blocks.txt', 'wt') as file: 
    file.write(f"Printing the results for blockable IPs above {LIMIT}%\n")
    for d in range(len(results)):
        totalPossible = 2**(32 - d)
        for subnet in sorted(results[d].items(), key=lambda x: x[1]):
            perc = float(subnet[1]/totalPossible) * 100
            if perc > LIMIT:
                file.write(f"This subnet {subnet[0]}({binToSubnetMask(subnet[0], d)}) has a depth of {d}({totalPossible} IPs) and {subnet[1]} leafNodes, blocking it is {perc}% effective.\n")
    

