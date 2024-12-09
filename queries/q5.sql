--q5.Quais são os adjudicatários que começam com a letra ‘M’?
SELECT entidade
FROM Entidades
NATURAL JOIN Adjudicatarios
WHERE entidade LIKE "M%";
