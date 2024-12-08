## 2. Entidades
Problema 1: Presença da sigla RGPD
Algumas entidades não têm NIF registrado, sendo substituído por uma marcação RGPD.

Solução:
- Criar um identificador único para cada entidade diretamente na base de dados. Para que possamos garantir a consistência, especialmente para registros fora de Portugal, onde o NIF pode se repetir, além de que não poderemos usar o nif para identificação.
Problema 2: Repetição de NIF fora de Portugal
Em países diferentes, um mesmo NIF pode ser associado a entidades distintas.
- Acredito que o melhor seria validarmos a existencia da entidade com base do conjunto (nif, nome)
- Ao adicionar os adjudicantes somente comparando o nif tem 1760 linhas, já comparando o if e o nome tem 1830, é bom verificar se de fato existem nifs ou nomes repetidos só para garantir, ou verificar se a função que faz essa checagem de fato está correta // esses valores foram antes de eu perceber que um contrato pode ter mais que uma entidade na coluna adjudicante ou adjudicatario
