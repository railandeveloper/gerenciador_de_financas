import os
import time
import json
from conexao import conexao


class Dividas():
    def __init__(self, nome_credor, valor_da_divida):
        self.nome_credor = nome_credor
        self.valor_da_divida = valor_da_divida
        
        
        
  # definindo como o objeto sera exibido
    def __str__(self):
        return f"Credor: {self.nome_credor.title()} |  Valor da Divida: R${self.valor_da_divida:.2f}"    


def calcular_divida_total():
    cursor = conexao.cursor()
    cursor.execute('SELECT SUM(valor_divida) FROM dividas')
    resultado = cursor.fetchone()
    valor_total = resultado[0]
    return valor_total

def buscar_todas_dividas():
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM dividas')
    return cursor.fetchall()



class Financeiro():
       
    #metodo para adicionar uma divida    
    def adicionar_divida(self):  
        cursor = conexao.cursor()
        while True:
            msg_cinza('Digite os dados da Divida: ')
            nome_credor = str(input(f'Qual o nome do seu credor(pessoa ou instituicao que voce deve)?: ')).strip()
            if nome_credor:
                break
            else:
                msg_de_alerta(f'o nome nao credor nao pode ser vazio')
                    
        while True:
            try:  
                valor_da_divida = float(input(f'Quanto voce deve para {nome_credor}?: '))
                if valor_da_divida > 0:
                    break
                else:
                    msg_de_alerta(f'o valor deve ser um numero positivo')    
            except ValueError:
                exibir_erro(f'o valor da divida deve conter apenas numeros e nao pode ser vazio')
                continue
        nova_divida = Dividas(nome_credor, valor_da_divida)#cria um objeto
        cursor.execute('INSERT INTO dividas (nome_credor, valor_divida) VALUES (%s, %s)', (nome_credor, valor_da_divida))
        msg_de_alerta('salvando divida...')
        conexao.commit()
        cursor.close()
        time.sleep(2)
        msg_de_sucesso(F'Divida com {nova_divida.nome_credor} adicionada com sucesso')
    
        
    #metodo para visulizar dividas    
    def visualizar_dividas(self):
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM dividas')
        lista_de_dividas = cursor.fetchall()
        if not lista_de_dividas:
            msg_de_alerta('Nenhuma dívida cadastrada.')
            return
        
        msg_lilas('LISTA DE DIVIDAS')
        for id, nome_credor, valor_da_divida in lista_de_dividas:
            msg_de_alerta(f'ID: {id} | Nome: {nome_credor.capitalize()} | Valor Da Divida: {valor_da_divida}')
        msg_de_alerta(f'Divida TOTAL: R${calcular_divida_total()}')
        
         
    #metodo para pagar uma divida              
    def pagar_uma_divida(self):
        cursor = conexao.cursor()
        lista_de_dividas = buscar_todas_dividas()
        if not lista_de_dividas:
            msg_de_sucesso('Você não tem dívidas para pagar.')
            return
        
        self.visualizar_dividas()
        
        while True:    
            try:
                id_divida = int(input(f'Digite o indice correspondente a divida que vc deseja pagar: '))
            except ValueError:
                exibir_erro("\033[91mErro: Digite um número inteiro válido.\033[0m")
                continue
            
            id_encontrado = False   
            for id, nome_credor, valor_da_divida in lista_de_dividas:
                if id == id_divida:
                    id_encontrado = True
            
            if not id_encontrado:
                msg_de_alerta('Id não encontrado')
                continue
            
            if id_encontrado:        
                cursor.execute('SELECT * FROM dividas Where id_divida = %s', (id_divida,))
                divida_escolhida = cursor.fetchone()
                nome_divida = divida_escolhida[1]
                valor_divida = float(divida_escolhida[2])
                print(f'Divida a ser paga: ID: {divida_escolhida[0]} | Credor: {nome_divida.capitalize()} | valor: {valor_divida}')
                break
                               
        while True:
            try:
                valor_pago = float(input(f'quanto voce deseja pagar da divida com {divida_escolhida[1]} Valor da divida: {divida_escolhida[2]}  :  '))
                if valor_pago > 0:
                    break
                else:
                    exibir_erro('O valor do pagamento deve ser maior que 0')
            except ValueError:
                  exibir_erro("Erro: Digite um valor numérico válido.")  
                            
        if valor_pago >= valor_divida:
            valor_sobrando = valor_pago - valor_divida
            msg_de_alerta('Pagando dívida...')
            time.sleep(2)          
            msg_de_sucesso(
                f'Parabéns! Você quitou a dívida com {nome_divida}. '
                f'{"Valor sobrando: R$" + str(valor_sobrando) + " será estornado para sua conta." if valor_sobrando > 0 else f"Parabéns! Você quitou a dívida com {nome_divida}."}'
            )
            cursor.execute('DELETE FROM dividas WHERE id_divida = %s', (id_divida,))
            conexao.commit()
            cursor.close() 
        else:
              novo_valor = valor_divida - valor_pago
              cursor.execute('UPDATE dividas SET valor_divida = %s WHERE id_divida = %s', (novo_valor, id_divida))
              valor_divida -= valor_pago
              time.sleep(2)
              msg_de_alerta(f'Você pagou R${valor_pago:.2f}. Novo saldo da dívida com {nome_divida}: R${valor_divida:.2f}')
              conexao.commit()
              cursor.close()
               
        msg_de_alerta(f'\nDívida total atualizada: R${calcular_divida_total()}\n')       
        
 
            
    def editar_divida(self):
        cursor = conexao.cursor()
        lista_de_dividas = buscar_todas_dividas()
        if not lista_de_dividas:
            msg_de_alerta('nao ha dividas para serem editadas')
            return
        
        self.visualizar_dividas()
        while True:
           try: 
                id_divida_editada = int(input(f'qual o indice da divida que voce deseja editar?: '))
           except ValueError:
               exibir_erro('O indice deve ser um numero inteiro valido')
               continue
           
           id_encontrado = False
           for id, nome_credor, valor_da_divida in lista_de_dividas:
             if id == id_divida_editada:
                 id_encontrado = True
        
           if not id_encontrado:
                msg_de_alerta('Id não encontrado')
                continue
        
           if id_encontrado:        
                cursor.execute('SELECT * FROM dividas Where id_divida = %s', (id_divida_editada,))
                divida_escolhida = cursor.fetchone()
                break
           
        while True:
            escolha = str(input(f'Voce quer editar o nome ou o valor de {divida_escolhida}? (nome/valor/cancelar): ')).strip().lower()
            
            if escolha == 'nome':
                novo_nome = str(input(f'Digite o novo nome da divida : ')).strip()
                cursor.execute('UPDATE dividas SET nome_credor = %s WHERE id_divida = %s', (novo_nome, id_divida_editada))
                msg_de_sucesso('novo nome adicionado')
                conexao.commit()
                cursor.close()
                break
            
            elif escolha == 'valor':
                while True:
                    try:            
                        novo_valor = float(input(f'Digite o novo valor de {divida_escolhida} : '))
                        if novo_valor > 0:
                            valor_atualizado = float(divida_escolhida[2])
                            self.divida_total -= valor_atualizado
                            valor_atualizado = novo_valor
                            self.divida_total += float(novo_valor)
                            cursor.execute('UPDATE dividas SET valor_divida = %s WHERE id_divida = %s', (novo_valor, id_divida_editada))
                            conexao.commit()
                            cursor.close()
                            msg_de_alerta('novo valor adicionado' )
                            break
                        else:
                            exibir_erro('O valor da dívida deve ser maior que zero.')
                    except ValueError:
                        exibir_erro('O valor deve ser um número válido.')
                break    
            elif escolha == 'cancelar':
                msg_de_alerta('Edição cancelada.')
                return
    
            else:
                exibir_erro('Opção inválida! Escolha entre (nome/valor/cancelar).')
               
        msg_de_sucesso('Dados atualizados com sucesso')
        self.visualizar_dividas()                                  

             
def exibir_menu():    
    print()
    msg_azul('OPCOES:')
    print ()
    msg_azul('1-  Adicionar Dividas')
    msg_azul('2 - Visualizar dividas')
    msg_azul('3 - Pagar uma divida')
    msg_azul('4 - Editar uma divida(nome/valor)')
    msg_azul('5 - Limpar tela')
    msg_azul('6 - Fechar Programa')
    print()        



def limpar_tela():
    os.system('cls')


def exibir_erro(msg):
    print(f"\033[91m{msg}.\033[0m")  # Vermelho para erro

def msg_de_sucesso(msg):
    print(f"\033[92m{msg}\033[0m")  # Verde para sucesso

def msg_lilas(msg):
    print(f"\033[35m{msg}\033[0m")  # Lilás/roxo para mensagens especiais

def msg_azul(msg):
    print(f"\033[34m{msg}\033[0m")  # Azul escuro para destaque

def msg_de_alerta(msg):
    print(f"\033[93m{msg}\033[0m")  # Amarelo para alertas

def msg_cinza(msg):
    print(f"\033[90m{msg}\033[0m")  # Cinza para textos informativos

                