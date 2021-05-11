import numpy as np

_ = 18


class System:
    def __init__(self):
        import pickle
        with open(str(_)+'.pickle', 'rb') as f:
            self.space, self.empty = pickle.load(f), None

    def __repr__(self):
        ret = [['  ']+['{:02}'.format(i) for i in range(1, _+1)]]
        ret += [['  ']*(_+1) for i in range(7)]
        for i, o in enumerate('XEGDAC'):
            for j, c in enumerate((self.space == o).sum(0)/len(self())):
                ret[i+2][j] = '{:02}'.format(round(99*c)) if c > 0 else '--'
            ret[i+2][0], ret[i+2][-1] = o+' ', ret[i+2][0]
        return '\n'.join(['  '.join(r) for r in ret])

    def __call__(self, i=None, j=None):
        if self.empty is None:
            self.empty = np.where(self.space == 'X', 'E', self.space)
        if i is None:
            return self.empty
        i %= _
        if j is None:
            return self.empty[:, i]
        j %= _
        return self.empty[:, range(i, j+1) if i <= j else [*range(i, _), *range(0, j+1)]]

    def filter(self, con):
        old = len(self())
        self.space, self.empty = self.space[con], None
        return (len(self()), round(len(self())/old, 6))

    def set(self, i, j, o, c):
        return self.filter((self(i, j) == o).sum(1) == c)

    def act(self, sky):
        l = self.locate()
        if l[0][0] > 1/2:
            return l
        return sorted([*self.survey(sky), *self.target(sky)])[:6]

    def locate(self):
        ret = []
        for i in range(_):
            s = self.space[self.space[:, i] == 'X'][:, ((i-1) % _, (i+1) % _)]
            for o, c in zip(*np.unique(s, return_counts=True, axis=0)):
                ret.append((c/len(self()), o[0], i, o[1]))
        return sorted(ret, reverse=True)[:6]

    def survey(self, sky):
        ret = []
        C = {2, 3, 5, 7, 11, 13, 17}
        for i in range(sky, sky+_//2):
            for j in range(i, sky+_//2):
                s = self(i, j)
                for o in 'CADGE':
                    if o == 'C' and (i % _ not in C or j % _ not in C):
                        continue
                    x = np.unique((s == o).sum(1), return_counts=True)[
                        1]/len(self())
                    ret.append(
                        ((x**2).sum()**(1/(4-(j-i)//3)), i % _, j % _, o))
        return sorted(ret)[:6]

    def target(self, sky):
        ret = []
        for i in range(sky, sky+_//2):
            x = np.unique(self(i), return_counts=True)[1] / len(self())
            ret.append(((x**2).sum()**(1/4), i % _))
        return sorted(ret)[:6]

    def theory(self, oth=[]):
        ret = []
        P = {'C': 3, 'A': 2, 'D': 8-_/3, 'G': 4, 'E': -1}
        for i in range(_):
            for o, c in zip(*np.unique(self(i), return_counts=True)):
                ret.append(((P[o]+(i not in oth)+2)*c/len(self())-2, i, o))
        return sorted(ret, reverse=True)[:6]

    def within(self, qty, ob1, win, ob2):
        ret = np.array([False]*len(self()))
        def identity(x): return x != 0
        neg = np.logical_not if qty in 'NA' else identity
        sub = identity if qty in 'NO' else np.logical_not
        for i in range(_):
            s = self.space.take(range(i-win, i+win+1), axis=1, mode='wrap')
            ret = ret | ((s[:, win] == ob1) & sub((s == ob2).sum(1)))
        return self.filter(neg(ret))
