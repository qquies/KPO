#!/usr/bin/env python3
"""Тест симуляций устройств для этапа 1"""

import sys
import time
sys.path.insert(0, 'src')

from devices.climate.thermostat import Thermostat
from devices.lighting.smart_light import SmartLight
from devices.security.security_camera import SecurityCamera

print("=" * 60)
print("ТЕСТ СИМУЛЯЦИЙ УСТРОЙСТВ - ЭТАП 1")
print("=" * 60)

# Создаем устройства
thermostat = Thermostat("thermostat", "Термостат")
lamp = SmartLight("lamp", "Умная лампа")
camera = SecurityCamera("camera", "Камера безопасности")

# Включаем устройства
print("\n1. Включаем устройства...")
thermostat.turn_on()
lamp.turn_on()
camera.turn_on()

print(f"   Термостат: {thermostat.state}, температура: {thermostat.temperature}°C")
print(f"   Лампа: {lamp.state}, яркость: {lamp.data['brightness']}%")
print(f"   Камера: {camera.state}, запись: {camera.recording}")

# Запускаем симуляции несколько раз
print("\n2. Запускаем симуляции (10 итераций)...")
for i in range(10):
    print(f"\n   Итерация {i+1}:")
    
    # Симуляция термостата
    old_temp = thermostat.temperature
    thermostat._simulate_temperature()
    if abs(thermostat.temperature - old_temp) > 0.1:
        print(f"   Термостат: {old_temp:.1f}°C → {thermostat.temperature:.1f}°C")
    
    # Симуляция лампы
    old_brightness = lamp.data['brightness']
    lamp._simulate_brightness()
    if abs(lamp.data['brightness'] - old_brightness) > 1:
        print(f"   Лампа: {old_brightness}% → {lamp.data['brightness']}%")
    
    # Симуляция камеры
    old_motion = camera.data.get('motion_detected', False)
    camera._simulate_motion_detection()
    if camera.data.get('motion_detected', False) != old_motion:
        print(f"   Камера: движение {'обнаружено' if camera.data['motion_detected'] else 'не обнаружено'}")
    
    time.sleep(0.5)

print("\n" + "=" * 60)
print("ТЕСТ ЗАВЕРШЕН!")
print("=" * 60)
print(f"\nФинальные значения:")
print(f"   Термостат: {thermostat.temperature:.1f}°C")
print(f"   Лампа: {lamp.data['brightness']}%")
print(f"   Камера: движение {'обнаружено' if camera.data.get('motion_detected') else 'не обнаружено'}")
