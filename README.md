# Simulador de Irradiância Fotovoltaica

Esta aplicação é um simulador baseado em Streamlit para o estudo de painéis fotovoltaicos e irradiância solar.

## Funcionalidades
- Simulação em tempo real do comportamento de painéis fotovoltaicos.
- Bancada de laboratório interativa.
- Análise comparativa de diferentes filtros de luz.
- Atualização em tempo real de esquemas de circuitos (V e mA).

## Como executar localmente
1. Instale as dependências: `pip install -r requirements.txt`
2. Execute a aplicação: `streamlit run app.py`

## Manutenção
Foi configurada uma GitHub Action automática que realiza um commit fictício de 5 em 5 horas. Isto serve para manter a aplicação no Streamlit Cloud ativa e "quente", evitando que entre em modo de suspensão por inatividade.
