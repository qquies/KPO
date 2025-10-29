class UseCaseElement:
    def __init__(self, name, element_type):
        self.name = name
        self.type = element_type  # 'actor', 'usecase', 'system', 'database'
        self.connections = []
        self.include_connections = []  # Специально для <<include>> отношений
    
    def add_connection(self, target, relationship="association"):
        self.connections.append({
            'target': target, 
            'relationship': relationship,
            'type': 'association'
        })
    
    def add_include_connection(self, target):
        """Добавляет связь использования <<include>>"""
        self.include_connections.append({
            'target': target,
            'relationship': 'include',
            'type': 'include'
        })
    
    def get_all_connections(self):
        """Возвращает все связи включая include"""
        return self.connections + self.include_connections

class UseCaseDiagram:
    def __init__(self, name):
        self.name = name
        self.elements = {}
    
    def add_element(self, element):
        self.elements[element.name] = element
    
    def get_element(self, name):
        return self.elements.get(name)
    
    def get_elements_by_type(self, element_type):
        return [elem for elem in self.elements.values() if elem.type == element_type]
