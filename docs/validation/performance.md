# Walidacja wydajności

Wydajność mierzymy w reprezentatywnej scenie, po rozgrzaniu shaderów i cache. Jednorazowy pomiar FPS nie jest wystarczający.

## Profil desktop 60 FPS

Baseline frame budget: 16.67 ms.

- CPU animation + rig + facial evaluation: <=2.0 ms;
- GPU character rendering: <=8.0 ms;
- pozostawiony budżet sceny i silnika: >=6.67 ms.

Test trwa minimum 60 s po 10 s warm-up.

## Metryki

Raportujemy medianę, p95 i p99 frame time, CPU character time, GPU character time, peak VRAM, draw calls, triangles per visible LOD, active bones, active morph targets i texture residency.

## Progi

Dla profilu 60 FPS:

- median frame time <=16.67 ms;
- p95 <=20 ms;
- p99 <=33.3 ms;
- brak powtarzalnych hitchy >50 ms;
- brak ciągłego wzrostu pamięci podczas 5-minutowego soak testu.

P99 33.3 ms dopuszcza sporadyczną utratę pojedynczej klatki, ale nie może maskować stałego braku budżetu.

## Sceny testowe

1. close-up twarzy z mową i groomem;
2. full body locomotion z ubraniem i secondary motion;
3. zmiana LOD podczas dolly;
4. maksymalna kombinacja mimiki + gest + lip-sync.

## Sprzęt

Każdy wynik zapisuje CPU, GPU, RAM, rozdzielczość, backend graficzny, engine version i ustawienia jakości. Wynik bez tego kontekstu jest nieważny.