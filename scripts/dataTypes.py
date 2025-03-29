#!/usr/bin/env python3
from dataclasses import dataclass, field, asdict
import math
import json

@dataclass
class BasicType:
    name: str
    nBytes: int | None
    cppType: str | None

i8 = BasicType(name='i8', nBytes=1, cppType='char')
i16 = BasicType(name='i16', nBytes=2, cppType='short')
i32 = BasicType(name='i32', nBytes=4, cppType='int')
i64 = BasicType(name='i64', nBytes=8, cppType='long')

char8 = BasicType(name='char8', nBytes=1, cppType='char')
uchar8 = BasicType(name='uchar8', nBytes=1, cppType='unsigned char')

