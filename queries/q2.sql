-- q2.Qual é o valor total dos contratos para cada país e tipo de contrato?
SELECT pais, tipo, SUM(precoContratual) AS total
FROM Contratos 
NATURAL JOIN LocaisDeExecucao
NATURAL JOIN Municipios
NATURAL JOIN Distritos
NATURAL JOIN Paises
NATURAL JOIN ClassificacaoContratos
NATURAL JOIN TiposContratos
GROUP BY pais, tipo;
