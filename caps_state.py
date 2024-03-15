from random import randint, seed
from caps_operators import Swap,Jump



class proposta:

    def __init__(self,n=20,caps_predeterminats: list = None, rand_seed = 41):
        seed(rand_seed)
        self.n = n
        if caps_predeterminats == None:
            self.llista = [None]*n

            for i in range(len(self.llista)):
                temp_cap = self.dades_cap()
                self.llista[i] = cap(temp_cap[0], temp_cap[1], temp_cap[2], temp_cap[3], temp_cap[4])
        else:
            self.llista = caps_predeterminats
        self.unitats = []
        

    def canviar_caps(self, unitat1,unitat2,index1,index2):
        aux = unitat1.caps.pop(index1)
        unitat2.caps.append(aux)
        unitat1.append(unitat2.caps.pop(index2))

    def dades_cap(self):
        self.nom_cap = str(input("Indica el nom del cap: "))
        self.sexe_cap = ""
        while self.sexe_cap != "M" and self.sexe_cap != "F":
            self.sexe_cap = str(input("Indica el sexe del cap (M/F): "))
        
        unitats = ["cill","enx","llid","ring","pic","truc"]
        self.preferencia = []
        for j in range(6):
            unitat = ""
            while unitat not in unitats:
                unitat = str(input("Quina unitat vols en lloc "+ str(j+1) +": "+ str(unitats)+ "\n"))

            self.preferencia.append(unitats.pop(unitats.index(unitat)))
        
        persona  = "?"
        self.persones_si = []
        while persona != "":
            persona = str(input("Amb qui t'agradaria compartir unitat? (si és ningú o ja has acabat deixa en blanc)"))
            self.persones_si.append(persona)
        
        persona_no  = "?"
        self.persones_no = []
        while persona_no != "":
            persona_no = str(input("Amb qui NO t'agradaria compartir unitat? (si és ningú o ja has acabat deixa en blanc)"))
            self.persones_no.append(persona_no) 
        
        this_cap = (self.nom_cap, self.sexe_cap, self.preferencia, self.persones_si, self.persones_no)
        return this_cap
    
    def crear_unitats(self,persones = [3,4,4,4,3,2]):
        llista_de_caps = []
        for cap in self.llista:
            llista_de_caps.append(cap.copy_cap())

        noms_unitats = ["cill","enx","llid","ring","pic","truc"]
        self.unitats: list[unitat] = []
        for i in range(6):
            caps_unitat = []
            for j in range(persones[i]):
                assig = llista_de_caps.pop(randint(0,len(llista_de_caps)-1))
                caps_unitat.append(assig)
            self.unitats.append(unitat(noms_unitats[i],caps_unitat))
    
    def heuristic(self):
        puntuacio = 0

        for unitats in self.unitats:
            bubuseados = 0
            caps_unitat = unitats.noms_caps()

            for caps in unitats.caps:
                puntuacio += caps.pref_unit.index(unitats.nom_unitat)**(1.5)
                
                if caps.bubusea == True:
                    bubuseados += 1

                for company in caps.pers_si:

                    if company in caps_unitat:
                        puntuacio -= 3
                
                for enemic in caps.pers_no:

                    if enemic in caps_unitat:
                        puntuacio += 8

            if bubuseados >= 2:
                puntuacio += 8*(bubuseados-1)

            puntuacio += unitats.unitat_mixta()

        return puntuacio

    def afinitat_persones(self):
        puntuacio = 0
        for unitats in self.unitats:
            caps_unitat = unitats.noms_caps()
            for caps in unitats.caps:
                for company in caps.pers_si:
                    if company in caps_unitat:
                        puntuacio += 3
                for enemic in caps.pers_no:
                    if enemic in caps_unitat:
                        puntuacio -= 8
        return puntuacio
    
    def afinitat_unitats(self):
        puntuacio = 0
        for unitats in self.unitats:
            caps_unitat = unitats.noms_caps()
            for caps in unitats.caps:
                puntuacio += caps.pref_unit.index(unitats.nom_unitat)**(1.5)
        return puntuacio
    
    def unitats_mixtes(self):
        puntuacio = 0
        for unitats in self.unitats:
            puntuacio -= unitats.unitat_mixta()
        return puntuacio
    
    def swap(self,index_unitat,index_cap,index_unitat2,index_cap2):
        aux = self.unitats[index_unitat].caps[index_cap]
        self.unitats[index_unitat].caps[index_cap] = self.unitats[index_unitat2].caps[index_cap2]
        self.unitats[index_unitat2].caps[index_cap2] = aux
    
    def jump(self,index_unitat,index_cap,index_unitat2):
        if len(self.unitats[index_unitat].caps) == 4:
            if len(self.unitats[index_unitat2].caps) <= 3:
                if self.unitats[index_unitat2].nom_unitat != "truc":
                    aux = self.unitats[index_unitat].caps.pop(index_cap)
                    self.unitats[index_unitat2].caps.append(aux)    
        

    def copy_poposta(self):
        caps_nous = []
        for i in range(self.n):
            caps_nous.append(self.llista[i].copy_cap())

        new_proposta = proposta(self.n,caps_nous)
        new_proposta.unitats = []
        for unitats in self.unitats:
            new_proposta.unitats.append(unitats.copy_unitat())
        
        return new_proposta

    def generate_actions(self):
        possible_actions = [Swap]
        for main_unitat in self.unitats:
            for main_cap in main_unitat.caps:
                for second_unitat in self.unitats:
                    yield(Jump(self.unitats.index(main_unitat),main_unitat.caps.index(main_cap),self.unitats.index(second_unitat)))
                    for second_cap in second_unitat.caps:
                        yield(Swap(self.unitats.index(main_unitat),main_unitat.caps.index(main_cap),self.unitats.index(second_unitat),second_unitat.caps.index(second_cap)))
    
    def apply_actions(self,action):

        copia_estat = self.copy_poposta()
        if type(action) == Swap:
            copia_estat.swap(action.unitat,action.cap_index,action.unitat2,action.cap_index2)
        
        elif type(action) == Jump:
            copia_estat.jump(action.unitat,action.cap_index,action.unitat2)
        
        return copia_estat

                    

                      

class cap(proposta):
    def __init__(self,nom,sexe, pref_unit,pers_si, pers_no, bubusea = False):
        self.bubusea = bubusea
        self.nom = nom
        self.pref_unit = pref_unit
        self.pers_si = pers_si
        self.pers_no = pers_no
        self.sexe = sexe

    def copy_cap(self):
        new_cap = cap(self.nom,self.sexe,self.pref_unit,self.pers_si,self.pers_no,self.bubusea)
        return new_cap

    def __repr__(self):
        return f"{self.nom}"

class unitat(proposta):

    def __init__(self,nom_unitat: str, caps: list[cap]):
        self.nom_unitat = nom_unitat
        self.caps = caps
    
    def noms_caps(self):
        result = []
        for capo in self.caps:
            result.append(capo.nom)
        
        return result
    
    def unitat_mixta(self):
        test = self.caps[0].sexe
        for capo in self.caps:
            if capo.sexe != test:
        
                return -3
        if self.nom_unitat != "truc":
            return +10
        else:
            return -1

    def copy_unitat(self):
        caps_copia = []
        for cap in self.caps:
            caps_copia.append(cap.copy_cap())

        nova_unitat = unitat(self.nom_unitat,caps_copia)
        return nova_unitat
    
    def __repr__(self):
        return f"{self.nom_unitat}: {self.caps}"


