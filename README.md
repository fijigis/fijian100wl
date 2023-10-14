# Fijian Language 100 Word List CLLD webb ap

## Requirements

- Python: 3.8+
- Dependencies: See [pyproject.toml](./pyproject.toml).

## Getting Started

After generating CLDF files at the `fijian100wl-cldf` repository, run the database initialization:

```shell
$ clld initdb development.ini --cldf ../../fijian100wl-cldf/fijian100wl/StructureDataset-metadata.json
```

Run the web server:

```shell
$ pserve --reload development.ini
```
