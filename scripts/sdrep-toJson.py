#!/usr/bin/env python3
import logging
import sdrep

logger = logging.getLogger(__name__)

def main(args):
    reader = sdrep.ModelReader()
    reader.read('ex1.yaml')
    model = reader.getModel()
    reader.saveJson('ex1.json')

if __name__ == '__main__':
    args = {}
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s %(name)-10s %(message)s')
    main(args)
    
