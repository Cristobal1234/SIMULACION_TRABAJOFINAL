## Issue relacionado
Closes #

## Equipo
<!-- Marca uno -->
- [ ] Engine
- [ ] Topologías
- [ ] Métricas
- [ ] UI

## Qué cambia
<!-- 2 o 3 líneas. Qué hace este PR, no cómo lo hace. -->

## Contratos de datos
- [ ] No modifica ningún contrato
- [ ] Modifica el contrato de **entrada** (configuración)
- [ ] Modifica el contrato de **salida** (resultado)

Si modifica alguno, describe el cambio y avisa a los líderes de los equipos que lo consumen:

## Cómo probarlo
<!-- Comandos o pasos para que el revisor lo verifique -->
```bash
pytest tests/
```

## Validación
<!-- Si aplica: contra qué caso conocido se verificó (ej. ejercicio 5.12 o 5.13) y qué resultado dio -->

## Checklist del autor
- [ ] Mi rama sigue el formato `feature/<equipo>-<tarea>`
- [ ] Mis commits usan prefijos `feat:`, `fix:` o `docs:`
- [ ] Las funciones nuevas tienen docstring
- [ ] Agregué o actualicé tests
- [ ] Los tests pasan en mi máquina
- [ ] No hay archivos que no correspondan al PR (datos temporales, `.env`, `__pycache__`)

## Revisión cruzada
Revisor asignado (líder del equipo que consume este trabajo): @

- Engine → revisa Topologías
- Topologías → revisa Engine
- Métricas → revisa UI
- UI → revisa Métricas
