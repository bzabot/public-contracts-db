--Q.14 Qual é fundamentação que mais aparece em cada distrito?
WITH FundamentacaoPorDistrito AS (
    SELECT 
        d.distrito, 
        f.artigo,
        f.numero,
        f.alinea,
        f.referenciaLegislativa,
        (COALESCE(f.artigo, '') || ' ' || 
         COALESCE(f.numero, '') || ' ' || 
         COALESCE(f.alinea, '') || ' - ' || 
         COALESCE(f.referenciaLegislativa, '')) AS fundamentacao, 
        COUNT(*) as total
    FROM LocaisDeExecucao le
    NATURAL JOIN Municipios m
    NATURAL JOIN Distritos d
    NATURAL JOIN FundamentacaoContratos fc
    NATURAL JOIN Fundamentacoes f
    GROUP BY d.distrito, f.artigo, f.numero, f.alinea, f.referenciaLegislativa, fundamentacao
),
MaxFundamentacao AS (
    SELECT 
        distrito, 
        MAX(total) as max_total
    FROM FundamentacaoPorDistrito
    GROUP BY distrito
)
SELECT 
    fpd.distrito, 
    fpd.artigo,
    fpd.numero,
    fpd.alinea,
    fpd.referenciaLegislativa,
    fpd.fundamentacao, 
    fpd.total
FROM FundamentacaoPorDistrito fpd
NATURAL JOIN MaxFundamentacao mf
WHERE fpd.total = mf.max_total
ORDER BY fpd.distrito;
;
