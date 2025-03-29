#!/usr/bin/env python3
from dataclasses import asdict
from detModel import *
import math
import json

class PixelBuilder:
    def __init__(self, detector=None):
        self.detector = detector
        self.nLayers = lambda: 5
        self.nStavesInLayer = lambda ilayer: 8 + ilayer*4
        self.nModulesInStave = lambda ilayer, istave: 10

    def build(self):
        det = self.detector
        if det.barrel is None:
            det.barrel = PixelBarrel('barrel')
        self.buildBarrel(det.barrel)

    def buildBarrel(self, barrel):
        if barrel.layers is None:
            barrel.layers = [
                PixelLayer(f'layer{ilayer}')
                for ilayer in range(self.nLayers())
            ]
        for ilayer, det1 in enumerate(barrel.layers):
            self.buildLayer(det1, ilayer)
            
    def buildLayer(self, layer, ilayer):
        if layer.staves is None:
            layer.staves = [
                PixelStave(f'stave{istave}')
                for istave in range(self.nStavesInLayer(ilayer) )
            ]
        for istave, stave in enumerate(layer.staves):
            self.buildStave(stave, ilayer, istave)

    def buildStave(self, stave, ilayer, istave):
        if stave.modules is None:
            stave.modules = [
                PixelModule(f'module{imodule}')
                for imodule in range(self.nModulesInStave(ilayer, istave) )
            ]
        for imodule, module in enumerate(stave.modules):
            self.buildModule(module, ilayer, istave, imodule)
        wx, wy = 500.0, 50.0
        r = 40.0 + 20.0*ilayer
        n = self.nStavesInLayer(ilayer)
        dtheta = math.pi/9*1.5
        #
        theta = 2.0*math.pi/n * istave
        x, y = r*math.cos(theta), r*math.sin(theta)
        stave.T = [ round(x, 3), round(y, 3) ]
        #
        theta -= math.pi/2 - dtheta
        c, s = math.cos(theta), math.sin(theta)
        c, s = round(c, 4), round(s, 4)
        stave.R = [ c, -s, s, c ]

    def buildModule(self, module, ilayer, istave, imodule):
        x0, y0 = 25.0, 25.0
        wx, wy = 50.0, 50.0
        module.T = [ wx * imodule + x0, y0 ]

if __name__ == '__main__':
    detector = PixelDetector('Pixel')
    pixelBuilder = PixelBuilder(detector)
    pixelBuilder.build()
    data = asdict(detector)
    with open('pixel.json', 'w') as fout:
        json.dump(data, fout, indent=2)
