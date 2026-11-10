class UnionFind:
    def __init__(self, names):
        self._parent = {name: name for name in names}
        self._rank = {name: 0 for name in names}

    def find(self, x: str) -> str:
        """Return the representative (root) of x's component."""
        while self._parent[x] != x:
            self._parent[x] = self._parent[self._parent[x]]  # path halving
            x = self._parent[x]
        return x

    def union(self, x: str, y: str) -> bool:
        """Merge the components of x and y. Return False if already merged."""
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x
        self._parent[root_y] = root_x                        # attach smaller under larger
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1
        return True