--q9.Qual o total de contratos realizados em cada distrito (que tenha o campo distrito cadastrado) que tenha descrição de acordo quadro e data de poblicação entre 10/01/2024 e 13/01/2024, inclusive?
SELECT distrito, COUNT(idContrato) AS total
FROM Contratos
NATURAL JOIN AcordoQuadroContratos -- pega só os que tem descrição acordo quadro
NATURAL JOIN LocaisDeExecucao
NATURAL JOIN Municipios
NATURAL JOIN Distritos
WHERE dataPublicacao > '2024-01-10'
AND  dataPublicacao < '2024-01-14'
AND distrito IS NOT NULL -- retira os distritos que não foram cadastrados
GROUP BY distrito;