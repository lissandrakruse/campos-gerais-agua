# Protocolo inicial de pesquisa — versão 0.1
Data: 29/10/2026. Documento prospectivo; não é um registro formal de pré-registro.

## Escopo e desfecho
Desfecho primário proposto: lâmina de escoamento superficial por evento e parcela (mm), calculada somente quando houver área, volume/vazão integrada e documentação de calibração. Chuva acumulada (mm), duração (h), chuva antecedente e cobertura anterior/compatível com o evento são candidatos a preditores. Propriedades do solo serão integradas apenas quando representarem a parcela e o período relevantes.

A intensidade de chuva deve ter intervalo explícito (p.ex., máximo em 30 minutos); não misturar máximos instantâneos, horários e médias. Dados pós-evento não entram como preditores antecipatórios. Solo de outro estudo/local não será atribuído a uma parcela por proximidade nominal.

## Hipóteses
- H1: incluir cobertura e solo melhora erro de previsão de escoamento frente a um comparador baseado apenas em chuva.
- H2: o ganho se mantém em eventos posteriores não usados no ajuste.
- H3, condicionada a dados: o modelo transfere entre áreas, com desempenho e incerteza documentados.

São hipóteses a testar, não resultados. Sem amostra adequada, o estudo será descritivo ou piloto, e H3 não será alegada.

## Comparadores e complexidade
Comparadores mínimos: previsão constante calculada apenas no treino e regressão simples/regularizada baseada em chuva. Métodos não lineares somente se o tamanho efetivo e a variedade dos dados justificarem. Não escolher IA apenas por novidade. Um modelo mais complexo que não superar o simples será reportado como tal.

## Unidade e separação treino–teste
A unidade é evento–parcela; parcelas sob a mesma tempestade são correlacionadas. `storm_group_id` identifica o evento meteorológico compartilhado. Linhas com o mesmo grupo não podem atravessar treino e teste. Medições a cada minuto não são réplicas independentes de tempestades. Publicações com eventos sobrepostos devem ser reconciliadas pelo estudo de origem.

Priorizar teste temporal posterior, com ajuste de hiperparâmetros e pré-processamento restritos ao treino e agrupados por tempestade. Uma validação em outra localidade deve ficar intocada até a avaliação final. Com apenas dois talhões e poucas dezenas de eventos, não prometer validade regional ou executar divisões aleatórias como prova de generalização.

## Avaliação
MAE e RMSE em mm; viés médio e gráficos observados–previstos. Reportar número de tempestades, parcelas e locais, erros por tratamento e dados ausentes. Intervalos devem respeitar agrupamento e tamanho reduzido; bootstrap por tempestade, se apropriado, não por minuto. Coeficiente de escoamento exige atenção à janela, armazenamento e contribuição externa; não impor automaticamente escoamento menor que chuva como regra universal.

## Módulo de satélite futuro
Sentinel-1/2 são candidatos principais. Confirmar passagem, nuvens, geometria, resolução efetiva, sazonalidade e datas. Valores de pixels próximos não criam novas réplicas de campo. SWOT é complementar e sua adequação depende da área/passagem; não se presume cobertura útil em pequenos talhões.

Alagamento é um desfecho diferente: exige presença/ausência ou extensão de lâmina de água observada por fotos, drone ou vistoria com data e localização. MapBiomas Água, chuva intensa e umidade do solo não substituem automaticamente essa referência. Ausência de observação não é ausência de água.

## Critérios de continuidade
Prosseguir para comparação preditiva somente após acesso legítimo, metadados auditáveis e desenho de avaliação viável. Se os dados forem apenas tabelas agregadas, limitar a síntese e a análise descritiva. Não extrapolar para alertas, perdas de produtividade ou recomendações de drenagem sem validação própria. Escolha da revista e alegações de contribuição dependem dos resultados e da revisão atualizada da literatura.

### Viés de seleção de eventos

Os 24 registros da Tabela S1 são eventos selecionados com escoamento, não todas as chuvas elegíveis. Um classificador de ocorrência exigiria também eventos elegíveis com ausência verificada de escoamento. Não se estima prevalência ou recall a partir desta lista. Agregados completos por evento e preditores auditados podem permitir modelos limitados futuros; hidrogramas minuto a minuto não são obrigatórios para todo modelo.
