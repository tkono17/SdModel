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
                    if self.data: self.toModel(self.data)
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
        return self.data

    def getModel(self):
        return self.model

    def convElement(self, cdata, parent=None):
        logger.info(f'convElement top {cdata}')
        comp = None
        if type(cdata) == type({}):
            if len(cdata) == 1:
                for k1, v1 in cdata.items():
                    logger.info(f'Convert component {k1}')
                    comp = self.convElementM(k1, v1, parent)
                    break
            else:
                logger.error(f'component as a map with more than one entries')
        elif type(cdata) == type(''):
            k1 = cdata
            logger.info(f'Convert component scalar {k1}')
            comp = self.convElementS(k1, parent)
        return comp

    def decodeKey(self, k):
        re1 = re.compile(r'(.*){(.*)}')
        name, ctype = '', ''
        mg1 = re1.match(k)
        if mg1:
            name, ctype = mg1.groups()
        return (name, ctype)
    
    def convElementS(self, k, parent):
        component = None
        name, ctype = self.decodeKey(k)
        if name == '':
            logger.error(f'Cannot parse component information from "{k}"')
            return None
        if parent:
            component = Element(name=name, componentType=ctype, parent=parent)
        return component
    
    def convElementM(self, k, v, parent):
        component = self.convElementS(k, parent)
        #
        if component != None:
            for sub in v:
                csub = self.convElement(sub, component)
                if csub != None:
                    component.addSubElement(csub)
        return component

    def setHeader(self, header, section):
        for k, v in section.items():
            match k:
                case 'name': header.name = v
                case 'version': header.name = v
                case 'authors': header.authors = list(v)
                case 'context': header.context = v
                case _: logger.warning(f'Unknown key in header {k}')
        pass
    
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
                case 'model':
                    parent = 1
                    e = self.convElement(data[key])
                    if e: e.parent = None
                    self.model.rootElement = e
                case 'components':
                    components = []
                    if section is None: continue
                    for cdata in section:
                        tdata = type(cdata)
                        match tdata:
                            case type({}): key = cdata.keys()[0]
                            case _:
                                logger.error(f'Component should be a dictionary')
                        name, ctype = self.decode(key)
                        c = Component(name, ctype)
                        c = self.convElement(cdata)
                        components.append(c)
                    names = map(lambda x: x.name, components)
                    self.model.components.update({
                        k: components[k] for k in names
                    })
                case 'styles':
                    if section:
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
