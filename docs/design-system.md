# Sistema Integrado de Gestão Comercial

# Design System

--------------------------------------------------

# Objetivo


Este documento define os padrões visuais, estruturais e organizacionais do sistema.

Todo novo módulo deve seguir este guia para garantir consistência, manutenção e escalabilidade.

# Estrutura CSS
static/
│
├── css/
│   ├── global/
│   ├── components/
│   └── pages/

# Estrutura MVC
app/

├── controllers/
├── models/
├── routes/
├── templates/
├── static/
└── database/

# Componentes
Button

Arquivo:

components/button.css

Tipos:

button-primary
button-secondary
button-success
button-danger
button-warning
Card

Arquivo:

components/card.css

Estrutura:

.card
.card-header
.card-body
.card-footer
Dashboard Card

Arquivo:

components/dashboard-card.css

Usado em:

Estoque Atual
Dashboard Geral
Relatórios
Search

Arquivo:

components/search.css

Recursos:

Pesquisa instantânea
Ignora acentos
Filtro por nome
Empty State
Input

Arquivo:

components/input.css

Estrutura:

.form-group
label
input
select
textarea
Product Card

Usado em:

Venda
Estoque Atual
Produtos

Estrutura:

.produto-card
.produto-header
.produto-info
.produto-expandido
Estoque Card

Usado em:

Estoque Atual

Estrutura:

.estoque-card
.status-normal
.status-minimo
.status-baixo
.status-sem
.status-nunca
Status de Estoque

🟢 Normal

🔵 No mínimo

🟡 Baixo

🔴 Sem estoque

⚫ Nunca abastecido

Módulos Existentes
Cliente
Cadastro
Edição
Exclusão
Produto
Cadastro
Edição
Inativação
Histórico de Preços
Fornecedor
Cadastro
Consulta
Estoque
Entrada
Estoque Atual
Movimentação
Histórico
Venda
Venda por caixa
Venda por unidade
Venda por dose
Venda de cigarro (solto, maço e box)
Fiado
Cadastro
Pagamento
Histórico
Conta Pendente
Cadastro
Baixa
Consulta
Relatórios
PDF
Financeiro
Estoque
Vendas
Ícones Oficiais

Cliente

fa-user

Produto

fa-box

Fornecedor

fa-truck

Venda

fa-cart-shopping

Estoque

fa-warehouse

Movimentação

fa-arrow-right-arrow-left

Fiado

fa-book

Conta Pendente

fa-clock

Relatórios

fa-chart-column
Ordem de Desenvolvimento
1. Banco de Dados
2. Model
3. Controller
4. Route
5. HTML
6. CSS
7. JavaScript
8. Testes
9. Refatoração
Roadmap Atual

✅ Produtos

✅ Estoque

✅ Entrada de Estoque

✅ Venda

✅ Fiado

✅ Conta Pendente

✅ Histórico de Preços

✅ Movimentação de Estoque

⬜ Histórico de Vendas

⬜ Relatórios PDF

⬜ Dashboard Financeiro

⬜ Select2

⬜ Fotos no Estoque

⬜ Ficha de Sinuca

⬜ Raspadinha

Última atualização: 27/08/2026