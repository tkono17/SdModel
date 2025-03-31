#!/usr/bin/env python3
import argparse
import logging
import sdrep

logger = logging.getLogger(__name__)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-yaml', '-i', dest='inputYaml',
                        type=str, default='',
                        help='Input YAML file')
    return parser.parse_args()

def main(args):
    reader = sdrep.ModelReader()
    reader.read(args.inputYaml)
    model = reader.getModel()
    reader.saveJson(f'{model.name()}.json')

if __name__ == '__main__':
    args = parseArgs()
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s %(name)-10s %(message)s')
    main(args)
    
