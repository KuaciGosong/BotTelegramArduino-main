import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

try:
    while True:
        # Meminta input dari pengguna
        user_input = input("Masukkan perintah (R1 ON/OFF, R2 ON/OFF, RS, RU): ")
        
        if user_input == 'R1 ON':
            ser.write(b'R1 ON\n')
        elif user_input == 'R1 OFF':
            ser.write(b'R1 OFF\n')
        elif user_input == 'R2 ON':
            ser.write(b'R2 ON\n')
        elif user_input == 'R2 OFF':
            ser.write(b'R2 OFF\n')
        elif user_input == 'RU':
            ser.write(b'RU\n')
            # time.sleep(1)
            ser.flushInput()
            response = ser.readline().decode().strip()
            print("Jarak Ultrasonik : ", response)
        elif user_input == 'RS':
            ser.write(b'RS\n')
            # time.sleep(1)
            ser.flushInput()
            response = ser.readline().decode().strip()
            print("Data Sensor DHT11 : ", response)
        else:
            print("Perintah tidak valid!")

except KeyboardInterrupt:
    ser.close() # Menutup koneksi serial saat program dihentikan
    print("Program dihentikan")