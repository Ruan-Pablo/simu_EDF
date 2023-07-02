
import time



###
#  coisas necessárias para esse EDF 
#  array de cada thread vai possui[periodo, custo, deadline relativa, proximo_periodo, quanto de custo ainda falta, deadline_absoluto]
#  Funcionamento: o "escalonador" ira escolher no inicio de cada tempo, a thread com a deadline mais proxima e
#  tentar executar ela até seu fim ou até o inicio do periodo de outra thread na qual a deadline esteja proxima, 
#  caso a thread termine todo seu custo, a deadline absoluta aumenta a quantidade da relativa e aguarda o inicio do proximo periodo para poder reiniciar o custo.
#  caso nenhum periodo tenha começado, o processador ficara INATIVO  ###

def EDF(threads:list[dict]):
    mmc = MMC(threads) #reinicio de ciclos
    print(f'tempo de reinicio de ciclo: {mmc}')

    tempo_atual = 0
    while(tempo_atual!= mmc+1):
        print(f'tempo atual:{tempo_atual}')
        thread = encontrar_thread(threads)
        if(thread!=None):
            if(thread['deadline_absoluta']<tempo_atual):
                print(f'Thread{thread["nome"]} passou da deadline')
                break
            else:
                executar(thread)
            pass
        else:
            print('Nenhuma Tarefa executando, processador inativo')
            time.sleep(0.5)

        tempo_atual +=1


        #checa se é inicio de algum periodo
        atualizar_custos(threads,tempo_atual)


def MMC(threads:list):
    valores = []
    for thread in threads:
        valores.append(thread['periodo'])


    maxin = max(valores)
    mmc = maxin
    print(valores)

    while( True ):
        if(mmc%valores[0]==0 and mmc%valores[1]==0 and mmc%valores[2]==0):
            break
        mmc+=maxin
        print(mmc)
        time.sleep(0.5)

    return mmc
    

def encontrar_thread(threads:list[dict]):
    thread_encontrada = None
    for thread in threads:
        if(thread['custo_restante'] !=0 ):
            if(thread_encontrada == None or thread['deadline_absoluta'] < thread_encontrada['deadline_absoluta'] or (thread['deadline_absoluta'] == thread_encontrada['deadline_absoluta'] and thread['custo_restante']<thread['custo'])):    
                 thread_encontrada = thread


    return thread_encontrada

def atualizar_custos(threads:list[dict],tempo_atual:int):
    for thread in threads:
        if(thread['prox_periodo'] == tempo_atual and thread['custo_restante']==0): 
            thread['custo_restante'] = thread['custo']
            thread['prox_periodo'] += thread['periodo'] 

def executar(thread:dict):
    


    thread['custo_restante'] -= 1
    print(f'executando tarefa {thread["nome"]} custo restante : {thread["custo_restante"]} / {thread["custo"]}')

    if(thread['custo_restante'] == 0):
        thread['deadline_absoluta'] += thread['deadline_relativa']

    time.sleep(0.5)




a = open('Parte1-SistemasTestes\sistema4.txt','r')
modes = a.readline().strip('\n').split('\t')
threads = []
i = 1 
for line in a:
    threads.append([i]+line.strip('\n').split('\t'))
    i+=1
    
print(threads,modes)

in_dic = []
for thread in threads:
    label = {
        'nome':int(thread[0]),
        'periodo':int(thread[1]),
        'custo':int(thread[2]),
        'deadline_relativa':int(thread[3]),
        'prox_periodo':int(thread[1]),
        'custo_restante':int(thread[2]),
        'deadline_absoluta':int(thread[3])
    }
    in_dic.append(label)

print(in_dic)

EDF(in_dic)