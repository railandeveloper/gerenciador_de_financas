#controle de financas
import time
from modulo import exibir_menu, Financeiro, msg_de_sucesso, limpar_tela, msg_de_alerta


financeiro = Financeiro()

msg_de_sucesso('Bem vindo')
while True:
    exibir_menu()
    try:
        opcao_usuario = int(input(f'Digite sua opcao: '))
    except ValueError:
        msg_de_alerta("\033[91mErro: Digite um número inteiro válido.\033[0m")
        continue     
    

    if opcao_usuario == 1:
        financeiro.adicionar_divida()
        

    elif opcao_usuario == 2:
        financeiro.visualizar_dividas()
        
    
    elif opcao_usuario == 3:
        financeiro.pagar_uma_divida()
        
    elif opcao_usuario == 4:
        financeiro.editar_divida()    
        
    elif opcao_usuario == 5:
        limpar_tela()
    
    elif opcao_usuario == 6:
        msg_de_alerta('Fechando o programa...')  
        time.sleep(2)
        msg_de_sucesso('Ate breve! ')
        break
    else:
        msg_de_alerta('Opcao invalida')    
    
        
            
  