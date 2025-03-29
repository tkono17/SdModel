#------------------------------------------------------------------------
# Page builder
# sdmodel.builder
#------------------------------------------------------------------------
import logging
from .model import Model, Header, Component, Element

logger = logging.getLogger(__name__)

C = Component
E = Element

class ModelBuilder(Model):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def findNodes(self, element):
        nodes = []
        cnames = []
        if element:
            if element.baseComponent:
                for child in element.baseComponent.children:
                    v = self.findNodes(child)
                    for c in v:
                        cfname = c.fullName()
                        if c and cfname not in cnames:
                            cnames.append(cfname)
                            nodes.append(c)
            else:
                for c in element.children:
                    v = self.findNodes(c)
                    for c in v:
                        cfname = c.fullName()
                        if c and cfname not in cnames:
                            cnames.append(cfname)
                            nodes.append(c)
            if element.baseComponent:
                nodes.append(element.baseComponent)
            if element.name not in cnames:
                nodes.append(element)
        return nodes
    
    def arrange(self):
        logger.info('Rearrange page model={self.model}')
        if self.model:
            logger.info('Rearrange page')
            nodes = self.findNodes(self.model)
            print(nodes)
            for node in nodes:
                nodeClass = node.__class__.__name__
                logger.info(f'  node {node.name} {nodeClass}')
                if issubclass(node.__class__, Component):
                    self.components.append(node)
                fullname = node.fullName()
                for key, value in node.properties.items():
                    self.properties[f'{fullname}.{key}'] = value
        else:
            logger.warning('Builder model is None')
    
