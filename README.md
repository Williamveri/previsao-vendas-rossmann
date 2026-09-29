# 📈 Previsão de Vendas - Rossmann Store Sales

Projeto de portfólio em Ciência de Dados com foco em **séries temporais/forecasting**, prevendo vendas diárias de mais de 1.100 lojas da rede Rossmann (varejo farmacêutico europeu), usando dados reais do Kaggle.

🔗 **Dashboard ao vivo:** [previsao-vendas-rossmann](https://previsao-vendas-rossmann-qd7uvzd4wi3wrkvalsce5u.streamlit.app)

## 🎯 Objetivo
Prever a demanda diária de vendas por loja, aplicando técnicas específicas de séries temporais: sazonalidade, lags, split temporal e comparação entre modelo estatístico clássico (SARIMA) e modelo de boosting (LightGBM).

## 📊 Dataset
[Rossmann Store Sales (Kaggle)](https://www.kaggle.com/c/rossmann-store-sales) — ~1 milhão de linhas, 1.115 lojas, período de 2013 a 2015.

## 🔍 Principais descobertas na EDA
- **Sazonalidade semanal forte**: vendas caem drasticamente aos domingos
- **Sazonalidade anual**: pico de vendas na semana anterior ao Natal, confirmado em 2013 e 2014
- **Sem tendência de longo prazo** clara ao longo dos 2,5 anos

## 🕵️ Uma investigação que valeu a pena
Ao analisar o gráfico de vendas totais, uma queda expressiva entre meados e fim de 2014 chamava atenção. A hipótese inicial poderia ser "queda de demanda" — mas ao investigar o número de lojas abertas no período, ficou claro que ~170 lojas estavam temporariamente fechadas. Normalizando as vendas por loja aberta, o "buraco" desaparecia. Esse tipo de verificação evita conclusões erradas a partir de artefatos nos dados, em vez de padrões reais de negócio.

## 🛠️ Tratamento de dados
Nulos tratados por contexto, não por imputação genérica: nulos em dados de concorrência/promoção contínua significam "não se aplica" (tratados com flag + valor neutro), não dado perdido. Dias com loja fechada (`Open=0`) removidos do treino, por não representarem demanda real.

## ⚙️ Engenharia de features
- Features de calendário (dia da semana, mês, dia do ano)
- Lags de 7 e 14 dias (venda no mesmo dia da semana anterior)
- Médias móveis de 7 e 30 dias

## 🔀 Validação
Split temporal (sem embaralhamento): treino com dados até 19/06/2015, teste com as últimas ~6 semanas — evitando vazamento de dados do futuro.

## 🤖 Modelos e resultados (Loja 1, para comparação justa)

| Modelo | MAE | RMSE | MAPE |
|---|---|---|---|
| **LightGBM** | 315.44 | 418.61 | **7.02%** |
| SARIMA(1,1,1)(1,1,1,7) | 641.82 | 726.30 | 15.25% |

**Por que o LightGBM superou o SARIMA:** o SARIMA modela apenas a série histórica isolada de uma loja, enquanto o LightGBM incorpora variáveis externas (promoção, feriados, características da loja) e aprende padrões compartilhados entre as 1.115 lojas simultaneamente — algo que o SARIMA, na sua forma univariada, não é capaz de fazer.

Resultado geral do LightGBM (todas as lojas): MAPE de 9.57%.

## 📈 Dashboard
Construído em Streamlit, com seletor de loja, métricas de erro e gráfico interativo de previsão vs. real, além de comparação lado a lado dos dois modelos.

## 🔭 Limitações e próximos passos
- O SARIMA foi ajustado manualmente (não via busca automática), devido a um conflito de dependências do `pmdarima` no ambiente de desenvolvimento — parâmetros otimizados poderiam melhorar seu desempenho
- SARIMA treinado apenas para uma loja (limitação estrutural de modelos univariados: não escalam para múltiplas séries no mesmo treino)
- Próximo passo natural: testar variáveis exógenas no SARIMA (SARIMAX) para uma comparação mais equilibrada com o LightGBM

## 🧰 Stack
Python · Pandas · LightGBM · statsmodels (SARIMA) · scikit-learn · Matplotlib · Streamlit

## 🚀 Como rodar localmente
\`\`\`bash
pip install -r requirements.txt
streamlit run dashboard.py
\`\`\`