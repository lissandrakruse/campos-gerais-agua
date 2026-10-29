# Acesso, proveniência e direitos

## Situação inicial
Nenhuma série bruta experimental de terceiros foi incorporada neste repositório. O suplemento público de De Paula et al. (2026, Journal of Soils and Sediments) contém 24 eventos datados e quatro contrastes percentuais derivados; esses contrastes não substituem as séries absolutas por parcela e estão preservados como uma extração derivada atribuída em `data/published_derived/`, separada do esquema de eventos brutos. O catálogo descreve evidência disponível e pendências, não uma coleção já integrada. Não houve contato com pesquisadores em nome da responsável.

Para cada fonte obter: versão/DOI, titular, licença ou autorização, unidade experimental, área, limites autorizados, datas/fuso, frequência, sensores/calibração, protocolo de agregação, faltantes, tratamentos e histórico de manejo. Registrar hash do arquivo recebido, data de acesso e transformações. Publicar dados brutos somente quando a permissão realmente cobrir redistribuição.

Dados recebidos podem permanecer locais em `data/raw/` (ignorado pelo Git). A regra de `.gitignore` não é garantia de privacidade; revisar o conteúdo antes de qualquer commit. Não incluir nomes, contatos ou coordenadas não autorizadas de produtores.

## Fontes orbitais e ambientais
Sentinel-1/2: catálogo oficial https://dataspace.copernicus.eu/ . Existência de cobertura em um ponto do município não comprova cena útil na data de cada evento.

MapBiomas Água: https://brasil.mapbiomas.org/iniciativas-e-produtos/agua/mapeamento-mensal/superficie-de-agua-mensal/ . Produto mensal de 30 m pode apoiar contexto, mas não a duração diária exata ou verdade de campo. Conferir coleção e licença ao baixar.

TOPODATA: https://www.dsr.inpe.br/topodata/acesso . Relevo regional, não microdrenagem levantada em campo.

Chuva: priorizar o pluviômetro do experimento. SIMEPAR/IDR/INMET podem complementar se houver acesso e representatividade; estação Castro não deve ser renomeada Ponta Grossa. Dados climáticos médios históricos não substituem a chuva de um evento.

## Sobreposições
Capão da Onça: Barbosa 2025 e De Paula 2026 não são dois sítios independentes. Carambeí: capacidade de água disponível é propriedade derivada de retenção, não observação contínua de umidade. Estudos históricos anteriores aos sensores não podem ser alinhados a imagens modernas como se contemporâneos.

## Inconsistências documentais a resolver
- Não unir automaticamente os eventos de março de 2023 entre os artigos: os rótulos/datas diferem; preservar o original e obter horários antes da integração.
- A figura de cobertura de 2025 associa uma imagem de 6/03/2023 a um evento de 3/03/2023 como antecedente. A cronologia precisa ser esclarecida; a imagem não será usada como preditor pré-evento sem verificação.
- Eventos sucessivos no mesmo período chuvoso e as duas parcelas observadas na mesma tempestade devem permanecer no mesmo grupo de avaliação, quando identificáveis. O agrupamento exigirá metadados reais, não somente IDs inventados.
