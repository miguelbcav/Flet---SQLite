# 🏦 Sistema Bancário Simples – Python, Flet & SQLite

Este projeto foi criado para **demonstrar conhecimento prático em desenvolvimento de aplicações desktop**, unindo **interface gráfica**, **persistência de dados** e **lógica de negócio**, tudo utilizando **Python**.

Ele simula um **sistema bancário simples**, onde cada pessoa possui:
- nome
- idade
- saldo em conta

---

## 🎯 Objetivo do projeto

Este projeto existe para mostrar que eu sei:

- criar **interfaces gráficas com Flet**
- integrar frontend com **banco de dados SQLite**
- estruturar dados de forma persistente
- trabalhar com **CRUD básico** (Create / Read)
- organizar lógica de UI e dados
- construir sistemas funcionais, não apenas scripts

Mesmo sendo simples, ele representa um **caso real de aplicação**.

---

## 🧠 O que este projeto demonstra tecnicamente

### ✅ Interface gráfica com Flet
- layout responsivo (`ResponsiveRow`)
- cards dinâmicos
- navegação entre telas
- botões, campos de texto e ícones
- atualização de interface em tempo real

O sistema não é apenas funcional, ele também tem **estrutura visual organizada**.

---

### ✅ Persistência de dados com SQLite
- criação automática de tabela
- inserção e leitura de registros
- uso de banco local (`.db`)
- dados mantidos mesmo após fechar o app

```sql
CREATE TABLE IF NOT EXISTS contas_bancarias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titular TEXT,
    saldo FLOAT,
    idade TEXT
)
