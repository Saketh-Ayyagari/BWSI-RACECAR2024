import time

start = round(time.perf_counter())

while True:
   print(f'It has been {round(round(time.perf_counter(), 2) - start, 2)} seconds since the program first began')