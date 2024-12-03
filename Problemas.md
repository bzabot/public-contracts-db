# Problemas e Soluções no Tratamento de Dados
## Local de execução
- Colunas que tem mais de um valor - local de execucao, tipo de contrato, cpv, entidades

- vi que pode ser que tenha mais que uma fundamentação, mas no caso do nosso dataset isso nao ocorre
nem todos tem fundamentacao
- Alterar nome das tabelas para que de para fazer natural join
- falta descricao acordo quadro
Menor Espaço de Armazenamento:

Um INTEGER ocupa menos espaço do que uma string. Por exemplo:
Em muitos bancos de dados, um INTEGER de até 10 dígitos ocupa 4 ou 8 bytes.
Uma string de 10 caracteres (usando VARCHAR(10)) pode ocupar até 10 bytes ou mais , dependendo da codificação, como UTF-8


SQLite nao tem tipo bool
SQLite does not have a separate Boolean storage class. Instead, Boolean values are stored as integers 0 (false) and 1 (true).

Tem mais ou menos umas 140 linhas de fundamentações sem valeiros, acho que nesse caso não há necessidade de criar uma nova tabela, pois em comparação ao todo é menos de 1% dos casos

No caso de não ter adjucatarios, colocamos none associado ao contrao ou nao colocamos nada? no momento vou colcoar nada

Tem sempre um adjudicante, adjudicatario pode ser mais de um

### Problema 1: Múltiplos locais por contrato
Em alguns casos, um contrato pode conter mais de uma localidade.

Formato fornecido: Locais separados por | e municipio, distrito e país são separados por , .

Solução:
- Criar uma tabela específica para localidades.
- Cada localidade será vinculada ao contrato correspondente.
- A tabela deve incluir o id do contrato e do municipio.

### Problema 2: Apenas o país é fornecido
Para contratos fora de Portugal, só o país está presente.

Solução:
- Vincular o país diretamente ao contrato na base de dados.
- Não criar registros de municipios ou distritos quando essas informações não estão disponíveis.

### Problema 3: Há casos com apenas municipio e país
Exemplo: Portugal, Guarda

Guarda não é um distrito, mas sim uma municipio.
Existem casos em que o distrito não é fornecido.
Solução:
- Se a municipio já estiver na bd não há problema só retornamos o id do municipio e adicionamos na tabela localidades
- caso contratio precisamos analisar como proceder

## 2. Entidades
Problema 1: Presença da sigla RGPD
Algumas entidades não têm NIF registrado, sendo substituído por uma marcação RGPD.

Solução:
- Criar um identificador único para cada entidade diretamente na base de dados. Para que possamos garantir a consistência, especialmente para registros fora de Portugal, onde o NIF pode se repetir, além de que não poderemos usar o nif para identificação.
Problema 2: Repetição de NIF fora de Portugal
Em países diferentes, um mesmo NIF pode ser associado a entidades distintas.
- Acredito que o melhor seria validarmos a existencia da entidade com base do conjunto (nif, nome)
- Ao adicionar os adjudicantes somente comparando o nif tem 1760 linhas, já comparando o if e o nome tem 1830, é bom verificar se de fato existem nifs ou nomes repetidos só para garantir, ou verificar se a função que faz essa checagem de fato está correta // esses valores foram antes de eu perceber que um contrato pode ter mais que uma entidade na coluna adjudicante ou adjudicatario

Problema 2: Contratos sem adjudicatarios

Existem contratos sem adjudicatarios, são bem poucos, como a tabela de adjudicatarios é separada não teremos problema com isso. 

Além disso é importante mencionar que tem contrato com mais de um adjudicantario, talvez ocorra o mesmo para adjudicante

### Problema 3: Sanitização
Precismaos verificar se essa sanitização é suficiente