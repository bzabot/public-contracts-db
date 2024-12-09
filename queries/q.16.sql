--Q.16 Quais são os pares distrito-procedimentocentralizados 
--tais que no distrito não exista nenhum um município com procedimentocentralizado = ‘Sim’.
SELECT DISTINCT 
    d.distrito,
    c.procedimentoCentralizado
FROM Distritos d
NATURAL JOIN Municipios m
NATURAL JOIN LocaisDeExecucao le
NATURAL JOIN Contratos c
WHERE d.idDistrito NOT IN (
    SELECT DISTINCT d2.idDistrito
    FROM Distritos d2
    NATURAL JOIN Municipios m2
    NATURAL JOIN LocaisDeExecucao le2
    NATURAL JOIN Contratos c2
    WHERE c2.procedimentoCentralizado = 1
)
AND d.distrito IS NOT NULL
ORDER BY d.distrito;
