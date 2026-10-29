# Campos Gerais Água

**Projeto em estruturação: auditoria computacional de dados publicados e processamento exploratório de uma imagem Sentinel-2. Sem modelo preditivo treinado ou validação de campo.**

Responsável: Lissandra Kruse Fuganti. Escopo inicial: lavouras de Ponta Grossa e Carambeí, com extensão regional condicionada à disponibilidade e comparabilidade de dados.

## Pergunta de pesquisa
Combinar chuva, propriedades do solo e cobertura vegetal melhora a estimativa de escoamento superficial em lavouras dos Campos Gerais, em comparação com modelos simples?

O objetivo é desenvolver e avaliar um fluxo computacional reprodutível que apoie estudos de conservação da água e do solo. Não é uma ferramenta operacional de alerta, recomendação de irrigação ou diagnóstico de dano agrícola.

## Por que começar por escoamento?
Há experimentos locais documentados de chuva e escoamento, mas as séries completas ainda precisam ser obtidas. Escoamento medido na saída da parcela **não equivale** a um mapa de água parada dentro do talhão. A futura detecção de alagamentos por satélite será um módulo separado, dependente de referências de campo datadas e georreferenciadas.

## O que existe aqui
- [Protocolo de pesquisa](docs/protocolo.md): hipóteses, comparadores, validação e limites.
- [Catálogo de fontes](docs/fontes.csv): artigos e fontes de dados, com disponibilidade verificada ou pendente.
- [Plano de acesso e proveniência](docs/dados.md): acesso, licenças e critérios de integração.
- [Dicionário de dados](docs/dicionario.md) e [CSV vazio](data/templates/eventos.csv).
- Validador de formato e testes unitários em Python, sem dependências externas.
- [Contrastes derivados publicados](data/published_derived/PROVENANCE.md): extração atribuída de 24 eventos/96 células do suplemento de De Paula et al. (2026), não séries brutas nem resultados de nosso modelo.
- Exemplo **inteiramente sintético**, destinado apenas a testar o validador de eventos.

## Executar
Requer Python 3.10 ou superior. A partir da raiz:

```sh
python -m unittest discover -s tests -v
python scripts/validate_events.py examples/eventos_sinteticos.csv --allow-synthetic
```

O validador recusa dados sintéticos sem a opção explícita. Ele verifica formato e limites básicos; não certifica a qualidade, independência ou plausibilidade hidrológica das observações.

## Estado da pesquisa
| Etapa | Estado |
|---|---|
| Levantamento inicial de literatura regional | Realizado, não sistemático |
| Acesso às séries brutas dos experimentos | Pendente |
| Autorização/licença para reutilizar e redistribuir dados | Pendente por fonte |
| Imagens para datas e limites exatos dos experimentos | Pendente |
| Treinamento e validação | Não iniciados |
| Submissão a revista | Não realizada |

Artigos da Capão da Onça de 2025 e 2026 compartilham o sítio experimental e não são validações geográficas independentes. O estudo de Carambeí de 2023 mede propriedades do solo, não uma série contínua de umidade ou alagamento. Não se afirma ineditismo: há precedentes regionais, incluindo AquaCrop para trigo.

## Próximos marcos
1. Confirmar acesso e licença das séries, limites de parcelas e metadados.
2. Auditar datas, unidades, eventos e dependência entre tratamentos/publicações.
3. Definir tamanho efetivo da amostra e congelar o protocolo antes de comparar modelos.
4. Construir comparadores simples e avaliação temporal agrupada; testar outra área apenas se houver dados independentes.
5. Relatar resultados positivos ou negativos com incertezas e rastreabilidade.

## Integridade e direitos
Foram publicados documentação original, código inicial, exemplos sintéticos e uma extração atribuída de tabela factual sob CC BY 4.0, com proveniência e limites explícitos. PDFs de artigos, séries de terceiros e coordenadas privadas de propriedades não foram republicados. As fontes mantêm suas licenças. A tabela derivada mantém a licença CC BY 4.0 da fonte, conforme sua proveniência. A disponibilização pública dos demais arquivos não concede uma licença geral de reutilização; nenhuma licença de software foi escolhida nesta versão.

Foi utilizada assistência de IA na estruturação e no código inicial. Os testes verificam software, não validade científica; análise, interpretação e eventual submissão exigem revisão humana. Publicação no GitHub não é publicação científica revisada por pares.

## Pipeline descritivo executável

```bash
python scripts/run_pipeline.py --out outputs/published
python -m unittest discover -s tests -v
```

Sem dependências externas. Confere o hash da tabela auditada (todos os 96 valores e metadados), gera `summary.json`, `metrics.csv`, `report.md` e `manifest.json` com hashes. Resultados determinísticos, sem dados sintéticos nesse fluxo. A comparação independente com o documento original é uma etapa separada de extração/auditoria.

Notebook autocontido, sem internet: [notebooks/campos_gerais_agua_kaggle.ipynb](notebooks/campos_gerais_agua_kaggle.ipynb). Pronto para execução no Kaggle; a presença deste arquivo não significa que já foi publicado ou executado naquela plataforma. Exemplos sintéticos continuam apenas no validador de esquema separado.

### Versão 2: auditoria de sensibilidade

O mesmo comando agora calcula médias por registro e balanceadas por data, influência da exclusão de cada data e cenários de denominadores desconhecidos. Descrições publicadas e testemunhas **construídas, não observadas** ficam em pastas separadas. Nenhum cenário representa produtividade/perda medida ou corrige conclusões dos autores. A não identificação se refere à Tabela S1 isolada. Consulte [método e limites](docs/sensitivity_method.md).

[Kaggle — notebook em inglês](https://www.kaggle.com/code/lissandrakruse/campos-gerais-water-published-runoff-pipeline). A versão publicada no Kaggle tem histórico próprio; confira a versão exibida antes de comparar os resultados.

## Observação da Terra — módulo separado

[Sentinel-2 corrigido v2](eo/sentinel2/README.md): imagem real processada no Kaggle, 71.145 pixels finitos em grade de 20 m e 24 pixels acima de MNDWI > 0 (0,96 ha exploratórios, não inundação validada). A primeira versão com offset duplicado foi descartada. Código, notebook-fonte, atribuição e manifest preservados; sem bandas grandes ou manuscrito. **SWOT ainda não processado; comparação entre sensores pendente.**

## Comparação real SWOT–Sentinel

[Módulo conjunto](eo/swot_sentinel/README.md) com subset mínimo público, código, métricas e mapas: filtro primário de boa qualidade tem **n=0**; a sensibilidade com 495 pares suspeitos é apenas exploratória, não acurácia ou validação agronômica. O status anterior de SWOT pendente fica superado por este módulo; não foi alterada a calibração Sentinel corrigida.
