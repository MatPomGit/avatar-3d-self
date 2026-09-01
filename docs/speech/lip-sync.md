# Lip-sync

Lip-sync jest generowaniem krzywych twarzy z czasów fonemów i mapowania visemów.

## Pipeline

`WAV + phoneme timings → viseme targets → coarticulation → curves → jaw/lips/cheeks/tongue`

## Koartykulacja

Kształt ust dla bieżącego fonemu zależy od sąsiadów. Stosuj overlap czasowy, wyprzedzenie dla silnych artykulacji i wygładzanie oparte na czasie, nie prostą interpolację klatka-po-klatce.

## Walidacja

Oceniaj nagranie w normalnym tempie, w zwolnieniu i bez dźwięku. Zwarcia warg i duże otwarcia żuchwy muszą wypadać we właściwych momentach.