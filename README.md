# KuboERP

**Automatiza • Integra • Optimiza**

KuboERP es un ERP para una empresa que vende productos eléctricos y presta servicios eléctricos
residenciales, comerciales e industriales. Este repositorio contiene el **incremento** de los módulos de
**Compras, Logística y Almacén**: proveedores, cotizaciones, órdenes de compra e inventario, desarrollados
con **pruebas unitarias desde el primer minuto** (TDD) y escenarios de comportamiento en español (BDD).

| | |
|---|---|
| **Estudiante** | Oscar Javier Bello Daza |
| **Materia** | Proyecto de Ingeniería de Software II |
| **Profesor** | Carlos Eduardo Mujica Reyes |
| **Institución** | Universidad de Cundinamarca |

## ERP en Visual Studio (C# · ASP.NET Core · SQL Server)

Solución `dotnet/KuboERP.slnx` para **Visual Studio 2026**. El proyecto `KuboERP.Web` es una aplicación
**ASP.NET Core MVC (.NET 10)** con **Entity Framework Core** y **SQL Server LocalDB** que implementa los módulos del ERP
con las mismas reglas de negocio del dominio en Python:

| Módulo | Funcionalidades |
|---|---|
| Tablero gerencial | Compras del mes, valor del inventario, stock crítico, costo de nómina, alertas y últimos movimientos |
| Proveedores | CRUD con NIT único y válido; con historial no se elimina, queda INACTIVO |
| Cotizaciones | Solicitudes, cuadro comparativo, una cotización por proveedor, selección de la ganadora |
| Órdenes de compra | PENDIENTE → APROBADA (descuenta presupuesto) → RECIBIDA (entra al inventario); cancelación con justificación y auditoría |
| Inventario | CRUD, entradas y retiros, kárdex, stock crítico con cantidad sugerida |
| Empleados | CRUD por cargo y contrato, salario mínimo legal, desvinculación |
| Nómina | Liquidación mensual con normativa colombiana 2026 y desprendible por empleado |

Abrir la solución, elegir el perfil **https** y pulsar ▶. La base de datos se crea sola con datos de ejemplo; el perfil
**«Reiniciar datos de ejemplo»** la deja limpia. Guion del video: [`docs/4-sprint-3/Guion_video_KuboERP.md`](docs/4-sprint-3/Guion_video_KuboERP.md).

## Despliegue (Docker · Kubernetes · Azure)

**En producción:** https://kuboerp-web.agreeableglacier-e55852c8.spaincentral.azurecontainerapps.io
(Azure Container Apps + Azure SQL). Acta de cierre en [`docs/6-cierre/acta.md`](docs/6-cierre/acta.md).

La misma imagen Docker corre en local con **Docker Compose** (web + SQL Server 2022, http://localhost:8080), en un
clúster de **Kubernetes** (`kubectl apply -k k8s/`) y en **Azure Container Apps** con Azure SQL
(`deploy/azure/desplegar.ps1`). Sonda de salud en `/health`. Pasos completos en el
[manual de despliegue](docs/despliegue/manual-despliegue.md).

```
cd dotnet
cp .env.example .env      # cambiar SQL_SA_PASSWORD
docker compose up -d --build
```

## Gestión ágil

Cronograma de iteraciones, roles, Product Backlog y actas de cada sprint en [`docs/`](docs/README.md).
Arquitectura (arc42) en [`docs/arquitectura/arc42.md`](docs/arquitectura/arc42.md); infraestructura en `infra/terraform/`; CI en `.github/workflows/ci.yml`.
Tablero de seguimiento: **GitHub Projects · KuboERP · Scrum** (pestaña *Projects* del repositorio).

## Resultados de las pruebas

| Proyecto | Herramientas | Resultado |
|---|---|---|
| `python/` | unittest, pytest, Behave, coverage.py · Google Colab | 101 pruebas unitarias, 25 escenarios BDD (97 pasos), cobertura **100 %** |
| `java/` | JUnit 5, Mockito, Cucumber | 18 pruebas unitarias + 19 escenarios = **37 aprobadas** |
| `js/` | Jest | **15 aprobadas** |
| `dotnet/` | SpecFlow (Reqnroll), NUnit, FluentAssertions | **3 escenarios aprobados** |

Todas las pruebas se ejecutaron sin fallos. Las capturas están en `evidencias/` y `python/evidencias_colab/`.

## Estructura

```
kuboerp/
├── python/                 Taller TDD · BDD · Calidad ágil con Python (Google Colab)
│   ├── kuboerp/            Código de producción: proveedores, cotizaciones, órdenes, inventario
│   ├── tests/              Pruebas unitarias (unittest + pytest)
│   ├── features/           Escenarios Gherkin en español + step definitions de Behave
│   ├── KuboERP_TDD_BDD_Python.ipynb   Notebook listo para Google Colab
│   └── evidencias_colab/   Capturas de la ejecución en Colab
├── java/                   JUnit 5 + Cucumber (Maven)
├── js/                     Jest (Node.js)
├── dotnet/                 SpecFlow / Reqnroll (.NET 10)
├── reportes/               Reporte de pruebas con Font Awesome y reporte de Cucumber
├── evidencias/             Capturas de IntelliJ, Jest y .NET
└── Solucion_Taller_Pruebas_KuboERP.html   Documento de solución del taller de herramientas de prueba
```

## Reglas de negocio probadas

* **Proveedores:** NIT único y válido, correo con formato correcto, nombre obligatorio; no se elimina un
  proveedor con órdenes de compra activas (pasa a `INACTIVO`).
* **Cotizaciones:** solo sobre solicitudes `ABIERTA`, monto mayor que cero, una cotización por proveedor
  y solicitud; queda en estado `RECIBIDA`.
* **Órdenes de compra:** no pueden exceder el presupuesto del proveedor, no se aprueban dos veces y la
  aprobación descuenta el presupuesto.
* **Inventario:** código único, stock inicial ≥ 0, categoría obligatoria; no se retira más del stock
  disponible (`Stock insuficiente`).

## Cómo ejecutar

**Python (Google Colab):** subir `python/KuboERP_TDD_BDD_Python.ipynb` a https://colab.research.google.com
y usar *Entorno de ejecución → Ejecutar todas*. En el computador:

```
cd python
pip install -r requirements.txt
python -m pytest -v
python -m behave
python -m coverage run --source=kuboerp -m pytest
python -m coverage report -m
```

**Java:** `cd java` y `mvn test` (JDK 21 o superior).
**JavaScript:** `cd js`, `npm install` y `npm test`.
**.NET:** `cd dotnet/KuboERP.Specs` y `dotnet test`.

## Referencias

* Behave. (2026). *Tutorial*. https://behave.readthedocs.io/en/stable/tutorial/
* Cucumber. (2026). *Reference: Gherkin*. https://cucumber.io/docs/gherkin/reference/
* JUnit Team. (s. f.). *JUnit 5 User Guide*. https://junit.org/junit5/docs/current/user-guide/
* Pytest. (2026). *pytest: helps you write better programs*. https://docs.pytest.org/
* Python Software Foundation. (2026). *unittest — Unit testing framework*. https://docs.python.org/3/library/unittest.html
* Reqnroll. (2025). *SpecFlow end-of-life has been announced*. https://reqnroll.net/news/2025/01/specflow-end-of-life-has-been-announced/
