#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script principal para ejecutar la consolidación de datos RENIEC

Uso:
    python main.py                    # Ejecutar consolidación
    python main.py --help             # Ver opciones
"""

import click
import sys
import os

# Agregar carpeta del proyecto al PATH para imports
if __name__ == '__main__':
    # Cuando se ejecuta directamente
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)

try:
    from analisis_reniec.consolidacion.pipeline import ejecutar_consolidacion
    from analisis_reniec.config import PROJECT_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR
except ImportError:
    # Fallback para ejecución directa
    from consolidacion.pipeline import ejecutar_consolidacion
    from config import PROJECT_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR

@click.group()
def cli():
    """RENIEC-ETL: Herramienta de consolidación de datos"""
    pass

@cli.command()
def consolidar():
    """Ejecuta el proceso de consolidación de datos"""
    click.echo("="*80)
    click.echo("EJECUTANDO CONSOLIDACIÓN DE DATOS RENIEC")
    click.echo("="*80)
    
    try:
        success = ejecutar_consolidacion()
        if success:
            click.echo("\n[EXITO] Consolidación completada correctamente")
            sys.exit(0)
        else:
            click.echo("\n[ERROR] La consolidación falló")
            sys.exit(1)
    except Exception as e:
        click.echo(f"\n[ERROR] {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def info():
    """Muestra información del proyecto"""
    click.echo("\n" + "="*80)
    click.echo("INFORMACIÓN DEL PROYECTO RENIEC-ETL")
    click.echo("="*80)
    click.echo(f"\nRaíz del proyecto:      {PROJECT_DIR}")
    click.echo(f"Datos crudos (entrada): {RAW_DATA_DIR}")
    click.echo(f"Datos procesados (salida): {PROCESSED_DATA_DIR}")
    click.echo("\n" + "="*80 + "\n")

if __name__ == '__main__':
    cli()
