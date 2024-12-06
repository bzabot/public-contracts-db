-- q10. Quais municípios cadastrados não possuem contratos que sejam procedimentos centralizados, ordene os municipios por ordem crescente?
WITH municipiosCentra AS ( -- municipios com contratos com procedimentos centralizados
    SELECT idMunicipio
    FROM Contratos
    NATURAL JOIN LocaisDeExecucao
    NATURAL JOIN Municipios
    WHERE procedimentoCentralizado = "Sim"
    GROUP BY idMunicipio
)
SELECT municipio 
FROM Municipios
WHERE idMunicipio NOT IN municipiosCentra
AND municipio IS NOT NULL
ORDER BY municipio;