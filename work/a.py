#!/usr/bin/env python3
from dataclasses import dataclass, field

@dataclass
class A:
    a: int = 2
    b: int = field(default=5)

if __name__ == '__main__':
    a = A(a=1)
    print(a)
    
