class CapsOperator(object):
    
    def __init__(self) -> None:
        pass

class Swap(CapsOperator):

    def __init__(self,unitat,cap_index,unitat2,cap_index2) -> None:
        self.unitat = unitat
        self.cap_index = cap_index
        self.unitat2 = unitat2
        self.cap_index2 = cap_index2
    
    def __repr__(self) -> None:
        return f"Swap {self.unitat.caps[self.cap_index]} with {self.unitat2.caps[self.cap_index2]}"

class Jump(CapsOperator):

    def __init__(self,unitat,cap_index,unitat2) -> None:
        self.unitat = unitat
        self.cap_index = cap_index
        self.unitat2 = unitat2
    
    def __repr__(self) -> str:
        return f"Jump {self.unitat.caps[self.cap_index]} to {self.unitat2}"

