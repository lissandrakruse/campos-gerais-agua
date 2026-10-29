# Dicionário mínimo — eventos.csv
Uma linha por evento e parcela. UTF-8, vírgula, ponto decimal; valores ausentes vazios. O modelo é inicial e deverá ser adaptado às fontes reais sem perder rastreabilidade.

| Campo | Definição |
|---|---|
| event_id | Identificador único da linha evento–parcela |
| storm_group_id | Tempestade compartilhada entre parcelas; chave de agrupamento na avaliação |
| site_id | Sítio experimental pseudonimizado |
| plot_id | Parcela dentro do sítio |
| start_utc / end_utc | ISO 8601 UTC terminando em Z |
| rainfall_mm | Chuva acumulada na janela; não negativa |
| runoff_mm | Lâmina de escoamento na janela; não negativa, ou vazia se ausente |
| cover_pct | Cobertura vegetal 0–100%, ou vazia; documentar método/data em metadados |
| source_id | Chave de proveniência da observação; artigo não substitui arquivo-fonte |
| data_kind | observed ou synthetic |

Os campos obrigatórios de identificação, tempo, chuva, fonte e tipo não podem estar vazios. Não preencher faltantes com zero. `source_id=synthetic_example` nos exemplos não representa fonte científica. Incluir metadados adicionais em arquivos separados para dados reais: unidade da área, calibração, direitos, tratamento e resolução temporal. Não publicar coordenadas privadas para completar este modelo.
