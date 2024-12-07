-- q5.Qual é o nif e a designação dos adjudicatários que têm contratos em Portugal e têm prazo de execução inferior a 365?
SELECT nif, entidade
FROM Contratos 
NATURAL JOIN LocaisDeExecucao
NATURAL JOIN Municipios
NATURAL JOIN Distritos
NATURAL JOIN Paises
NATURAL JOIN Adjudicatarios
NATURAL JOIN Entidades
WHERE prazoExecucao < 365
GROUP BY idEntidade; -- pois, um adjudicatario pode estar em mais de um contrato
