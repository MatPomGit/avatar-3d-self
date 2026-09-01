# Praktyczne przykłady konwersji

## FBX → GLB: kompletna postać do viewera lub aplikacji WWW

```bash
python scripts/model_format_converter.py avatar.fbx avatar.glb \
  --textures embed \
  --animations keep
```

To jest preferowana konwersja, gdy model zawiera szkielet, blendshapes i animacje. GLB przechowuje geometrię, materiały PBR, tekstury i animację w jednym pliku, więc łatwo go przenieść albo opublikować.

## FBX → GLB z optymalizacją tekstur

```bash
python scripts/model_format_converter.py avatar.fbx avatar_web.glb \
  --textures embed \
  --texture-format jpeg \
  --max-texture-size 2048 \
  --animations keep
```

Tekstury większe niż 2048 px zostaną zmniejszone proporcjonalnie. JPEG ma sens głównie dla map bez przezroczystości, np. Base Color; do map z alfą lepszy jest PNG. Po takiej operacji trzeba wizualnie sprawdzić materiały, ponieważ kompresja JPEG może być niepożądana dla map technicznych, np. normal map.

## GLB → glTF: rozdzielenie jednego assetu na pliki

```bash
python scripts/model_format_converter.py avatar.glb avatar.gltf --textures copy
```

glTF jest wygodniejszy od GLB, gdy chcesz ręcznie podmieniać obrazy tekstur albo analizować strukturę assetu. Funkcjonalnie oba formaty potrafią przechowywać animowaną postać.

## GLB → FBX: przeniesienie do klasycznego pipeline DCC

```bash
python scripts/model_format_converter.py avatar.glb avatar.fbx --animations keep
```

Geometria, szkielet i animacje mogą zostać zachowane, ale materiały trzeba sprawdzić po imporcie. FBX i glTF mają inne modele opisu materiałów, więc idealna konwersja shaderów nie zawsze jest możliwa.

## FBX → OBJ: statyczna geometria z UV

```bash
python scripts/model_format_converter.py avatar.fbx avatar.obj
```

OBJ może zachować geometrię, UV i prostsze materiały, ale traci szkielet, skinning, blendshapes i animacje. Obok modelu może powstać plik MTL oraz osobne obrazy tekstur.

Jeżeli taka utrata danych ma być błędem, użyj:

```bash
python scripts/model_format_converter.py avatar.fbx avatar.obj --strict
```

## OBJ → STL: model do druku 3D

```bash
python scripts/model_format_converter.py bust.obj bust.stl --apply-transforms
```

STL zachowuje zasadniczo tylko geometrię. UV, tekstury i materiały nie są częścią tego formatu, więc wygląd wydruku wynika z materiału fizycznego i ustawień drukarki, a nie z materiału PBR modelu.

## STL → GLB

```bash
python scripts/model_format_converter.py scan.stl scan.glb
```

Konwersja utworzy plik GLB, ale nie „odtworzy” danych, których nie było w STL. GLB będzie zawierał geometrię, natomiast tekstury, UV, rig i animacje trzeba utworzyć osobno.
