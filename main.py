import threading
import time

limite_deposito = 20
caixas_no_deposito = 0


class Trem(threading.Thread):
    N = 0
    tv = 0
    
    def __init__(self, N, tv):
        threading.Thread.__init__(self)
        self.caixas_no_trem, self.limite_caixas, self.tempo_viagem = 0, N, tv
        self.carregandoo, self.descarregandoo, self.viajando_para__B, self.viajando_para__A = True, False, False, False
        self.timee2, self.j = 0, 0

    def carregando(self):
        global caixas_no_deposito, limite_deposito
        if caixas_no_deposito < self.limite_caixas:
            self.carregandoo = False
        else:
            self.carregandoo = True
            print("CARREGANDO TREM")    
        while self.carregandoo:
            
            caixas_no_deposito -= 1
            self.caixas_no_trem += 1
            print('caixas no deposito:' + str(caixas_no_deposito))
            print('caixas no trem:' + str(self.caixas_no_trem))
            time.sleep(1)
            if self.caixas_no_trem == self.limite_caixas:
                self.carregandoo = False
                self.viajando_para__B = True
                   
    
    def descarregando(self):
        global caixas_no_deposito, limite_deposito
        
        while self.descarregandoo:
            
            if self.caixas_no_trem > 0:
                self.caixas_no_trem -= 1
                
                print("descarregando caixas do trem, caixas:" + str(self.caixas_no_trem))
            else:
                self.descarregandoo = False 
                self.viajando_para__A = True 


    def viajando_para_B(self):
        if self.viajando_para__B:
            self.j = 0
            self.timee2 = 0
            self.timee2 = round(time.time() * 1000)
            print("VIAJANDO PARA B")
            while round(time.time() * 1000) - self.timee2 < (self.tempo_viagem)*1000:
                self.j += 1
            
            print("CHEGOU EM B")
            self.descarregandoo = True
            self.viajando_para__B = False 
     
     
    def viajando_para_A(self):
        if self.viajando_para__A:
            self.j = 0
            self.timee2 = 0
            self.timee2 = round(time.time() * 1000)
            print("VIAJANDO PARA A")
            while round(time.time() * 1000) - self.timee2 < (self.tempo_viagem)*1000:
                self.j += 1
            
            print("CHEGOU EM A")
            self.carregandoo = True
            self.viajando_para__A = False

    def run(self):
        while True:
            self.carregando()
            self.viajando_para_B()
            self.descarregando()
            self.viajando_para_A()




class Empacotador(threading.Thread):
    id = 0
    te = 0

    def __init__(self, id, te):
        threading.Thread.__init__(self)
        self.limite_empacotadores, self.empacotandoo, self.tempo_empacotando, self.empacotador = 0, True, te, id
        self.timee = 0
        self.k = 0

    def empacotando(self):
        global limite_deposito, caixas_no_deposito
        if caixas_no_deposito < limite_deposito:
            self.timee = round(time.time() * 1000)
            self.k = 0
            print("Empacotador"+ str(self.empacotador) + "\nempacotando")
            #print(self.timee)
            while round(time.time() * 1000) - self.timee < (self.tempo_empacotando) * 1000:
                self.k += 1
                self.empacotandoo = True
            
            while self.empacotandoo:
                caixas_no_deposito += 1
                print("empacotado")
                print('deposito:' + str(caixas_no_deposito))
                self.empacotandoo = False
        


    def run(self):
        while True:
            self.empacotando()
        


        




t1 = Trem(8, 5)
t2 = Empacotador(1, 4)








t2.start()
t1.start()





