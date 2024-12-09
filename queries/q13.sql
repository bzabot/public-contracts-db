-- 13. Qual é o valor médio dos contratos para cada tipo de procedimento em cada distrito?
WITH MediaPorTipoProcedimentoDistrito AS (
    SELECT 
        D.distrito,
        TP.procedimento AS tipoProcedimento,
        ROUND(AVG(C.precoContratual), 2) AS mediaValor
    FROM Contratos C
    JOIN LocaisDeExecucao L ON C.idContrato = L.idContrato
    JOIN Municipios M ON L.idMunicipio = M.idMunicipio
    JOIN Distritos D ON M.idDistrito = D.idDistrito
    JOIN TiposProcedimentos TP ON C.idProcedimento = TP.idProcedimento
    WHERE C.precoContratual IS NOT NULL
      AND D.distrito IS NOT NULL
    GROUP BY D.distrito, TP.procedimento
)
SELECT * 
FROM MediaPorTipoProcedimentoDistrito
ORDER BY distrito, tipoProcedimento;
