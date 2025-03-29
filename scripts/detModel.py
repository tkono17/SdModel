#!/usr/bin/env python3
from dataclasses import dataclass, field

@dataclass
class Base:
    name: str
    T: list[float] = field(default_factory=lambda: [0.0,0.0], kw_only=True)
    R: list[float] = field(default_factory=lambda: [1.0,0.0,0.0,1.0], kw_only=True)

@dataclass
class PixelModule(Base):
    pass

@dataclass
class PixelStave(Base):
    modules: list[PixelModule] | None = None

@dataclass
class PixelLayer(Base):
    staves: list[PixelStave] | None = None

            
@dataclass
class PixelBarrel(Base):
    layers: list[PixelLayer] | None = None

            
@dataclass
class PixelRing(Base):
    modules: list[PixelModule] | None = None

@dataclass
class PixelEndcap(Base):
    rings: list[PixelRing] | None = None

@dataclass
class PixelDetector(Base):
    barrel: PixelBarrel | None = None
    endcapA: PixelEndcap | None = None
    endcapC: PixelEndcap | None = None

if __name__ == '__main__':
    detector = PixelDetector('Pixel')
    data = asdict(detector)
    with open('det.json', 'w') as fout:
        json.dump(data, fout, indent=2)
