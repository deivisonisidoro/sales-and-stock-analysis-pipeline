SELECT produto, cor_produto, AVG(velocidade_venda) AS avg_velocidade_venda
FROM sales_velocity
GROUP BY produto, cor_produto
ORDER BY avg_velocidade_venda DESC
LIMIT 10;