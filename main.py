import threading
import time




limite_deposito = 15
caixas_no_deposito = 0
verif = 0
MUTEX = threading.Lock()
deposito_empty = threading.Semaphore(20)
deposito_full = threading.Semaphore(caixas_no_deposito)

class TremT(threading.Thread):
    N = None
    tv = None

    def __init__(self, N, tv):
        threading.Thread.__init__(self)
        self.caixas_no_trem, self.limite_caixas, self.tempo_viagem = 0, N, tv
        self.carregandoo, self.descarregandoo, self.viajando_para__B, self.viajando_para__A = False, False, False, False
        self.timee2, self.j = 0, 0

    def carregando(self):
        global caixas_no_deposito, limite_deposito
        #ESPERANDO_LIMITE_CAIXAS_TREM.release()
        if caixas_no_deposito < self.limite_caixas:
            self.carregandoo = False
        else:
            self.carregandoo = True
            print("\nCARREGANDO TREM")

        while self.carregandoo:

            caixas_no_deposito -= 1
            self.caixas_no_trem += 1
            print('\ncaixas no deposito:' + str(caixas_no_deposito))
            print('\ncaixas no trem:' + str(self.caixas_no_trem))
            time.sleep(1)
            if self.caixas_no_trem == self.limite_caixas:
                self.carregandoo = False
                self.viajando_para__B = True
                #ESPERANDO_LIMITE_CAIXAS_TREM.acquire()

    def descarregando(self):
        global caixas_no_deposito, limite_deposito

        while self.descarregandoo:

            if self.caixas_no_trem > 0:
                self.caixas_no_trem -= 1

                print("\ndescarregando caixas do trem, caixas:" + str(self.caixas_no_trem))
            else:
                self.descarregandoo = False
                self.viajando_para__A = True

    def viajando_para_B(self):
        if self.viajando_para__B:
            self.j = 0
            self.timee2 = 0
            self.timee2 = round(time.time() * 1000)
            print("\nVIAJANDO PARA B")
            while round(time.time() * 1000) - self.timee2 < (self.tempo_viagem) * 1000:
                self.j += 1

            print("\nCHEGOU EM B")
            self.descarregandoo = True
            self.viajando_para__B = False

    def viajando_para_A(self):
        if self.viajando_para__A:
            self.j = 0
            self.timee2 = 0
            self.timee2 = round(time.time() * 1000)
            print("\nVIAJANDO PARA A")
            while round(time.time() * 1000) - self.timee2 < (self.tempo_viagem) * 1000:
                self.j += 1

            print("\nCHEGOU EM A")
            self.carregandoo = True
            self.viajando_para__A = False

    def run(self):
        while True:
            self.carregando()
            self.viajando_para_B()
            self.descarregando()
            self.viajando_para_A()


class EmpacotadorT(threading.Thread):
    id = 0
    te = 0

    def __init__(self, id, te):
        threading.Thread.__init__(self)
        self.limite_empacotadores, self.empacotandoo, self.tempo_empacotando, self.empacotador = 0, True, te, id
        self.timee = 0
        self.k = 0



    def empacotando(self):
        global limite_deposito, caixas_no_deposito, verif
        MUTEX.acquire()
        if verif < limite_deposito:
            MUTEX.release()
            self.timee = round(time.time() * 1000)
            self.k = 0
            verif += 1

            print(f"\nEmpacotador {str(self.empacotador)}\nempacotando")

            while round(time.time() * 1000) - self.timee < (self.tempo_empacotando) * 1000:
                self.k += 1


            caixas_no_deposito += 1


            print(f"\n{str(self.empacotador)} terminou de empacotar")
            print(f'\ndeposito adicionado: {str(caixas_no_deposito)}')
            #self.empacotandoo = False

    def run(self):
        while True:
            self.empacotando()



t1 = TremT(4, 5)
te = [1, 1, 1, 1]
Empacotadores = []


def run_threads():
    for i, k in zip(range(4), te):
        Empacotadores.append(EmpacotadorT(i, k))

    for j in Empacotadores:
        j.start()

    #t1.start()


run_threads()