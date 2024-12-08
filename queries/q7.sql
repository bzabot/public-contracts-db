-- q7.Qual é a quantidade de contratos em cada tipo diferente de procedimento?
SELECT COUNT(idcontrato) as quantidade, procedimento as tipo_procedimento
FROM contratos
NATURAL JOIN tiposProcedimentos 
GROUP BY idProcedimento
