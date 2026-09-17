DESIGN SYSTEM OFICIAL — SIGC
Sistema Integrado de Gestão Comercial

Versão Oficial 1.0

Esta documentação define a identidade visual oficial do SIGC e deve ser considerada a única referência válida para qualquer novo desenvolvimento.

1. IDENTIDADE VISUAL
Conceito

O SIGC é um sistema administrativo/comercial.

A interface deve transmitir:

Organização
Confiabilidade
Clareza
Rapidez operacional
Facilidade de uso
Estilo Visual

O estilo oficial é:

Moderno + Administrativo + Comercial

Inspirado em:

ERP's modernos
Sistemas de gestão empresarial
Dashboards SaaS
PDVs contemporâneos
Objetivos da Interface

Prioridades:

Velocidade operacional
Facilidade de aprendizado
Poucos cliques
Leitura rápida
Consistência visual
Responsividade
2. PALETA DE CORES OFICIAL
Cor Primária
Azul SIGC

HEX:

#0D6EFD

RGB:

rgb(13, 110, 253)

Uso:

Botões principais
Links
Elementos ativos
Destaques
Cor Secundária

HEX:

#6C757D

RGB:

rgb(108,117,125)

Uso:

Botões secundários
Textos auxiliares
Cor de Sucesso

HEX:

#198754

RGB:

rgb(25,135,84)

Uso:

Confirmações
Pagamentos
Indicadores positivos
Cor de Aviso

HEX:

#FFC107

RGB:

rgb(255,193,7)

Uso:

Alertas
Atenção
Estoque baixo
Cor de Erro

HEX:

#DC3545

RGB:

rgb(220,53,69)

Uso:

Exclusões
Erros
Ações destrutivas
Cor de Informação

HEX:

#0DCAF0

RGB:

rgb(13,202,240)

Uso:

Informações
Avisos neutros
Fundo Principal

HEX:

#F5F7FA

Uso:

Plano de fundo geral.

Fundo dos Cards

HEX:

#FFFFFF

Uso:

Cards e painéis.

Bordas

HEX:

#DEE2E6

Uso:

Separações sutis.

Texto Principal

HEX:

#212529

Uso:

Títulos e conteúdo principal.

Texto Secundário

HEX:

#6C757D

Uso:

Descrições e informações auxiliares.

3. TIPOGRAFIA
Fonte Principal
'Inter', sans-serif

Caso não esteja instalada:

'Segoe UI', sans-serif
Fontes Fallback
Arial
Helvetica
sans-serif
Pesos
400 Regular
500 Medium
600 SemiBold
700 Bold
Hierarquia
H1
36px
700
H2
30px
700
H3
24px
600
Texto padrão
16px
400
Texto auxiliar
14px
400
4. ESPAÇAMENTO
Sistema Base

Utilizar múltiplos de:

4px
Espaçamentos Oficiais
4px
8px
12px
16px
20px
24px
32px
40px
48px
Padding dos Cards
20px
Border Radius

Padrão:

12px

Grandes:

15px

Pequenos:

8px
5. COMPONENTES PADRÃO
BOTÕES
Primário
background: #0D6EFD;
color: white;
Secundário
background: #6C757D;
color: white;
Sucesso
background: #198754;
color: white;
Aviso
background: #FFC107;
color: #212529;
Perigo
background: #DC3545;
color: white;
Hover

Escurecer:

10%
Disabled
opacity: .6;
cursor: not-allowed;
INPUTS

Padrão:

height: 48px;
border-radius: 10px;
border: 1px solid #CED4DA;
Focus
border-color: #0D6EFD;
box-shadow:
0 0 0 3px rgba(13,110,253,.15);
Select2

Já padronizado.

Altura:

60px

Radius:

15px
TABELAS
Cabeçalho
background: #F8F9FA;
font-weight: 600;
Hover
background: #F5F7FA;
Bordas
#DEE2E6
CARDS
Estrutura
background: white;
border-radius: 12px;
padding: 20px;
Sombra
box-shadow:
0 2px 8px rgba(0,0,0,.08);
Hover
transform: translateY(-3px);
MODAIS
Estrutura
.modal
.modal-content
.modal-header
.modal-actions
Cabeçalho

Ícone + título.

Corpo

Texto centralizado.

Rodapé

Botões alinhados à direita.

6. ÍCONES

Biblioteca oficial:

Font Awesome
Tamanhos

Pequeno

16px

Médio

20px

Grande

30px
Regra

Sempre utilizar ícones sem exagero.

Ícone deve complementar a informação.

Nunca substituir texto.

7. DASHBOARD
Cards KPI

Estrutura:

background: white;
padding: 25px;
border-radius: 15px;

Conteúdo:

Ícone
Valor
Descrição

Exemplo:

💰
R$ 12.350
Faturamento do mês
Indicadores

Cores:

Verde

Positivo

Vermelho

Negativo

Azul

Neutro
8. MÓDULO DE PRODUTOS
Cartões

Estrutura oficial:

Imagem
Nome
Categoria
Preço
Estoque
Ações
Imagem

Prioridade:

Foto do produto

Fallback:

Ícone da categoria
Estoque

Verde

Normal

Amarelo

Baixo

Vermelho

Sem estoque
9. MÓDULO DE VENDAS
Layout

Duas áreas:

Catálogo
+
Carrinho
Produto

Cartão clicável.

Adicionar com um clique.

Carrinho

Estrutura oficial:

Imagem

Nome

Tipo de venda

Quantidade

Desconto aplicado

Preço original

Preço aplicado

Subtotal

Excluir
Confirmações

Obrigatórias:

Limpar carrinho
Remover item
Reduzir de 1 para 0

Todos utilizando modal reutilizável.

10. MÓDULO DE ESTOQUE
Estrutura

Mostrar:

Produto
Origem
Quantidade recebida
Quantidade atual
Preço compra
Data
Destaques

Entrada recente:

Azul

Estoque baixo:

Amarelo

Sem estoque:

Vermelho

11. MÓDULO DE FICHAS DE SINUCA
Identidade

Cor principal:

#6F42C1

(Roxo)

Ícone

Mesa de sinuca ou taco.

Indicadores

Mostrar:

Fichas disponíveis
Fichas vendidas
Receita
Participação 50%
12. RESPONSIVIDADE
Desktop

≥ 1200px

Layout completo.

Notebook

992px–1199px

Grid reduzido.

Tablet

768px–991px

Menu recolhível.

Celular

≤ 767px

Cards empilhados.

Botões largura total.

13. REGRAS DE UX
Navegação

Sempre previsível.

Nunca mudar localização dos elementos principais.

Feedback

Toda ação deve gerar:

flash()
Sucesso

Verde.

Erro

Vermelho.

Aviso

Amarelo.

Exclusões

Sempre exigir confirmação.

Nunca excluir diretamente.

Carregamento

Sempre indicar quando houver processamento demorado.

14. CSS BASE
:root{

    /* CORES */

    --primary:#0D6EFD;
    --secondary:#6C757D;

    --success:#198754;
    --warning:#FFC107;
    --danger:#DC3545;
    --info:#0DCAF0;

    --bg:#F5F7FA;
    --card:#FFFFFF;

    --border:#DEE2E6;

    --text:#212529;
    --text-muted:#6C757D;

    --sinuca:#6F42C1;

    /* FONTES */

    --font-primary:'Inter',sans-serif;
    --font-secondary:'Segoe UI',sans-serif;

    /* TAMANHOS */

    --h1:36px;
    --h2:30px;
    --h3:24px;

    --text-size:16px;
    --small-size:14px;

    /* ESPAÇAMENTOS */

    --space-1:4px;
    --space-2:8px;
    --space-3:12px;
    --space-4:16px;
    --space-5:20px;
    --space-6:24px;
    --space-7:32px;
    --space-8:40px;

    /* BORDAS */

    --radius-sm:8px;
    --radius-md:12px;
    --radius-lg:15px;

    /* SOMBRAS */

    --shadow:
        0 2px 8px rgba(0,0,0,.08);

}
15. REGRAS OBRIGATÓRIAS DE DESIGN
Utilizar exclusivamente a paleta oficial.
Todo card deve utilizar sombra padrão.
Todo formulário deve utilizar inputs padronizados.
Toda exclusão deve possuir confirmação.
Toda ação deve possuir feedback visual (flash message).
Novos módulos devem seguir o mesmo padrão de cards.
Utilizar Font Awesome como biblioteca oficial.
Utilizar Select2 em listas grandes.
Nunca criar componentes visuais duplicados se já existir componente reutilizável.
Manter consistência entre Dashboard, Produtos, Estoque, Vendas e Contas.
Priorizar clareza operacional antes de estética.
O sistema deve parecer um ERP comercial moderno.