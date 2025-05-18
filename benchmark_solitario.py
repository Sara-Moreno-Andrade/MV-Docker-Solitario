import time
import psutil
import subprocess

start = time.time()

# Ejecutar el juego
proc = subprocess.Popen(["python", "solitario/solitario.py"])

# Esperar 10 segundos y tomar métricas
time.sleep(10)
p = psutil.Process(proc.pid)

cpu = p.cpu_percent()
ram = p.memory_info().rss / 1024 ** 2
end = time.time()
tiempo_total = end - start

print(f"CPU: {cpu}%")
print(f"RAM usada: {ram:.2f} MB")
print(f"Tiempo total: {tiempo_total:.2f} segundos")

# Guardar en CSV
import os
os.makedirs("results", exist_ok=True)

modo = "docker" if os.environ.get("DOCKER_ENV") else "vm"
ruta = f"results/benchmark_{modo}.csv"

with open(ruta, "a") as f:
    f.write(f"{tiempo_total:.2f}, {ram:.2f}, {cpu:.2f}\n")

proc.terminate()
