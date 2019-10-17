# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MMA8452Q
# This code is designed to work with the MMA8452Q_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=MMA8452Q_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# MMA8452Q address, 0x1C(28)
# Select Control register, 0x2A(42)
#               0x00(00)        StandBy mode
bus.write_byte_data(0x1D, 0x2A, 0x00)
# MMA8452Q address, 0x1C(28)
# Select Control register, 0x2A(42)
#               0x01(01)        Active mode
bus.write_byte_data(0x1D, 0x2A, 0x01)
# MMA8452Q address, 0x1C(28)
# Select Configuration register, 0x0E(14)
#               0x00(00)        Set range to +/- 2g
bus.write_byte_data(0x1D, 0x0E, 0x00)

m = 0

with open("accelerometer.log", "a") as f:  
    f.write("Meassuring stuf:\n")
    while m < 1000:
        time.sleep(0.5)

        # MMA8452Q address, 0x1C(28)
        # Read data back from 0x00(0), 7 bytes
        # Status register, X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
        data = bus.read_i2c_block_data(0x1D, 0x00, 7)

        # Convert the data
        xAccl = (data[1] * 256 + data[2]) / 16

        yAccl = (data[3] * 256 + data[4]) / 16

        zAccl = (data[5] * 256 + data[6]) / 16

        # Output data to screen
        print("Acceleration in X-Axis : %d" %xAccl)
        print("Acceleration in Y-Axis : %d" %yAccl)
        print("Acceleration in Z-Axis : %d" %zAccl)
        print(m)

        f.write(str(xAccl)+";"+str(yAccl)+";"+str(zAccl)+"\n")

        m += 1
    f.close