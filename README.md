# Tugas Besar IF3070 | Kelompok 37 - kelompoktigatujuh


Program untuk memilih dan menata kendaraan pada geladak kapal dengan memaksimalkan total shipping fee menggunakan algoritma local search: Hill Climbing, Simulated Annealing, dan Genetic Algorithm.

## Persyaratan
- python 3.10 atau lebih baru
- libary Matplotlib

## Instalasi Matplotlib
```bash
python -m pip install matplotlib
```

## Cara Menjalankan Program

dari root folder:

```bash
python -m src.main
```
atau
```bash
python -m src.main all
```

untuk menjalankan algoritma tertentu saja:

- hillclimbing
```bash
python -m src.main hc
```

- simulated annealing
```bash
python -m src.main sa
```

- genetic algorithm
```bash
python -m src.main ga
```

## Hasil Program

Hasil pencarian disimpan di folder `output/` berdasarkan algoritma masing-masing

## Struktur Repository

- `src/`: source code program.
- `docs/`: laporan PDF.
- `output/`: hasil eksperimen.

## Pembagian Tugas

|        Nama             |   NIM    |    Tugas             |
|-------------------------|----------|----------------------|
|Andreas Saputra Tambun   | 18224110 | Hill Climbing        |
|Ghaisan Nufail           | 18224090 | Simulated Annealing  |
|Daniel Wicaksana Godjali | 18224114 | Genetic Algorithm    |