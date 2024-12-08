-- 13. Quais são os tipos de contrato que tiveram a data de celebração no dia 15/01/2024,
-- com a contagem de contratos por município?
SELECT 
    TC.tipo AS tipoContrato,
    M.municipio,
    COUNT(C.idContrato) AS quantidadeContratos,
    DATE(C.dataCelebracaoContrato) AS dia
FROM Contratos C
JOIN LocaisDeExecucao L ON C.idContrato = L.idContrato
JOIN Municipios M ON L.idMunicipio = M.idMunicipio
JOIN TiposContratos TC ON C.idProcedimento = TC.idTipoContrato
WHERE DATE(C.dataCelebracaoContrato) = '2024-01-15'
GROUP BY TC.tipo, M.municipio, dia
ORDER BY TC.tipo, M.municipio;
;
