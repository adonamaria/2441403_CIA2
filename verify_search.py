"""Independent computation of every numeric / ordering answer used in the quiz."""
import heapq, itertools, random
from collections import deque

# ---------- P1: BFS / DFS on tree G1 ----------
G1 = {"A": ["B","C"], "B": ["D","E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}
def bfs(g, s, goal=None):
    seen, q, order = {s}, deque([s]), []
    while q:
        n = q.popleft(); order.append(n)
        if n == goal: break
        for m in g[n]:
            if m not in seen: seen.add(m); q.append(m)
    return order
def dfs(g, s, goal=None):
    seen, order = set(), []
    def rec(n):
        seen.add(n); order.append(n)
        if n == goal: return True
        for m in g[n]:
            if m not in seen and rec(m): return True
        return False
    rec(s); return order
print("P1 BFS G1:", "".join(bfs(G1,"A")))
print("DFS G1  :", "".join(dfs(G1,"A")))

# ---------- P2: DFS on cyclic undirected graph G2 ----------
G2 = {"S":["A","B"], "A":["C","S"], "B":["D","S"], "C":["A","D"], "D":["B","C","G"], "G":["D"]}
print("P2 DFS G2 to G:", "".join(dfs(G2,"S","G")), "| BFS:", "".join(bfs(G2,"S","G")))

# ---------- P3: IDS visit count on G1 (count every visit, stop at goal) ----------
def dls(g, n, limit, goal, counter):
    counter[0] += 1
    if n == goal: return True
    if limit == 0: return False
    return any(dls(g, m, limit-1, goal, counter) for m in g[n])
total, per = 0, []
for L in range(0, 10):
    c=[0]; found = dls(G1,"A",L,"G",c); total+=c[0]; per.append(c[0])
    if found: break
print("P3 IDS per-iteration visits:", per, "total", total)

# ---------- P4: hill climbing on 1-D landscape ----------
land=[2,4,6,5,3,7,9,8,1]
def hc(i):
    while True:
        nb=[j for j in (i-1,i+1) if 0<=j<len(land)]
        best=max(nb,key=lambda j:land[j])
        if land[best]>land[i]: i=best
        else: return i
print("P4 start1 ->", hc(1), land[hc(1)], "| start4 ->", hc(4), land[hc(4)])

# ---------- P5: greedy vs A* ----------
E={"S":[("A",2),("B",3)],"A":[("G",9)],"B":[("C",2)],"C":[("G",3)],"G":[]}
H={"S":4,"A":2,"B":4,"C":3,"G":0}
def best_first(mode):
    pq=[(H["S"],0,"S",["S"])]; expanded=[]; closed={}
    while pq:
        f,g,n,p=heapq.heappop(pq)
        if n in closed and closed[n]<=g: continue
        closed[n]=g; expanded.append(n)
        if n=="G": return p,g,expanded
        for m,c in E[n]:
            g2=g+c; key = H[m] if mode=="greedy" else g2+H[m]
            heapq.heappush(pq,(key,g2,m,p+[m]))
print("P5 greedy:", best_first("greedy"))
print("   A*    :", best_first("astar"))
# admissible / consistent?
true={}
for n in E:
    # dijkstra backward cost
    pass
def cost_to_goal(n):
    if n=="G": return 0
    return min(c+cost_to_goal(m) for m,c in E[n])
print("   h admissible:", all(H[n]<=cost_to_goal(n) for n in E),
      "consistent:", all(H[n]<=c+H[m] for n in E for m,c in E[n]))

# ---------- P6: water jug 4L/3L, get exactly 2 in 4L jug ----------
def jug_moves(s):
    x,y=s; r=set()
    r.add((4,y)); r.add((x,3)); r.add((0,y)); r.add((x,0))
    t=min(x,3-y); r.add((x-t,y+t))
    t=min(y,4-x); r.add((x+t,y-t))
    r.discard(s); return r
def jug_bfs(goal_fn):
    q=deque([((0,0),0)]); seen={(0,0)}
    while q:
        s,d=q.popleft()
        if goal_fn(s): return d
        for t in jug_moves(s):
            if t not in seen: seen.add(t); q.append((t,d+1))
print("P6 jug (x==2):", jug_bfs(lambda s:s[0]==2), "| any jug==2:", jug_bfs(lambda s:2 in s))

# ---------- P7: 3-colourings: triangle A,B,C + D adjacent to C ----------
edges=[("A","B"),("A","C"),("B","C"),("C","D")]
cnt=0
for col in itertools.product(range(3),repeat=4):
    a=dict(zip("ABCD",col))
    if all(a[u]!=a[v] for u,v in edges): cnt+=1
print("P7 colourings:", cnt)

# ---------- P8: 8-puzzle heuristics ----------
goal=[1,2,3,4,5,6,7,8,0]
def h1(b): return sum(1 for i,t in enumerate(b) if t and t!=goal[i])
def h2(b): return sum(abs(i//3-goal.index(t)//3)+abs(i%3-goal.index(t)%3) for i,t in enumerate(b) if t)
def neighbours(b):
    z=b.index(0); r,c=divmod(z,3)
    for dr,dc in((1,0),(-1,0),(0,1),(0,-1)):
        nr,nc=r+dr,c+dc
        if 0<=nr<3 and 0<=nc<3:
            n=b[:]; n[z],n[nr*3+nc]=n[nr*3+nc],n[z]; yield n
cand=[1,2,3,4,0,6,7,5,8]
for b in ([1,2,3,0,4,6,7,5,8],[1,2,0,4,6,3,7,5,8],[2,8,3,1,6,4,7,0,5],[1,3,6,4,2,0,7,5,8],[4,1,3,7,2,6,0,5,8]):
    print("P8 board",b,"h1",h1(b),"h2",h2(b))
# shortest solution length for a chosen board
def solve_len(b):
    q=deque([(b,0)]); seen={tuple(b)}
    while q:
        s,d=q.popleft()
        if s==goal: return d
        for n in neighbours(s):
            if tuple(n) not in seen: seen.add(tuple(n)); q.append((n,d+1))
for b in ([1,2,3,0,4,6,7,5,8],[1,3,6,4,2,0,7,5,8],[4,1,3,7,2,6,0,5,8]):
    print("  optimal moves", b, solve_len(b))

# ---------- other facts ----------
# reachable 8-puzzle states
seen={tuple(goal)}; q=deque([goal])
while q:
    s=q.popleft()
    for n in neighbours(s):
        if tuple(n) not in seen: seen.add(tuple(n)); q.append(n)
print("8-puzzle reachable states:", len(seen), "of", 362880)
# N(IDS) vs N(BFS) b=10,d=5
b,d=10,5
nids=sum((d-i+1)*b**i for i in range(1,d+1)); nbfs=sum(b**i for i in range(1,d+1))
print("IDS", nids, "BFS", nbfs, "overhead %.1f%%"%(100*(nids-nbfs)/nbfs))
# 4-queens, missionaries & cannibals
def queens(n):
    return sum(1 for p in itertools.permutations(range(n)) if all(abs(p[i]-p[j])!=j-i for i in range(n) for j in range(i+1,n)))
print("4-queens:",queens(4),"8-queens:",queens(8))
