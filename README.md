# Campos Gerais Água

**Projeto de pesquisa em estruturação. Sem modelo treinado, resultados próprios ou validação de campo nesta versão.**

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
- Exemplo **inteiramente sintético**, destinado apenas a testar o programa.

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
Somente documentação original, código inicial e exemplos sintéticos foram publicados. PDFs de artigos, séries de terceiros e coordenadas privadas de propriedades não foram republicados. As fontes mantêm suas licenças. A disponibilização pública deste repositório não concede uma licença geral de reutilização; nenhuma licença de software foi escolhida nesta versão.

Foi utilizada assistência de IA na estruturação e no código inicial. Os testes verificam software, não validade científica; análise, interpretação e eventual submissão exigem revisão humana. Publicação no GitHub não é publicação científica revisada por pares.
