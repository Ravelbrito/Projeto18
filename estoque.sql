create database estoque;

use estoque;

create table produto(
id_produto int auto_increment primary key,
Nome varchar (200) not null,
Descricao varchar (200) not null,
quantidade varchar (200) not null,
preco decimal (10, 2)
);

Create table venda(
id_venda int auto_increment primary key,
id_produto_vendido int auto_increment primary key,
qtd_vendida int,
data_venda datetime
);
