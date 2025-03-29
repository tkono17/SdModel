#------------------------------------------------------------------------
# Basic data model of SdPage
# sdpage.model
#------------------------------------------------------------------------
import copy
from dataclasses import dataclass, field, asdict
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
    parent: Optional['Element'] = None
    subElements: list['Element'] | None = None

    def fullName(self):
        fullname = self.name
        if self.parent:
            fullname = f'{self.parent.fullName()}.{self.name}'
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
    
    properties: dict[str, Any] | None = None

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
    rootElement: Element | None = None
    
@dataclass        
class ComponentType:
    name: str
    componentName: str
    isArray: bool = field(default=False, kw_only=True)
    arraySize: int | None = field(default=None, kw_only=True)
    
    def __post_init__(self):
        self.name = self.name.strip()
        re1 = re.compile(r'^(.*)[]$')
        re2 = re.compile(r'^(.*)[(\d+)]$')
        resolved = False
        mg1 = re1.match(self.name)
        if mg1:
            self.componentName = mg1.group(1)
            self.isArray = True
            self.arraySize = None
            resolved = True
        else:
            mg2 = re2.match(self.name)
            if mg2:
                self.componentName = mg1.group(1)
                self.isArray = True
                self.arraySize = int(mg2.group(2))
                resolved = True
    
@dataclass
class Model:
    header: Header | None = field(default_factory=Header)
    rootElement: Element | None = None
    components: dict[str, Component] = field(default_factory=dict)
    styles: dict[str, Any] = field(default_factory=dict)

    def addComponent(self, e):
        self.components.append(e)
        e.parent = self

    def findComponent(self, ename):
        v = list(filter(lambda x: x.name == ename, self.components) )
        e = None
        if len(v) == 1:
            e = v[0]
        return e
    
    def componentNames(self):
        names = [ e.name for e in self.components ]
        return names

    pass


