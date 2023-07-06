
import time
###
#  coisas necessárias para esse EDF 
#  array de cada tarefa vai possui[periodo, custo, deadline relativa, proximo_periodo, quanto de custo ainda falta, deadline_absoluto]
#  Funcionamento: o "escalonador" ira escolher no inicio de cada tempo, a tarefa com a deadline mais proxima e
#  tentar executar ela até seu fim ou até o inicio do periodo de outra tarefa na qual a deadline esteja proxima, 
#  caso a tarefa termine todo seu custo, a deadline absoluta aumenta a quantidade da relativa e aguarda o inicio do proximo periodo para poder reiniciar o custo.
#  caso nenhum periodo tenha começado, o processador ficara INATIVO  ###

def EDF(tarefas:list[dict]):
    img = ['','','']
    mmc = MMC(tarefas) #reinicio de ciclos
    intax = 0.0
    print(f'tempo de reinicio de ciclo: {mmc}')

    tempo_atual = 0
    while(tempo_atual!= mmc):
        print(f'tempo atual:{tempo_atual}')
        tarefa = encontrar_tarefa(tarefas)
        if(tarefa!=None):
            if(tarefa['deadline_absoluta']<tempo_atual):
                print(f'Tarefa{tarefa["nome"]} passou da deadline')
                break
            else:
                executar(tarefa)
                if(tarefa["nome"] == 1):
                    img[0]+=("◼ ")
                    img[1]+=("◻ ")
                    img[2]+=("◻ ")

                elif(tarefa["nome"] == 2):
                    img[0]+=("◻ ")
                    img[1]+=("◼ ")
                    img[2]+=("◻ ")
                else:
                    img[0]+=("◻ ")
                    img[1]+=("◻ ")
                    img[2]+=("◼ ")
            
        else:
            print('Nenhuma Tarefa executando, processador inativo')
            img[0]+=("◻ ")
            img[1]+=("◻ ")
            img[2]+=("◻ ")
            intax+=1
            #time.sleep(0.25)

        tempo_atual +=1


        #checa se é inicio de algum periodo
        atualizar_custos(tarefas,tempo_atual)

   

    print(f'Taxa de utilização para um ciclo: {(1-(intax/mmc))*100}%')

    f = open("img.txt",'w',encoding='UTF-8')
    for imgs in img: 
       f.write(imgs+'\n')



def MMC(tarefas:list):
    valores = []
    for tarefa in tarefas:
        valores.append(tarefa['periodo'])


    maxin = max(valores)
    mmc = maxin
    print(valores)

    while( True ):
        if(mmc%valores[0]==0 and mmc%valores[1]==0 and mmc%valores[2]==0):
            break
        mmc+=maxin
        print(mmc)
        #time.sleep(0.25)

    return mmc
    

def encontrar_tarefa(tarefas:list[dict]):
    tarefa_encontrada = None
    for tarefa in tarefas:
        if(tarefa['custo_restante'] !=0 ):
            if(tarefa_encontrada == None or tarefa['deadline_absoluta'] < tarefa_encontrada['deadline_absoluta'] or (tarefa['deadline_absoluta'] == tarefa_encontrada['deadline_absoluta'] and tarefa['custo_restante']<tarefa['custo'])):    
                 tarefa_encontrada = tarefa


    return tarefa_encontrada

def atualizar_custos(tarefas:list[dict],tempo_atual:int):
    for tarefa in tarefas:
        if(tarefa['prox_periodo'] == tempo_atual and tarefa['custo_restante']==0): 
            tarefa['custo_restante'] = tarefa['custo']
            tarefa['prox_periodo'] += tarefa['periodo'] 

def executar(tarefa:dict):
    


    tarefa['custo_restante'] -= 1
    print(f'executando tarefa {tarefa["nome"]} custo restante : {tarefa["custo_restante"]} / {tarefa["custo"]}')

    if(tarefa['custo_restante'] == 0):
        tarefa['deadline_absoluta'] += tarefa['deadline_relativa']

    #time.sleep(0.25)


""" ----------------------------------------MAIN-----------------------------------------------------"""



a = open('Parte1-SistemasTestes\sistema3.txt','r')
modes = a.readline().strip('\n').split('\t')
tarefas = []
i = 1 
for line in a:
    tarefas.append([i]+line.strip('\n').split('\t'))
    i+=1
    
print(tarefas,modes)

in_dic = []
for tarefa in tarefas:
    label = {
        'nome':int(tarefa[0]),
        'periodo':int(tarefa[1]),
        'custo':int(tarefa[2]),
        'deadline_relativa':int(tarefa[3]),
        'prox_periodo':int(tarefa[1]),
        'custo_restante':int(tarefa[2]),
        'deadline_absoluta':int(tarefa[3])
    }
    in_dic.append(label)


taxa = 0.0
escalona = True
print(in_dic)
for tarefa in in_dic:
    taxa += (tarefa['custo']/tarefa['periodo'])

print(f'a taxa de utilização: {taxa}')
if(taxa<=1):
    print('Sistema é escalonavel')
else:
    print('Sistema provavelmente não é escalonavel')

input()

EDF(in_dic)
a.close()