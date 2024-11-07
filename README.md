# Objetivo

O projeto pretende constituir uma oportunidade de experimentação das matérias expostas na unidade curricular, em particular a especificação de um modelo UML e respetiva tradução para um modelo relacional e a criação, o povoamento e a interrogação de BD utilizando a linguagem SQL.
# Método
## Trabalho em grupo

O trabalho deverá ser realizado em grupos de 2 ou 3 alunos registados via Moodle. São permitidos também grupos de 1 só aluno em casos especiais.

## Atividades

O projeto é constituído pelos 12 passos abaixo, sendo que o passo 6 é um ponto de controlo que requer a validação pelo docente das práticas.

    1. Constituição dos grupos;
    2. atribuição de um tema a cada grupo, baseado num dataset com dados reais;
    3. descrição do universo em causa;
    4. elaboração de um diagrama de classes UML correspondente;
    5. mapeamento do modelo de classes UML num modelo relacional;
    6. [wait]-> validação pelo docente das práticas;
    7. criação do esquema da BD no SGBD escolhido (pode ser em SQLite);
    8. povoamento da BD com a totalidade dos dados do dataset;
    9. elaboração de 10+ interrogações em SQL de complexidade variável, extraindo conteúdo relevante do dataset e ilustrando as técnicas de interrogação estudadas;
    10. construção de uma interface em Python com acesso à BD;
    11. escrita do relatório e entrega no Moodle até 2024-12-09;
    12. apresentação do trabalho na aula prática da semana de 2024-12-12/18.

# Resultado

Deverá entregar um relatório em formato Word ou PDF, podendo inspirar-se no modelo do documento disponibilizado aqui. A entrega deverá ser feita até 2024-12-09 via Moodle, na presente atividade.

# Restrições
## Universo da BD

O universo da BD deverá corresponder a dados reais. O tema do trabalho e o respetivo conjunto de dados serão atribuídos pelos docentes das práticas.

Os modelos de dados elaborados devem captar todo o conteúdo do conjunto de dados e evitar redundâncias, procurando registar cada facto apenas uma vez.

## Modelo relacional

O modelo relacional deverá corresponder a um mapeamento bem feito do diagrama de classes UML e ter chaves primárias e externas bem definidas.


## Povoamento da BD

A implementação do esquema deverá ser realizada em SQLite. As tabelas devem ser povoadas com os dados obtidos do conjunto de dados fornecido, evitando perda de informação.


## Extração de informação

As interrogações SQL, 10 ou mais de complexidade variável, visam ilustrar conteúdos relevantes da BD e, ao mesmo tempo, demonstrar as técnicas de interrogação estudadas.

## Interface

A interface, construída em Python, deverá permitir navegar pelas tabelas e executar as interrogações SQL elaboradas no ponto anterior.
