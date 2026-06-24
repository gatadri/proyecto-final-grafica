import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')
django.setup()

from tareas.models import Nino, Skin, Sticker

def ajustar_economia():
    """
    Ajusta la economía del sistema para que las monedas tengan más impacto.
    """
    print("=" * 60)
    print("AJUSTANDO ECONOMÍA DEL SISTEMA DE MONEDAS")
    print("=" * 60)
    
    # 1. Ajustar precios de skins (más baratos para motivar compras)
    print("\n1. AJUSTANDO PRECIOS DE SKINS...")
    skins = Skin.objects.all()
    for skin in skins:
        if skin.rareza == 'comun':
            skin.precio = 50  # Antes podía ser más alto
        elif skin.rareza == 'raro':
            skin.precio = 150
        elif skin.rareza == 'legendario':
            skin.precio = 300
        skin.save()
    print(f"   OK - {skins.count()} skins actualizadas")
    print(f"     - Común: 50 monedas")
    print(f"     - Raro: 150 monedas")
    print(f"     - Legendario: 300 monedas")
    
    # 2. Ajustar precios de stickers
    print("\n2. AJUSTANDO PRECIOS DE STICKERS...")
    stickers = Sticker.objects.all()
    for sticker in stickers:
        if sticker.rareza == 'comun':
            sticker.precio = 30
        elif sticker.rareza == 'raro':
            sticker.precio = 80
        elif sticker.rareza == 'legendario':
            sticker.precio = 200
        sticker.save()
    print(f"   OK - {stickers.count()} stickers actualizados")
    print(f"     - Común: 30 monedas")
    print(f"     - Raro: 80 monedas")
    print(f"     - Legendario: 200 monedas")
    
    # 3. Dar monedas iniciales a niños que no tienen
    print("\n3. DANDO MONEDAS INICIALES...")
    ninos = Nino.objects.all()
    ninos_actualizados = 0
    for nino in ninos:
        if nino.monedas < 100:
            bonus = 100 - nino.monedas
            nino.monedas = 100  # Mínimo 100 monedas para empezar
            nino.save()
            ninos_actualizados += 1
            print(f"   OK - {nino.nombre}: +{bonus} monedas (Total: {nino.monedas})")
    
    if ninos_actualizados == 0:
        print("   OK - Todos los ninos ya tienen monedas suficientes")
    
    # 4. Mostrar estadísticas finales
    print("\n4. ESTADÍSTICAS DEL SISTEMA:")
    print("-" * 60)
    total_ninos = ninos.count()
    total_monedas_sistema = sum(n.monedas for n in ninos)
    promedio_monedas = total_monedas_sistema / total_ninos if total_ninos > 0 else 0
    
    print(f"   Total de niños: {total_ninos}")
    print(f"   Total monedas en el sistema: {total_monedas_sistema}")
    print(f"   Promedio por niño: {promedio_monedas:.0f} monedas")
    
    # Items más caros y baratos
    skin_cara = Skin.objects.order_by('-precio').first()
    skin_barata = Skin.objects.order_by('precio').first()
    sticker_caro = Sticker.objects.order_by('-precio').first()
    sticker_barato = Sticker.objects.order_by('precio').first()
    
    print(f"\n   Skin más cara: {skin_cara.nombre} - {skin_cara.precio} monedas")
    print(f"   Skin más barata: {skin_barata.nombre} - {skin_barata.precio} monedas")
    print(f"   Sticker más caro: {sticker_caro.nombre} - {sticker_caro.precio} monedas")
    print(f"   Sticker más barato: {sticker_barato.nombre} - {sticker_barato.precio} monedas")
    
    print("\n" + "=" * 60)
    print("ECONOMIA AJUSTADA EXITOSAMENTE")
    print("=" * 60)
    print("\nSISTEMA DE RECOMPENSAS:")
    print("   - Tarea completada: Puntos obtenidos en monedas")
    print("   - Tarea perfecta (0 errores): +50% bonus")
    print("   - Racha de dias: +2 monedas por dia (max 50)")
    print("   - Practica perfecta: +30% bonus")
    print("   - Logros desbloqueados: Bonus segun rareza")
    print("\nLos ninos ahora pueden:")
    print("   - Comprar skins comunes (50 monedas)")
    print("   - Comprar stickers (desde 30 monedas)")
    print("   - Coleccionar items legendarios (200-300 monedas)")
    print("   - Ver su progreso en monedas en dashboards")
    print("\nLas monedas ahora tienen un impacto real en el sistema!")

if __name__ == '__main__':
    ajustar_economia()
