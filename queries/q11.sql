-- 12. Qual o ID e o código CPV do contrato com o maior valor em cada país?
-- Ordene por ordem de valor, para o caso do contrato ter mais de um CPV.
-- Criação de uma CTE (Common Table Expression) chamada "MaiorValorPorPais"
WITH MaiorValorPorPais AS (
    SELECT 
        idContrato,
        precoContratual,
        idPais,
        pais AS nomePais
    FROM Contratos
    NATURAL JOIN LocaisDeExecucao
    NATURAL JOIN Municipios
    NATURAL JOIN Distritos
    NATURAL JOIN Paises
    WHERE precoContratual IS NOT NULL
    GROUP BY idPais
    HAVING precoContratual = MAX(precoContratual)
)

SELECT 
    MVPC.idContrato,
    CP.codigoCPV,
    MVPC.nomePais,
    MVPC.precoContratual AS valorContrato
FROM MaiorValorPorPais MVPC
NATURAL JOIN CPVContratos CP
ORDER BY  valorContrato desc, CP.codigoCPV ASC;
