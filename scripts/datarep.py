#!/usr/bin/env python3

import dataclasses

@dataclass
class BasicType:
    name: str
    nBytes: int
    cppTypeName: str

dataTypes = {
    i8: basicType('i8', 8, 'char')
    i16: basicType('i16', 16, 'short')
    i32: basicType('i32', 32, 'int')
    i64: basicType('i64', 64, 'long')

    u8: basicType('u8', 8, 'unsigned char')
    u16: basicType('u16', 16, 'unsigned short')
    u32: basicType('u32', 32, 'unsigned int')
    u64: basicType('u64', 64, 'unsigned long')

    char8: basicType('char8', 8, 'char')

    f32: basicType('f32', 32, 'float')
    f64: basicType('f64', 64, 'double')
    
