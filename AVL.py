class No:
    def __init__(self, val):
        self.valor = val
        self.altura = 1
        self.esq = None
        self.dir = None

class AVL:
    def __init__(self):
        self.raiz = None

    def altura(self, no):
        if no is None:
            return 0
        return no.altura

    def obter_fator_balanceamento(self, no):
        if no is None:
            return 0
        
        return self.altura(no.esq) - self.altura(no.dir)

    def atualizar_altura(self, no):
        no.altura = 1 + max(self.altura(no.esq), self.altura(no.dir))

    def rotacionar_a_direita(self, y):
        x = y.esq
        z = x.dir
        x.dir = y
        y.esq = z
        self.atualizar_altura(y)
        self.atualizar_altura(x)
        return x
    
    def rotacionar_a_esquerda(self, x):
        y = x.dir
        z = y.esq
        y.esq = x
        x.dir = z
        self.atualizar_altura(x)
        self.atualizar_altura(y)
        return y
    
    def rebalancear(self, no):
        self.atualizar_altura(no)
        fator = self.obter_fator_balanceamento(no)

        # Caso Esquerda-Esquerda (LL) e Esquerda-Direita (LR)
        if fator > 1:
            if self.obter_fator_balanceamento(no.esq) >= 0:
                # Caso LL
                return self.rotacionar_a_direita(no)
            else:
                # Caso LR
                no.esq = self.rotacionar_a_esquerda(no.esq)
                return self.rotacionar_a_direita(no)

        # Caso Direita-Direita (RR) e Direita-Esquerda (RL)
        if fator < -1:
            if self.obter_fator_balanceamento(no.dir) <= 0:
                # Caso RR
                return self.rotacionar_a_esquerda(no)
            else:
                # Caso RL
                no.dir = self.rotacionar_a_direita(no.dir)
                return self.rotacionar_a_esquerda(no)

        return no
    
    def inserir(self, valor):
        self.raiz = self._inserir(self.raiz, valor)
    
    def _inserir(self, no, valor):
        if no is None:
            return No(valor)
        elif valor < no.valor:
            no.esq = self._inserir(no.esq, valor)
        elif valor > no.valor:
            no.dir = self._inserir(no.dir, valor)
        else:
            
            return no

        return self.rebalancear(no)
    
    def deletar(self, valor):
        self.raiz = self._deletar(self.raiz, valor)

    def _deletar(self, no, valor):
        if no is None:
            return no

        if valor < no.valor:
            no.esq = self._deletar(no.esq, valor)
        elif valor > no.valor:
            no.dir = self._deletar(no.dir, valor)
        else:
            if no.esq is None:
                return no.dir
            elif no.dir is None:
                return no.esq
            
            # Nó com dois filhos
            sucessor = self.no_mais_a_esq(no.dir)
            no.valor = sucessor.valor
            no.dir = self._deletar(no.dir, sucessor.valor)

        if no is None:
            return no

        return self.rebalancear(no)

    def no_mais_a_esq(self, no):
        atual = no
        while atual.esq is not None:
            atual = atual.esq
        return atual

    def buscar(self, valor):
        """Interface pública para a busca."""
        return self._buscar(self.raiz, valor)

    def _buscar(self, no, valor):
        """Função recursiva que realiza a busca."""
        if no is None:
            return False 
        
        if valor == no.valor:
            return True
        elif valor < no.valor:
            return self._buscar(no.esq, valor)
        else:
            return self._buscar(no.dir, valor)

    def em_ordem(self, no):
        """Retorna uma lista com os valores em ordem."""
        if no is not None:
            return self.em_ordem(no.esq) + [no.valor] + self.em_ordem(no.dir)
        return []

    def pre_ordem(self, no):
        """Retorna uma lista com os valores em pré-ordem."""
        if no is not None:
            return [no.valor] + self.pre_ordem(no.esq) + self.pre_ordem(no.dir)
        return []

    def pos_ordem(self, no):
        """Retorna uma lista com os valores em pós-ordem."""
        if no is not None:
            return self.pos_ordem(no.esq) + self.pos_ordem(no.dir) + [no.valor]
        return []


avl = AVL()
chaves = [10, 20, 30, 40, 50, 25]
print(f"Inserindo chaves: {chaves}")

for chave in chaves:
    avl.inserir(chave)

print("\n--- PERCURSOS APÓS INSERÇÃO ---")
print("Em Ordem (valores ordenados):", avl.em_ordem(avl.raiz))
print("Pré-Ordem (Raiz, Esq, Dir):", avl.pre_ordem(avl.raiz))
print("Pós-Ordem (Esq, Dir, Raiz):", avl.pos_ordem(avl.raiz))

print("\n--- BUSCANDO VALORES ---")
print("Buscando valor 30:", "Encontrado" if avl.buscar(30) else "Não Encontrado")
print("Buscando valor 99:", "Encontrado" if avl.buscar(99) else "Não Encontrado")

print("\n--- DELETANDO VALOR 30 ---")
avl.deletar(30)
print("Pré-Ordem após deletar 30:", avl.pre_ordem(avl.raiz))
