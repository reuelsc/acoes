# Análise de Ações B3 — Fundamentalista + Técnica + Opções

Sistema que analisa ações da B3, combina análise fundamentalista e técnica,
e sugere a melhor operação via opções (call, put, trava, venda coberta etc.)
conforme o cenário identificado para cada ativo.

## Visão geral da arquitetura

```
                     ┌──────────────────────┐
                     │   GitHub Actions      │  (agendador diário, grátis)
                     │  roda 1x/dia após     │
                     │  fechamento do pregão │
                     └──────────┬────────────┘
                                │
                     ┌──────────▼────────────┐
                     │  main.py (pipeline)    │
                     │  coleta -> analisa ->  │
                     │  rankeia -> reporta    │
                     └───┬───────────────┬────┘
                         │               │
            ┌────────────▼───┐   ┌───────▼─────────┐
            │ Relatório HTML  │   │ Notificação      │
            │ (GitHub Pages)  │   │ Telegram         │
            └─────────────────┘   └──────────────────┘

                     ┌──────────────────────┐
                     │  api/app.py (FastAPI) │  backend sempre ativo
                     │  hospedado no Render  │  (busca sob demanda)
                     └──────────┬────────────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                            │
         ┌────────▼────────┐         ┌─────────▼────────┐
         │ Dashboard web    │         │ Bot do Telegram   │
         │ (busca qualquer  │         │ /analisar TICKER  │
         │ ticker, gráficos)│         │ a qualquer hora   │
         └──────────────────┘         └───────────────────┘
```

## Estrutura de pastas

- `config/` — configurações gerais (tickers padrão, chaves de API via `.env`)
- `data_collector/` — clientes para buscar dados externos (brapi, opções)
- `analysis/` — motores de análise fundamentalista, técnica e de opções
- `report/` — geração do relatório diário (HTML)
- `bot/` — bot do Telegram para consulta sob demanda
- `api/` — backend (FastAPI) que serve o dashboard web e a busca sob demanda
- `.github/workflows/` — automação do GitHub Actions (agendador diário)
- `main.py` — pipeline principal (coleta → analisa → rankeia → publica)

## Fontes de dados

- **[brapi.dev](https://brapi.dev)** — cotações, histórico e fundamentos das ações da B3
- **[OBM](https://obm.com.br/opcoes)** — cadeia de opções da B3 com Greeks e volatilidade implícita

## Como rodar localmente (para testar)

```bash
cd analise-acoes-b3
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # preencha o token da brapi (opcional no sandbox)
python main.py
```

Isso vai gerar o relatório do dia em `report/output/relatorio_YYYY-MM-DD.html`
usando a lista de tickers definida em `config/settings.py`.

## Status atual (esqueleto inicial)

- [x] Estrutura de pastas e pipeline principal
- [x] Coleta de cotações e fundamentos (brapi) — 4 tickers de sandbox funcionando sem token
- [x] Análise fundamentalista básica (P/L, ROE, dívida, dividend yield)
- [x] Análise técnica básica (médias móveis, RSI)
- [x] Motor de sugestão de estratégia de opções (regras iniciais)
- [x] Ranking das 10 melhores ações
- [x] Geração de relatório HTML
- [ ] Integração real com a API de opções (OBM) — hoje com dados de exemplo (mock)
- [ ] Bot do Telegram funcional
- [ ] Dashboard web (FastAPI) com busca por ticker
- [ ] Deploy no GitHub Actions + GitHub Pages + Render

## Próximos passos sugeridos

1. Validar a coleta de dados com seus tickers de interesse (precisa de token
   free da brapi para ir além dos 4 tickers de sandbox).
2. Refinar as regras de análise fundamentalista/técnica e da estratégia de
   opções junto com você.
3. Conectar a fonte real de dados de opções (OBM ou similar).
4. Subir o backend no Render e o bot no Telegram.
5. Configurar o GitHub Actions para rodar diariamente e publicar no GitHub Pages.
