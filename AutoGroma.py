#!/usr/bin/env python
# coding: utf-8

# In[2]:


import subprocess
import sys
import os
from subprocess import Popen


# Em muitas partes do programa irei usar de prints caso ocorra erro para rodar alguma parte, sendo assim é econômico criar uma função que print já o formato do erro que eu quero que apareça na tela.

# In[3]:


def ERRO(E):
    print('----------------------------------------------------')
    print(E)
    print('----------------------------------------------------')
    return


# A primeira parte consiste em verificar se o sistema gromacs foi instalado corretamente, isso é feita chamando o gromacs através do comando gmx, caso o comando retornee um erro o código é interrompido. 

# In[5]:


if 'win' in sys.platform: #Parte destinada ao windows
    try:
        c1 = os.system('gmx')
        with open('processo.txt','w') as arquivo:
            arquivo.write(' 1) Verificação do Gromacs: Concluida')
    except Exception as E:
        print( 'Verificamos um erro ao tentar rodar o Gromacs, verifique se o mesmo se encontra instalado')
        ERRO(E)
        with open('processo.txt','w') as arquivo:
            arquivo.write(' 1) Verificação do Gromacs: Falha')
        exit()
else: #Parte para Linux é apenas uma cópia da parte destinada a windowns, mas que não tem o shell
    try:
        c1 = os.system('gmx')
        with open('processo.txt','w') as arquivo:
            arquivo.write(' 1) Verificação do Gromacs: Concluida')
    except Exception as E:
        print( 'Verificamos um erro ao tentar rodar o Gromacs, verifique se o mesmo se encontra instalado')
        ERRO(E)
        with open('processo.txt','w') as arquivo:
            arquivo.write(' 1) Verificação do Gromacs: Falha')
        exit()
os.system('clear')


# Antes de mais nada é necessário saber qual o nome do arquivo pdb que iremos usar, logo é preciso pedir para o usuário inserir o nome do arquivo que será feita a simulação, e é necessário o usuário informar se a estrutura é ou não uma proteína, para que assim possamos prosseguir com a simulação.

# In[ ]:


print('Para que a simulação se inicie, é necessário sabermos o nome do arquivo PDB que será simulado, por favor insirá o nome abaixo, sem a extensão pdb')
nome_ar = input()
nomeR = nome_ar + '.pdb'
nome_novo = nome_ar + '_' + 'clean'+'.pdb'
print('Para que possamos continuar, é necessário entender que essa simulação é para proteínas em soluto, deseja continuar?')
print('a) Sim, a estrutura é uma proteína')
print('b) Não, interrompa o processo pois não estou simulando uma proteína')
cont_simula = input()
if cont_simula in ['a','b']:
    if cont_simula == 'a':
        print('(: a simulação irá prosseguir, obrigado :)')
    if cont_simula == 'b':
        print('): a simulação não irá prosseguir, desculpe :(')
        exit()
else:
    print('a resposta dada não esta dentro das opções :\, vamos interromper a simulação')
    print('até a próxima ;-;')
    exit()


# Após a verificação da existência do Gromacs, precisamos verificar com o usuário se é necessário retirar as moléculas de água do arquivo pdb

# In[ ]:


#print('Agora é necessário informar se a estrutura contém água em sua composição ou não')
print(f'O arquivo contém água? \n a) sim\n b) não')
HOH_resposta = input()
if cont_simula in ['a','b']:
    if HOH_resposta == 'a':
        print('-_- Estamos retirando a água aguarde... -_-')
        if 'win' in sys.platform: #Parte destinada ao windows
            try:
                c2 = os.system(f'grep -v HOH {nomeR} > {nome_novo}')  #concertar essa parte ele não entende como um comando
                with open('processo.txt','a') as arquivo:
                    arquivo.write(f'\n 2) Retirada das moléculas de água')
                    arquivo.write(f'\n -  Criação de um novo arquivo chamado {nome_novo}')
            except Exception as E:
                print('Não foi possivel retirar as águas, devido a falha >:(')
                ERRO(E)
                with open('processo.txt','a') as arquivo:
                    arquivo.write(f'\n 2) Retirada das moléculas de água não foi executada')
                    arquivo.write(f'\n -  Nenhum arquivo foi criado')
                    exit()
        else: #Parte para Linux
            try:
                c2 = os.system(f'grep -v HOH {nomeR} > {nome_novo}') 
                with open('processo.txt','a') as arquivo:
                    arquivo.write(f'\n 2) Retirada das moléculas de água')
                    arquivo.write(f'\n -  Criação de um novo arquivo chamado {nome_novo}')
            except Exception as E:
                print('Não foi possivel retirar as águas, devido a falha >:(')
                ERRO(E)
                with open('processo.txt','a') as arquivo:
                    arquivo.write(f'\n 2) Retirada das moléculas de água não foi executada')
                    arquivo.write(f'\n -  Nenhum arquivo foi criado')
                    exit()
    if HOH_resposta == 'b':
        nome_novo = nomeR
        print('(:(:(: Adiantou nosso trabalho :):):)')
else:
    print('a resposta dada não esta dentro das opções :\, vamos interromper a simulação')
    print('até a próxima ;-;')
    exit()


# Vamos criar a topologia do sistema estudado, para isso usamos praticamente as mesmas linhas de comandos anteriormente, 

# In[ ]:


print('criando topologia >:(')
if 'win' in sys.platform:#Parte destidana ao windows
    try:
        c3 = os.system(f'gmx pdb2gmx -f {nome_novo} -o {nome_ar}_processed.gro -water spce')
        with open('processo.txt','a') as arquivo:
            arquivo.write(f'\n 3) Criação da topologia da estrutura {nome_novo} \n Criação dos arquivos: \n {nome_ar}_processed.gro \n posre.itp \n topol.top ')
    except Exception as E:
        print(';-; Não foi possivel gerar a topologia da estrutura devido a erros ;-;')
        ERRO(E)
        with open('processo.txt', 'a') as arquivo:
            arquivo.write(f'\n 3) Erro ao escrever a topologia do sistema')
else:#Parte destinada ao  Linux
    try:
        c3 = os.system(f'gmx pdb2gmx -f {nome_novo} -o {nome_ar}_processed.gro -water spce')
        with open('processo.txt','a') as arquivo:
            arquivo.write(f'\n 3) Criação da topologia da estrutura {nome_novo} \n Criação dos arquivos: \n {nome_ar}_processed.gro \n posre.itp \n topol.top ')
    except Exception as E:
        print(';-; Não foi possivel gerar a topologia da estrutura devido a erros ;-;')
        ERRO(E)
        with open('processo.txt', 'a') as arquivo:
            arquivo.write(f'\n 3) Erro ao escrever a topologia do sistema')


# Com a topologia criada, verifique os arquivos que foram criados, agora iremos definir a caixa que conterá o solvente
# 

# In[ ]:


print('(: Vamos definir a caixa de simulação :)')
if 'win' in sys.platform: #Parte do Windows
    try:
        c4 = os.system(f'gmx editconf -f {nome_ar}_processed.gro -o {nome_ar}_newbox.gro -c -d 1.0 -bt cubic')
        with open('processo.txt','a') as arquivo:
            arquivo.write(f'\n 4) Criação da caixa onde ocorrerá a simulação')
    except Exception as E:
        print('Encontramos um erro ao definir a caixa da simulação')
        ERRO(E)
        with open('processo.txt', 'a') as arquivo:
            arquivo.write(f'\n 4) Erro ao definir a caixa de simulação')
else: #Parte para o Linux
    try:
        c4 = os.system(f'gmx editconf -f {nome_ar}_processed.gro -o {nome_ar}_newbox.gro -c -d 1.0 -bt cubic')
        with open('processo.txt','a') as arquivo:
            arquivo.write(f'\n 4) Criação da caixa onde ocorrerá a simulação')
    except Exception as E:
        print('Encontramos um erro ao definir a caixa da simulação')
        ERRO(E)
        with open('processo.txt', 'a') as arquivo:
            arquivo.write(f'\n 4) Erro ao definir a caixa de simulação')


# Adição das moléculas de água

# In[ ]:


print('):< Estamos colocando o solvente >:(')
if 'win' in sys.platform: #Parte do Windows
    try:
        c4 = os.system(f'gmx solvate -cp {nome_ar}_newbox.gro -cs spc216.gro -o {nome_ar}_solv.gro -p topol.top')
        with open('processo.txt','a') as arquivo:
            arquivo.write(f'\n 5) Inserimos o solvente')
    except Exception as E:
        print('Encontramos um erro ao inserir o solvente')
        ERRO(E)
        with open('processo.txt', 'a') as arquivo:
            arquivo.write(f'\n 5) Erro ao inserir o solvente')
else: #Parte para o Linux
    try:
        c4 = os.system(f'gmx solvate -cp {nome_ar}_newbox.gro -cs spc216.gro -o {nome_ar}_solv.gro -p topol.top')
        with open('processo.txt','a') as arquivo:
            arquivo.write(f'\n 5) Inserimos o solvente')
    except Exception as E:
        print('Encontramos um erro ao inserir o solvente')
        ERRO(E)
        with open('processo.txt', 'a') as arquivo:
            arquivo.write(f'\n 5) Erro ao inserir o solvente')


# Agora vamos ionizar o sistema:

# In[ ]:


print('criação do arquivo ions.mdp')
with open('ions.mdp', 'a') as arquivo1:
    arquivo1.write(f'; ions.mdp - used as input into grompp to generate ions.tpr\n; Parameters describing what to do, when to stop and what to save\nintegrator  = steep         ; Algorithm (steep = steepest descent minimization)\nemtol       = 1000.0        ; Stop minimization when the maximum force < 1000.0 kJ/mol/nm\nemstep      = 0.01          ; Minimization step size\nnsteps      = 50000         ; Maximum number of (minimization) steps to perform\n; Parameters describing how to find the neighbors of each atom and how to calculate the interactions\nnstlist         = 1         ; Frequency to update the neighbor list and long range forces\ncutoff-scheme	= Verlet    ; Buffered neighbor searching\nns_type         = grid      ; Method to determine neighbor list (simple, grid)\ncoulombtype     = cutoff    ; Treatment of long range electrostatic interactions\nrcoulomb        = 1.0       ; Short-range electrostatic cut-off\nrvdw            = 1.0       ; Short-range Van der Waals cut-off\npbc             = xyz       ; Periodic Boundary Conditions in all 3 dimensions')
with open('processo.txt', 'a') as arquivo:
    arquivo.write(f'Escrita do arquivo de texto ions.mdp para usar na adição de ions')


# In[ ]:


if 'win' in sys.platform: #Parte do Windows
    try:
        c4 = os.system(f'gmx grompp -f ions.mdp -c {nome_ar}_solv.gro -p topol.top -o ions.tpr')
        with open('processo.txt','a') as arquivo:
            arquivo.write(f'\n 6) Escrita do arquivo .tpr')
    except Exception as E:
        print('Encontramos um erro ao escrever o arquivo .tpr')
        ERRO(E)
        with open('processo.txt', 'a') as arquivo:
            arquivo.write(f'\n 6) Erro na escrita do arquivo .tpr')
else: #Parte para o Linux
    try:
        c4 = os.system(f'gmx grompp -f ions.mdp -c {nome_ar}_solv.gro -p topol.top -o ions.tpr')
        with open('processo.txt','a') as arquivo:
            arquivo.write(f'\n 6) Escrita do arquivo .tpr')
    except Exception as E:
        print('Encontramos um erro ao escrever o arquivo .tpr')
        ERRO(E)
        with open('processo.txt', 'a') as arquivo:
            arquivo.write(f'\n 6) Erro na escrita do arquivo .tpr')


# Uso do genion

# In[ ]:


if 'win' in sys.platform: #Parte do Windows
    try:
        c4 = os.system(f'gmx genion -s ions.tpr -o {nome_ar}_solv_ions.gro -p topol.top -pname NA -nname CL -neutral')
        with open('processo.txt','a') as arquivo:
            arquivo.write(f'\n 7) Uso do genion para adição de ions')
    except Exception as E:
        print('Encontramos um erro ao chamar o genion')
        ERRO(E)
        with open('processo.txt', 'a') as arquivo:
            arquivo.write(f'\n 7) Erro ao chamar o genion')
else: #Parte para o Linux
    try:
        c4 = os.system(f'gmx genion -s ions.tpr -o {nome_ar}_solv_ions.gro -p topol.top -pname NA -nname CL -neutral')
        with open('processo.txt','a') as arquivo:
            arquivo.write(f'\n 7) Uso do genion para adição de ions')
    except Exception as E:
        print('Encontramos um erro ao chamar o genion')
        ERRO(E)
        with open('processo.txt', 'a') as arquivo:
            arquivo.write(f'\n 7) Erro ao chamar o genion')

