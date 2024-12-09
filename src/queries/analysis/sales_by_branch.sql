SELECT id_filial, SUM(venda_pecas) AS venda_pecas
FROM sales
GROUP BY id_filial;
