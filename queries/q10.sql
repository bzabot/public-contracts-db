-- q10.	Qual é o nif e a designação dos adjudicantes com pelo moenos 5 contratos, e quais são objectos contrato associados a cada contrato um desses contratos? Ordene a designacao por ordem crescente.
WITH Adjudicantes5Cont AS ( -- retorna o id dos adjjudicantes com pelo menos 5 contratos
    SELECT idAdjudicante
    FROM Contratos
    JOIN Entidades ON idAdjudicante = idEntidade
    GROUP BY idAdjudicante
    HAVING COUNT(idContrato) <= 5
) 
SELECT nif, entidade AS designacao, objetoContrato
FROM Contratos
JOIN Entidades ON idAdjudicante = idEntidade
WHERE idAdjudicante IN Adjudicantes5Cont
ORDER BY entidade;