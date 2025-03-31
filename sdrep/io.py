#------------------------------------------------------------------------
# Basic data model of SdModel
# sdmodel.io
#------------------------------------------------------------------------
import copy
import logging
import pathlib
import re
import json
import yaml
from dataclasses import asdict

from .model import Component, Element, Header, Model

logger = logging.getLogger(__name__)

class ModelReader:
    def __init__(self, fileName: str=''):
        self.filePath = fileName
        self.data = None
        self.model = None

    def read(self, fileName: str=''):
        if fileName != '':
            self.filePath = fileName
        if self.filePath != '':
            fpath = pathlib.Path(self.filePath)
            match fpath.suffix:
                case '.json':
                    logger.warning(f'JSON file is not supported {fpath}')
                case '.yaml' | '.yml':
                    self.loadYaml(fpath)
                case '.xml':
                    pass
                case _:
                    logger.warning(f'Unsupported suffix {fpath.suffix}, {fpath}')
        pass

    def loadYaml(self, fpath: pathlib.Path):
        self.data = None
        if fpath.is_file() and fpath.exists():
            with open(fpath.absolute(), 'r') as fin:
                self.data = yaml.load(fin, Loader=yaml.SafeLoader)
        if self.data: self.toModel(self.data)
        return self.model

    def getModel(self):
        return self.model

    def convElement(self, cdata, parent=None):
        e1 = None
        if type(cdata) == type({}):
            logger.info(f'  element is a map with {len(cdata)} items')
            if len(cdata) == 1:
                for k1, v1 in cdata.items():
                    logger.info(f'    Create element {k1} ({len(v1)} sub elements)')
                    e1 = self.createElement(k1, parent)
                    self.convSubElements(v1, e1)
            else:
                logger.error(f'component as a map with more than one entries')
        elif type(cdata) == type(''):
            k1 = cdata
            logger.info(f'  Create an element with no children')
            e1 = self.createElement(k1, parent)
        return e1

    def decodeKey(self, k):
        re1 = re.compile(r'(.*){(.*)}')
        name, ctype = '', ''
        mg1 = re1.match(k)
        if mg1:
            name, ctype = mg1.groups()
        return (name, ctype)
    
    def createElement(self, k, parent):
        element = None
        name, cType = self.decodeKey(k)
        if name == '':
            logger.error(f'Cannot parse element information from "{k}"')
            return None
        parentName = ''
        if parent:
            parentName = parent.fullName()
        element = Element(name=name, componentType=cType, parentName=parentName)
        logger.info(f'create element {name}')
        if parent:
            parent.addSubElement(element)
        return element
    
    def convSubElements(self, v, parent):
        for sub in v:
            csub = self.convElement(sub, parent)
        return parent
    
    def convElements(self, section):
        elements = None
        if type(section) != type([]):
            logger.error(f'contents section should be a list of elements')
        else:
            elements = []
            for e in section:
                elements.append(self.convElement(e) )
        logger.info(f'Found {len(elements)} top-element(s)')
        return elements
        
    def setHeader(self, header, section):
        for k, v in section.items():
            match k:
                case 'name': header.name = v
                case 'version': header.version = v
                case 'authors': header.authors = list(v)
                case 'context': header.context = v
                case _: logger.warning(f'Unknown key in header {k}')
        pass

    def convComponents(self, section):
        # This section should be a list of components
        if section is None:
            return []
        components = {}
        for cdata in section:
            tname = type(cdata).__name__
            subElements = None
            match tname:
                case 'dict':
                    key = list(cdata.keys())[0]
                    logger.info(f'Component as a dictionary found {key}')
                    subElements = cdata[key]
                case 'str':
                    key = cdata
                    logger.info(f'Component as a string found {key}')
                case _:
                    logger.error(f'Component should be a dictionary')
            name, baseType = self.decodeKey(key)
            c = Component(name, baseType)
            if subElements:
                self.convSubElements(subElements, c)
            components[name] = c
        return components

    def toModel(self, data):
        self.model = Model()
        if data is None:
            return self.model
        keys = data.keys()
        for key in keys:
            section = data[key]
            match key:
                case 'header':
                    self.setHeader(self.model.header, section)
                case 'contents':
                    self.model.contents = self.convElements(section)
                case 'components':
                    self.model.components = self.convComponents(section)
                case 'styles':
                    if section:
                        print(section)
                        self.model.styles.update(copy.deepcopy(section) )
                case _:
                    logger.warning(f'Unknown section {key}')
        return self.model
    
    def saveJson(self, fn):
        data = asdict(self.model)
        with open(fn, 'w') as fout:
            logger.info(f'Save model to JSON {fn}')
            json.dump(data, fout, indent=2)

    def saveXml(self, fn):
        logger.warning('saveXml is not available yet')
