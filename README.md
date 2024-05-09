# SO-Disk-Simulator 

## QUESTÃO 2

Escreva um simulador de disco que permita indicar qual a latência de acesso para uma lista de blocos indicados como dados de entrada. Aqui o simulador deve receber uma configuração que inclua:

1. tamanho do setor
2. quantidade de trilhas no disco
3. quantidade de setores por trilha
4. tempo de seek, rotação e transferência de dados

O simulador deve incorporar um dos algoritmos de scheduling:

1. SSTF
2. SPTF
3. F-SCAN
4. C-SCAN
5. C-SCAN + anticipatory 

## Setup inicial

- `Python:` Linguagem utilizada no projeto.

```bash
python 3.9
```

- `Matplotlib:` Biblioteca de software para criação de gráficos e visualizações de dados.
- `Numpy:` Biblioteca para processamento de arranjos e matrizes grandes e multi-dimensionais.

```bash
pip install matplotlib numpy
```

## COMO EXECUTAR 

Altere os parâmetros do disco no config.ini. Uma lista de requests pode ser encontrada no arquivo main.py

```bash
python main.py
```

## DOCUMENTO DO PROJETO

- *[Documento](https://docs.google.com/document/d/1JHo7JTkJMtmudXlRcFw4E-dY8jndV9HFU2wjJ9msoEI/edit?usp=sharing)*
