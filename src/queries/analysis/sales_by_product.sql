SELECT produto, SUM(venda_pecas) AS venda_pecas
FROM sales
GROUP BY produto;
