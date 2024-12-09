--17.Quais municipios não possuem contratos cujo valor contratual seja superior a 1.000.000 euros? 
--E qual o contrato com o valor mais alto de cada um desses municipios?"
WITH MunicipiosSemContratosAltos AS (
    SELECT DISTINCT m.municipio, 
           MAX(c.precoContratual) AS valorMaisProximo
    FROM Municipios m
    NATURAL JOIN LocaisDeExecucao le
    NATURAL JOIN Contratos c
    WHERE m.idMunicipio NOT IN (
        SELECT DISTINCT m2.idMunicipio
        FROM Municipios m2
        NATURAL JOIN LocaisDeExecucao le2
        NATURAL JOIN Contratos c2
        WHERE c2.precoContratual > 1000000
    )
    AND m.municipio IS NOT NULL
    GROUP BY m.municipio
    HAVING MAX(c.precoContratual) IS NOT NULL
)
SELECT 
    municipio, 
    valorMaisProximo
FROM MunicipiosSemContratosAltos
ORDER BY municipio;
