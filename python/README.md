# KuboERP · TDD, BDD y Calidad Ágil con Python

**Automatiza • Integra • Optimiza**

Solución del taller de TDD, BDD y calidad ágil con Python aplicada a los módulos de Compras,
Logística y Almacén de KuboERP (proveedores, cotizaciones, órdenes de compra e inventario).

## En Google Colab
1. Entra a https://colab.research.google.com y elige **Subir → KuboERP_TDD_BDD_Python.ipynb**.
2. Menú **Entorno de ejecución → Ejecutar todas**.

## En el computador
```
pip install -r requirements.txt
python -m pytest -v
python -m behave
python -m coverage run --source=kuboerp -m pytest
python -m coverage report -m
```

## Estructura
| Carpeta | Contenido |
|---|---|
| `kuboerp/` | Código de producción: proveedores, cotizaciones, órdenes e inventario |
| `tests/` | Pruebas unitarias con unittest y pytest (ejercicios 1, 2 y 4 y talleres 1 a 4) |
| `features/` | Escenarios Gherkin en español y step definitions de Behave (ejercicio 3 y talleres) |
