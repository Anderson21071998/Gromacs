#!/usr/bin/env python
# coding: utf-8

# In[2]:

import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import pandas as pd
import subprocess
import sys
import os
from subprocess import Popen


# Em muitas partes do programa irei usar de prints caso ocorra erro para rodar alguma parte, sendo assim é econômico criar uma função que print já o formato do erro que eu quero que apareça na tela.

# In[1]:


def ERRO(E):
    print('----------------------------------------------------')
    print(E)
    print('----------------------------------------------------')
    return

def Grafico_ME(op):
    if op == "Po":
        print('Escolha a opção "10 0" para potencial')
        try:
            OPPo = os.system(f'gmx energy -f em.edr -o Potencial.xvg')
            Plot('Potencial.xvg', "Potencial do sistema.png")
            with open('processo.txt','a') as arquivo:
                arquivo.write(f'\n OPPo) Geração dos arquivos:\n Arquivo para plot de minimização de energia Potencial.xvg \n Arquivo com o plot em Potencial.png')
        except Exception as E:
            print('Encontramos um erro ao gerar os arquivos do Potêncial')
            ERRO(E)
            with open('processo.txt', 'a') as arquivo:
                arquivo.write(f'\n OPPo) Erro ao gerar os arquivos do Potêncial')
        return 1
    
    if op == "T":
        print('Escolha a opção "16 0" para temperatura')
        try:
            OPT = os.system(f'gmx energy -f nvt.edr -o temperatura.xvg')
            Plot('temperatura.xvg', "Temperatura do sistema.png")
            with open('processo.txt','a') as arquivo:
                arquivo.write(f'\n OPT) Geração dos arquivos:\n Arquivo para plot de minimização de energia temperatura.xvg \n Arquivo com o plot em Temperatura.png')
        except Exception as E:
            print('Encontramos um erro ao gerar o gráfico da minimização de energia')
            ERRO(E)
            with open('processo.txt', 'a') as arquivo:
                arquivo.write(f'\n OPT) Erro ao gerar o gráfico da minimização de energia')
        return 1
    if op == "P":
        print('Escolha a opção "18 0" para temperatura')
        try:
            OPP = os.system(f'gmx energy -f npt.edr -o pressão.xvg')
            Plot('pressão.xvg', "Pressão do sistema.png")
            with open('processo.txt','a') as arquivo:
                arquivo.write(f'\n OPP) Geração dos arquivos:\n Arquivo para plot de pressão Pressão.xvg \n Arquivo com o plot em Pressão.png')
        except Exception as E:
            print('Encontramos um erro ao gerar os arquivos de pressão')
            ERRO(E)
            with open('processo.txt', 'a') as arquivo:
                arquivo.write(f'\n OPP) Erro ao gerar os arquivos de Pressão')
        return 1
    if op == "D":
        print('Escolha a opção "24 0" para temperatura')
        try:
            OPP = os.system(f'gmx energy -f npt.edr -o Densidade.xvg')
            Plot('Densidade.xvg', "Densidade do sistema.png")
            with open('processo.txt','a') as arquivo:
                arquivo.write(f'\n OPD) Geração dos arquivos:\n Arquivo para plot da densidade Densidade.xvg \n Arquivo com o plot em Densidade.png')
        except Exception as E:
            print('Encontramos um erro ao gerar os arquivos de densidade')
            ERRO(E)
            with open('processo.txt', 'a') as arquivo:
                arquivo.write(f'\n OPD) Erro ao gerar os arquivos de densidade')
        return 1
    return 0

def Plot (arquivo, saida):
    #Essa função irá plotar os gráficos de saída
    arquivo = open(arquivo,"r")
    eixox, eixoy, nome_eixox, nome_eixoy= [], [], '', ''
    for linha in arquivo:
        valor = linha.split()
        if valor[0] in ['#','@'] and len(valor) > 1:
            if valor[1] in ['title','xaxis','yaxis']:
                if valor[1] == 'xaxis': nome_eixox = valor[3] + ' ' + valor[4]
                if valor[1] == 'yaxis': nome_eixoy = valor[3] + ' ' + valor[4]
        if valor[0] not in ['#','@','@TYPE']:
            eixox.append(float(valor[0]))
            eixoy.append(float(valor[1]))
    plt.plot(eixox, eixoy, color = 'black', )
    plt.xlabel(nome_eixox)
    plt.ylabel(nome_eixoy)
    plt.title(saida)
    plt.savefig(saida+'.png', format = 'png')


# A primeira parte consiste em verificar se o sistema gromacs foi instalado corretamente, isso é feita chamando o gromacs através do comando gmx, caso o comando retornee um erro o código é interrompido. 

# In[5]:


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
try:
    c3 = os.system(f'gmx pdb2gmx -f {nome_novo} -o {nome_ar}_processed.gro -water spce')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 3) Criação da topologia da estrutura {nome_novo} \n Criação dos arquivos: \n {nome_ar}_processed.gro \n posre.itp \n topol.top ')
except Exception as E:
    print(';-; Não foi possivel gerar a topologia da estrutura devido a erros ;-;')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 3) Erro ao escrever a topologia do sistema')
    exit()


# Com a topologia criada, verifique os arquivos que foram criados, agora iremos definir a caixa que conterá o solvente
# 

# In[ ]:


print('(: Vamos definir a caixa de simulação :)')
try:
    c4 = os.system(f'gmx editconf -f {nome_ar}_processed.gro -o {nome_ar}_newbox.gro -c -d 1.0 -bt cubic')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 4) Criação da caixa onde ocorrerá a simulação \n Escrita do arquivo {nome_ar}_newbox.gro')
except Exception as E:
    print('Encontramos um erro ao definir a caixa da simulação')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 4) Erro ao definir a caixa de simulação')
    exit()


# Adição das moléculas de água

# In[ ]:


print('):< Estamos colocando o solvente >:(')
try:
    c5 = os.system(f'gmx solvate -cp {nome_ar}_newbox.gro -cs spc216.gro -o {nome_ar}_solv.gro -p topol.top')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 5) Inserimos o solvente \n Escrita dos arquivos:\n {nome_ar}_solv.gro')
except Exception as E:
    print('Encontramos um erro ao inserir o solvente')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 5) Erro ao inserir o solvente')
    exit()


# Agora vamos ionizar o sistema:

# In[ ]:


print('criação do arquivo ions.mdp') #50000 
with open('ions.mdp', 'a') as arquivo1:
    arquivo1.write(f'; ions.mdp - used as input into grompp to generate ions.tpr\n; Parameters describing what to do, when to stop and what to save\nintegrator  = steep         ; Algorithm (steep = steepest descent minimization)\nemtol       = 1000.0        ; Stop minimization when the maximum force < 1000.0 kJ/mol/nm\nemstep      = 0.01          ; Minimization step size\nnsteps      = 50000        ; Maximum number of (minimization) steps to perform\n; Parameters describing how to find the neighbors of each atom and how to calculate the interactions\nnstlist         = 1         ; Frequency to update the neighbor list and long range forces\ncutoff-scheme	= Verlet    ; Buffered neighbor searching\nns_type         = grid      ; Method to determine neighbor list (simple, grid)\ncoulombtype     = cutoff    ; Treatment of long range electrostatic interactions\nrcoulomb        = 1.0       ; Short-range electrostatic cut-off\nrvdw            = 1.0       ; Short-range Van der Waals cut-off\npbc             = xyz       ; Periodic Boundary Conditions in all 3 dimensions')
with open('processo.txt', 'a') as arquivo:
    arquivo.write(f'\n Escrita do arquivo de texto ions.mdp para usar na adição de ions')


# In[ ]:


try:
    c6 = os.system(f'gmx grompp -f ions.mdp -c {nome_ar}_solv.gro -p topol.top -o ions.tpr')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 6) Escrita do arquivo ions.tpr')
except Exception as E:
    print('Encontramos um erro ao escrever o arquivo ions.tpr')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 6) Erro na escrita do arquivo ions.tpr')
    exit()


# Uso do genion

# In[ ]:


try:
    c7 = os.system(f'gmx genion -s ions.tpr -o {nome_ar}_solv_ions.gro -p topol.top -pname NA -nname CL -neutral')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 7) Uso do genion para adição de ions')
except Exception as E:
    print('Encontramos um erro ao chamar o genion')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 7) Erro ao chamar o genion')
    exit()


# Agora a parte de minimização da proteina

# In[ ]:


print('Criação do arquivo minim.mdp') #50000
with open('minim.mdp', 'a') as arquivo1:
    arquivo1.write(f'; minim.mdp - used as input into grompp to generate em.tpr\n; Parameters describing what to do, when to stop and what to save\nintegrator  = steep         ; Algorithm (steep = steepest descent minimization)\nemtol       = 1000.0        ; Stop minimization when the maximum force < 1000.0 kJ/mol/nm\nemstep      = 0.01          ; Minimization step size\nnsteps      = 50000        ; Maximum number of (minimization) steps to perform\n\n; Parameters describing how to find the neighbors of each atom and how to calculate the interactions\nnstlist         = 1         ; Frequency to update the neighbor list and long range forces\ncutoff-scheme   = Verlet    ; Buffered neighbor searching\nns_type         = grid      ; Method to determine neighbor list (simple, grid)\ncoulombtype     = PME       ; Treatment of long range electrostatic interactions\nrcoulomb        = 1.0       ; Short-range electrostatic cut-off\nrvdw            = 1.0       ; Short-range Van der Waals cut-off\npbc             = xyz       ; Periodic Boundary Conditions in all 3 dimensions')
with open('processo.txt', 'a') as arquivo:
    arquivo.write(f'\n Escrita do arquivo de texto minim.mdp para usar na minimização de energia')


# In[ ]:


try:
    c8 = os.system(f'gmx grompp -f minim.mdp -c {nome_ar}_solv_ions.gro -p topol.top -o em.tpr')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 8) Criação do arquivo que contém as informações dos átomo para minimização')
except Exception as E:
    print('Encontramos um erro ao gerar o arquivo .tpr da minimização')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 8) Erro ao gerar o arquivo .tpr da minimização')
    exit()


# In[ ]:


try:
    c9 = os.system(f'gmx mdrun -v -deffnm em')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 9) Processo de minimização de energia, geração dos seguintes arquivos:\n em.log\n em.edr\n em.trr\n em.gro')
except Exception as E:
    print('Encontramos um erro executar a minimização de energia')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 9) Erro ao executar a minimização de energia')
    exit()


# In[16]:


choice1 = 1
while choice1 == 1:
    print('Você deseja gerar um arquivo para produzir o gráfico de Energia por tempo de simulação?\n a) Sim \n b) Não')
    escolha1 = input()
    if escolha1 in ['a','b']:
        if escolha1 == 'a':
            Grafico_ME('PO')
            choice1 = 0
        else:
            print('Continuaremos com a simulação')
            choice1 = 0
    else:
        print('Insira uma resposta entre as opções dadas, coloque "a" ou "b"')            


# Essa parte é responsavel por equilibrar o sistema em temperatura e pressão, antes de executar a simulação própriamente dita.

# In[ ]:


print('Criação do arquivo nvt.mdp')
with open('nvt.mdp', 'a') as arquivo1:
    arquivo1.write(f'title                   = OPLS Lysozyme NVT equilibration\ndefine                  = -DPOSRES  ; position restrain the protein\n; Run parameters\nintegrator              = md        ; leap-frog integrator\nnsteps                  = 50000     ; 2 * 50000 = 100 ps\ndt                      = 0.002     ; 2 fs\n; Output control\nnstxout                 = 500       ; save coordinates every 1.0 ps\nnstvout                 = 500       ; save velocities every 1.0 ps\nnstenergy               = 500       ; save energies every 1.0 ps\nnstlog                  = 500       ; update log file every 1.0 ps\n; Bond parameters\ncontinuation            = no        ; first dynamics run\nconstraint_algorithm    = lincs     ; holonomic constraints \nconstraints             = h-bonds   ; bonds involving H are constrained\nlincs_iter              = 1         ; accuracy of LINCS\nlincs_order             = 4         ; also related to accuracy\n; Nonbonded settings \ncutoff-scheme           = Verlet    ; Buffered neighbor searching\nns_type                 = grid      ; search neighboring grid cells\nnstlist                 = 10        ; 20 fs, largely irrelevant with Verlet\nrcoulomb                = 1.0       ; short-range electrostatic cutoff (in nm)\nrvdw                    = 1.0       ; short-range van der Waals cutoff (in nm)\nDispCorr                = EnerPres  ; account for cut-off vdW scheme\n; Electrostatics\ncoulombtype             = PME       ; Particle Mesh Ewald for long-range electrostatics\npme_order               = 4         ; cubic interpolation\nfourierspacing          = 0.16      ; grid spacing for FFT\n; Temperature coupling is on\ntcoupl                  = V-rescale             ; modified Berendsen thermostat\ntc-grps                 = Protein Non-Protein   ; two coupling groups - more accurate\ntau_t                   = 0.1     0.1           ; time constant, in ps\nref_t                   = 300     300           ; reference temperature, one for each group, in K\n; Pressure coupling is off\npcoupl                  = no        ; no pressure coupling in NVT\n; Periodic boundary conditions\npbc                     = xyz       ; 3-D PBC\n; Velocity generation\ngen_vel                 = yes       ; assign velocities from Maxwell distribution\ngen_temp                = 300       ; temperature for Maxwell distribution\ngen_seed                = -1        ; generate a random seed')
with open('processo.txt', 'a') as arquivo:
    arquivo.write(f'\n Escrita do arquivo de texto nvt.mdp para usar na equilibração como processo NVT ')


# In[ ]:


try:
    c10 = os.system(f'gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 10) Escrita do arquivo nvt.tpr para equilibração do sistema')
except Exception as E:
    print('Encontramos um erro ao escrever o arquivo nvt.tpr')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 10) Erro ao escrever o arquivo nvt.tpr')
    exit()


# In[ ]:


try:
    c11 = os.system(f'gmx mdrun -deffnm nvt')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 11) Equilibração do sistema através de um processo NVT')
except Exception as E:
    print('Encontramos um erro equilibrar o sistema através do processo NVT')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 11) Erro na equilibração através do processo NVT')
    exit()


# In[ ]:


choice2 = 0
while choice2 == 0:
    print('Você deseja gerar um arquivo para produzir o gráfico de Temperatura por tempo de simulação?\n a) Sim \n b) Não')
    escolha2 = input()
    if escolha2 in ['a','b']:
        if escolha2 == 'a':
            Grafico_ME('T')
            choice2 = 1
        else:
            print('Continuaremos com a simulação')
            choice2 = 1
    else:
        print('Insira uma resposta entre as opções dadas, coloque "a" ou "b"')


# In[ ]:





# In[ ]:


print('Criação do arquivo npt.mdp')
with open('npt.mdp', 'a') as arquivo1:
    arquivo1.write(f'title                   = OPLS Lysozyme NPT equilibration \ndefine                  = -DPOSRES  ; position restrain the protein\n; Run parameters\nintegrator              = md        ; leap-frog integrator\nnsteps                  = 50000     ; 2 * 50000 = 100 ps\ndt                      = 0.002     ; 2 fs\n; Output control\nnstxout                 = 500       ; save coordinates every 1.0 ps\nnstvout                 = 500       ; save velocities every 1.0 ps\nnstenergy               = 500       ; save energies every 1.0 ps\nnstlog                  = 500       ; update log file every 1.0 ps\n; Bond parameters\ncontinuation            = yes       ; Restarting after NVT \nconstraint_algorithm    = lincs     ; holonomic constraints \nconstraints             = h-bonds   ; bonds involving H are constrained\nlincs_iter              = 1         ; accuracy of LINCS\nlincs_order             = 4         ; also related to accuracy\n; Nonbonded settings \ncutoff-scheme           = Verlet    ; Buffered neighbor searching\nns_type                 = grid      ; search neighboring grid cells\nnstlist                 = 10        ; 20 fs, largely irrelevant with Verlet scheme\nrcoulomb                = 1.0       ; short-range electrostatic cutoff (in nm)\nrvdw                    = 1.0       ; short-range van der Waals cutoff (in nm)\nDispCorr                = EnerPres  ; account for cut-off vdW scheme\n; Electrostatics\ncoulombtype             = PME       ; Particle Mesh Ewald for long-range electrostatics\npme_order               = 4         ; cubic interpolation\nfourierspacing          = 0.16      ; grid spacing for FFT\n; Temperature coupling is on\ntcoupl                  = V-rescale             ; modified Berendsen thermostat\ntc-grps                 = Protein Non-Protein   ; two coupling groups - more accurate\ntau_t                   = 0.1     0.1           ; time constant, in ps\nref_t                   = 300     300           ; reference temperature, one for each group, in K\n; Pressure coupling is on\npcoupl                  = Parrinello-Rahman     ; Pressure coupling on in NPT\npcoupltype              = isotropic             ; uniform scaling of box vectors\ntau_p                   = 2.0                   ; time constant, in ps\nref_p                   = 1.0                   ; reference pressure, in bar\ncompressibility         = 4.5e-5                ; isothermal compressibility of water, bar^-1\nrefcoord_scaling        = com\n; Periodic boundary conditions\npbc                     = xyz       ; 3-D PBC\n; Velocity generation\ngen_vel                 = no        ; Velocity generation is off ')
with open('processo.txt', 'a') as arquivo:
    arquivo.write(f'\n Escrita do arquivo de texto npt.mdp para usar na equilibração como processo NPT ')


# In[ ]:


try:
    c12 = os.system(f'gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 12) Escrita do arquivo npt.tpr para equilibração do sistema')
except Exception as E:
    print('Encontramos um erro ao escrever o arquivo npt.tpr')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 12) Erro ao escrever o arquivo npt.tpr')
    exit()


# In[ ]:


try:
    c13 = os.system(f'gmx mdrun -deffnm npt')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 13) Equilibração do sistema através de um processo NPT')
except Exception as E:
    print('Encontramos um erro equilibrar o sistema através do processo NPT')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 13) Erro na equilibração através do processo NPT')
    exit()


# In[18]:


choice3 = 0
while choice3 == 0:
    print('Você deseja gerar um arquivo para produzir o gráfico de Energia por tempo de simulação?\n a) Sim \n b) Não')
    escolha3 = input()
    if escolha3 in ['a','b']:
        if escolha3 == 'a':
            Grafico_ME('P')
            choice3 = 1
        else:
            print('Continuaremos com a simulação')
            choice3 = 1
    else:
        print('Insira uma resposta entre as opções dadas, coloque "a" ou "b"')


# In[ ]:


choice4 = 0
while choice4 == 0:
    print('Você deseja gerar um arquivo para produzir o gráfico de Densidade por tempo de simulação?\n a) Sim \n b) Não')
    escolha4 = input()
    if escolha4 in ['a','b']:
        if escolha4 == 'a':
            Grafico_ME('D')
            choice4 = 1
        else:
            print('Continuaremos com a simulação')
            choice4 = 1
    else:
        print('Insira uma resposta entre as opções dadas, coloque "a" ou "b"')


# In[ ]:


print('Criação do arquivo md.mdp')
with open('md.mdp', 'a') as arquivo1:
    arquivo1.write(f'title                   = OPLS Lysozyme NPT equilibration \n; Run parameters\nintegrator              = md        ; leap-frog integrator\nnsteps                  = 500000    ; 2 * 500000 = 1000 ps (1 ns)\ndt                      = 0.002     ; 2 fs\n; Output control\nnstxout                 = 0         ; suppress bulky .trr file by specifying \nnstvout                 = 0         ; 0 for output frequency of nstxout,\nnstfout                 = 0         ; nstvout, and nstfout\nnstenergy               = 5000      ; save energies every 10.0 ps\nnstlog                  = 5000      ; update log file every 10.0 ps\nnstxout-compressed      = 5000      ; save compressed coordinates every 10.0 ps\ncompressed-x-grps       = System    ; save the whole system\n; Bond parameters\ncontinuation            = yes       ; Restarting after NPT \nconstraint_algorithm    = lincs     ; holonomic constraints \nconstraints             = h-bonds   ; bonds involving H are constrained\nlincs_iter              = 1         ; accuracy of LINCS\nlincs_order             = 4         ; also related to accuracy\n; Neighborsearching\ncutoff-scheme           = Verlet    ; Buffered neighbor searching\nns_type                 = grid      ; search neighboring grid cells\nnstlist                 = 10        ; 20 fs, largely irrelevant with Verlet scheme\nrcoulomb                = 1.0       ; short-range electrostatic cutoff (in nm)\nrvdw                    = 1.0       ; short-range van der Waals cutoff (in nm)\n; Electrostatics\ncoulombtype             = PME       ; Particle Mesh Ewald for long-range electrostatics\npme_order               = 4         ; cubic interpolation\nfourierspacing          = 0.16      ; grid spacing for FFT\n; Temperature coupling is on\ntcoupl                  = V-rescale             ; modified Berendsen thermostat\ntc-grps                 = Protein Non-Protein   ; two coupling groups - more accurate\ntau_t                   = 0.1     0.1           ; time constant, in ps\nref_t                   = 300     300           ; reference temperature, one for each group, in K\n; Pressure coupling is on\npcoupl                  = Parrinello-Rahman     ; Pressure coupling on in NPT\npcoupltype              = isotropic             ; uniform scaling of box vectors\ntau_p                   = 2.0                   ; time constant, in ps\nref_p                   = 1.0                   ; reference pressure, in bar\ncompressibility         = 4.5e-5                ; isothermal compressibility of water, bar^-1\n; Periodic boundary conditions\npbc                     = xyz       ; 3-D PBC\n; Dispersion correction\nDispCorr                = EnerPres  ; account for cut-off vdW scheme\n; Velocity generation\ngen_vel                 = no        ; Velocity generation is off ')
with open('processo.txt', 'a') as arquivo:
    arquivo.write(f'\n Escrita do arquivo de texto md.mdp para rodar a simulação ')


# In[ ]:


try:
    c14 = os.system(f'gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_0_1.tpr')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 14) Escrita do arquivo md_0_1.tpr para simulação')
except Exception as E:
    print('Encontramos um erro ao escrever o arquivo md_0_1.tpr')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 14) Erro ao escrever o arquivo md_0_1.tpr')
    exit()


# In[ ]:


try:
    c15 = os.system(f'gmx mdrun -deffnm md_0_1')
    with open('processo.txt','a') as arquivo:
        arquivo.write(f'\n 15) Execução da simulação')
except Exception as E:
    print('Erro ao executar a simulação')
    ERRO(E)
    with open('processo.txt', 'a') as arquivo:
        arquivo.write(f'\n 15) Erro na Erro na simulação')
    exit()

