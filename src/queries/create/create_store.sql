CREATE TABLE IF NOT EXISTS store (
    ID_FILIAL INT NOT NULL,
    LOJA VARCHAR(100) NOT NULL,
    PONTO_VENDA_COD INT NOT NULL,
    PONTO_VENDA VARCHAR(200) NOT NULL,
    PUBLICO_LOJA CHAR(50) NOT NULL,
    CANAL VARCHAR(50) NOT NULL,
    CIDADE VARCHAR(100) NOT NULL,
    LOJA_M2 INT NOT NULL,
    PAIS CHAR(2) NOT NULL,
    UF CHAR(2) NOT NULL,
    CLIMA VARCHAR(50) NOT NULL,
    STATUS VARCHAR(20) NOT NULL
);