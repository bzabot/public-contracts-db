-- q3. Qual é adjudicante com o contrato de valor mais alto?
SELECT entidade AS adjudicante, MAX(precoContratual) AS valor_maximo
FROM Contratos
JOIN Entidades ON idAdjudicante = idEntidade;
