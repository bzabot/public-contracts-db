-- q8.Qual o nome do adjudicatário que tem o maior número de contratos realizados? 
SELECT entidade, COUNT(idContrato) AS num_contratos
FROM Contratos
NATURAL JOIN Adjudicatarios 
NATURAL JOIN Entidades  
GROUP BY idEntidade
ORDER BY num_contratos DESC
LIMIT 1;
