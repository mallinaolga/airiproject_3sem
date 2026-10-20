### Сгенерировать новые детали

### 10 деталей

```bash
cadgen gen --output ./generations/demo2 --n-train-samples 10 --n-val-samples 0 --n-folders 1 --max-workers 1
```

### 100 деталей

```bash
cadgen gen --output ./generations/demo100 --n-train-samples 100 --n-val-samples 0 --n-folders 1 --max-workers 1
```


### Найти возможные соединения

Для набора из **10 деталей**:

```bash
python -m cadgen.assembly_search --folder generations/demo2/train/0
```

Для набора из **100 деталей**:

```bash
python -m cadgen.assembly_search --folder generations/demo100/train/0
```



### Создать демонстрационную сборку

```bash
python -m cadgen.assembly_export
```