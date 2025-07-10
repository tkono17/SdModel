#------------------------------------------------------------------------
# Basic data model of SdPage
# sdpage.model
#------------------------------------------------------------------------
import copy
from dataclasses import dataclass, field, asdict, InitVar, KW_ONLY
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

@dataclass
class Header:
    name: str = None
    version: str | None = None
    authors: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)

    def firstAuthor(self):
        x = ''
        if authors is not None and len(self.authors)>0:
            x = self.authors[0]
        return x

@dataclass
class Element:
    name: str
    componentType: str
    subElements: list['Element'] = field(default_factory=list)
    parentName: str = field(default='', kw_only=True)
    properties: dict[str, Any] | None = None

    def fullName(self):
        fullname = self.name
        if self.parentName != '':
            fullname = f'{self.parentName}.{self.name}'
        return fullname
    
    def addSubElement(self, c):
        self.subElements.append(c)
        
    def setSubElements(self, v):
        self.subElements = v

    def nSubElements(self):
        return len(self.subElements)

    def findSubElement(self, names):
        element = None
        n1 = len(names)
        if n1 == 0:
            return element
        name0 = names[0]
        for e in self.subElements:
            if e.name == name0:
                element = e
                if n1 == 1:
                    break
                else:
                    element = e.findSubElement(names[1:])
        return element    

    def setProperties(self, **kwargs):
        self.properties.update(copy.deepcopy(kwargs))
        
    def setProperty(self, pName, pValue):
        self.properties[pName] = pvalue

    def property(self, pName):
        if pName in self.properties.keys():
            return self.properties[pName]
        else:
            return None

@dataclass
class Component:
    name: str
    baseType: str | None = None
    _: KW_ONLY
    subElements: list[Element] | None = field(default_factory=list)

    def fullName(self):
        fullname = self.name
        return fullname

    def addSubElement(self, c):
        self.subElements.append(c)
        
    def setSubElements(self, v):
        self.subElements = v

    def nSubElements(self):
        return len(self.subElements)

    def findSubElement(self, names):
        element = None
        n1 = len(names)
        if n1 == 0:
            return element
        name0 = names[0]
        for e in self.subElements:
            if e.name == name0:
                element = e
                if n1 == 1:
                    break
                else:
                    element = e.findSubElement(names[1:])
        return element

@dataclass
class ComponentArray:
    name: str
    elementType: str = None
    nElements: int | None = None
    
@dataclass
class ComponentType:
    name: str
    component: Component | ComponentArray | None = None

    def resolveName(self):
        componentName = ''
        isArray = False
        arraySize = None
        #
        self.name = self.name.strip()
        re1 = re.compile(r'^(.*)[]$')
        re2 = re.compile(r'^(.*)[(\d+)]$')
        #
        resolved = False
        mg1 = re1.match(self.name)
        if mg1:
            componentName = mg1.group(1)
            isArray = True
            arraySize = None
            resolved = True
        else:
            mg2 = re2.match(self.name)
            if mg2:
                componentName = mg1.group(1)
                isArray = True
                arraySize = int(mg2.group(2))
                resolved = True
        return (componentName, isArray, arraySize)
    
@dataclass
class Model:
    header: Header | None = field(default_factory=Header)
    contents: list[Element] | None = None
    components: dict[str, Component] = field(default_factory=dict)
    styles: dict[str, Any] = field(default_factory=dict)

    def name(self):
        x = ''
        if self.header: x = self.header.name
        return x
    
    def addComponent(self, e):
        self.components.append(e)

    def findComponent(self, cname):
        v = list(filter(lambda x: x.name == cname, self.components) )
        e = None
        if len(v) == 1:
            e = v[0]
        return e
    
    def componentNames(self):
        names = [ e.name for e in self.components ]
        return names

    def findStyle(self, sname):
        style = None
        if sname in self.styles:
            style = self.styles[sname]
        return style

    pass


