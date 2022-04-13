from threading import Lock, Semaphore, Thread
import time


LIMITE_DEPOSITO = 10
caixas_no_deposito = 0

MUTEX_DEPOSITO = Lock()
pode_depositar = Semaphore(LIMITE_DEPOSITO)
pode_carregar = Semaphore(caixas_no_deposito)


class TremT(Thread):
    def __init__(self, n, tv):
        '''Thread Trem
        -n : número de caixas transportadas
        -tv: tempo de viagem
        '''
        Thread.__init__(self)
        self.caixas_no_trem = 0
        self.limite_caixas = n
        self.tempo_viagem = tv
        self.executando = True

    def parar_trem(self):
        self.executando = False
        print("trem para garagem")

    def carregando(self):
        global caixas_no_deposito, LIMITE_DEPOSITO

        pode_carregar.acquire()

        with MUTEX_DEPOSITO:
            caixas_no_deposito -= self.limite_caixas
            self.caixas_no_trem += self.limite_caixas
            print('\ncaixas no deposito:' + str(caixas_no_deposito))
            print('\ncaixas no trem:' + str(self.caixas_no_trem))
            time.sleep(1)
        for _ in range(self.limite_caixas):
            pode_depositar.release()

    def descarregando(self):
        global caixas_no_deposito, LIMITE_DEPOSITO
        print("\ndescarregando caixas do trem, caixas:" + str(self.caixas_no_trem))
        self.caixas_no_trem -= self.caixas_no_trem

    def viajando_para_B(self):
        print("\nVIAJANDO PARA B")
        time.sleep(self.tempo_viagem)
        print("\nCHEGOU EM B")

    def viajando_para_A(self):
        print("\nVIAJANDO PARA A")
        time.sleep(self.tempo_viagem)
        print("\nCHEGOU EM A")

    def run(self):
        while self.executando:
            self.carregando()
            self.viajando_para_B()
            self.descarregando()
            self.viajando_para_A()
        print("parou de executar")


class EmpacotadorT(Thread):
    def __init__(self, id, te, n):
        Thread.__init__(self)
        self.empacotandoo = True
        self.tempo_empacotando = te
        self.empacotador = id
        self.n = n

    def empacotando(self):
        global caixas_no_deposito, MUTEX_DEPOSITO, pode_carregar
        pode_depositar.acquire()

        print(f"\nEmpacotador {str(self.empacotador)}\nempacotando")
        time.sleep(self.tempo_empacotando)
        print(f"\n{str(self.empacotador)} terminou de empacotar")

        with MUTEX_DEPOSITO:
            caixas_no_deposito += 1
            print(f'\nEmpacotador {str(self.empacotador)} adicionou ao deposito: {str(caixas_no_deposito)}')
            if caixas_no_deposito >= self.n:
                pode_carregar.release()
                print("liberado")

    def run(self):
        while True:
            self.empacotando()


if __name__ == '__main__':
    N = 4
    TV = 5

    t1 = TremT(N, TV)
    t1.start()

    te = [1, 1, 1, 1]
    lista_Empacotadores = [EmpacotadorT(id_empacotador, tempo, N) for id_empacotador, tempo in enumerate(te)]

    for emp in lista_Empacotadores:
        emp.start()