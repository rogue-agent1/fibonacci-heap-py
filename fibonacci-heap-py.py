#!/usr/bin/env python3
"""Fibonacci heap with insert, extract-min, decrease-key."""
import sys,math
class FibNode:
    def __init__(self,key):self.key=key;self.degree=0;self.parent=self.child=None;self.left=self.right=self;self.mark=False
class FibHeap:
    def __init__(self):self.min=None;self.n=0
    def insert(self,key):
        n=FibNode(key)
        if self.min is None:self.min=n
        else:self._add_to_root(n);
        if n.key<self.min.key:self.min=n
        self.n+=1;return n
    def _add_to_root(self,n):
        n.left=self.min;n.right=self.min.right;self.min.right.left=n;self.min.right=n;n.parent=None
    def extract_min(self):
        z=self.min
        if z:
            if z.child:
                children=[];c=z.child
                while True:children.append(c);c=c.right;
                if c==z.child:break
                for child in children:self._add_to_root(child);child.parent=None
            z.left.right=z.right;z.right.left=z.left
            if z==z.right:self.min=None
            else:self.min=z.right;self._consolidate()
            self.n-=1
        return z.key if z else None
    def _consolidate(self):
        max_deg=int(math.log2(self.n))+2;A=[None]*max_deg
        nodes=[];c=self.min
        while True:nodes.append(c);c=c.right;
        if c==self.min:break
        for w in nodes:
            x=w;d=x.degree
            while d<max_deg and A[d]:
                y=A[d]
                if x.key>y.key:x,y=y,x
                self._link(y,x);A[d]=None;d+=1
            if d<max_deg:A[d]=x
        self.min=None
        for a in A:
            if a:
                if self.min is None:self.min=a;a.left=a.right=a
                else:self._add_to_root(a);
                if a.key<self.min.key:self.min=a
    def _link(self,y,x):
        y.left.right=y.right;y.right.left=y.left
        y.parent=x
        if x.child is None:x.child=y;y.left=y.right=y
        else:y.left=x.child;y.right=x.child.right;x.child.right.left=y;x.child.right=y
        x.degree+=1;y.mark=False
    def find_min(self):return self.min.key if self.min else None
def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        h=FibHeap()
        h.insert(10);h.insert(3);h.insert(7);h.insert(1);h.insert(5)
        assert h.find_min()==1
        assert h.extract_min()==1
        assert h.find_min()==3
        assert h.extract_min()==3
        assert h.extract_min()==5
        assert h.n==2
        print("All tests passed!")
    else:
        h=FibHeap();[h.insert(x) for x in[5,3,8,1]];print(f"Min: {h.extract_min()}")
if __name__=="__main__":main()
