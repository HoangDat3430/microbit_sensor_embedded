def on_data_received():
    global CMD
    CMD = serial.read_until(serial.delimiters(Delimiters.HASH))
    if CMD == "L1":
        pins.digital_write_pin(DigitalPin.P4, 1)
        pins.digital_write_pin(DigitalPin.P5, 0)
    elif CMD == "L0":
        pins.digital_write_pin(DigitalPin.P4, 0)
        pins.digital_write_pin(DigitalPin.P5, 1)
    elif CMD == "B0":
        pins.analog_write_pin(AnalogPin.P6, 0)
    elif CMD == "B1":
        pins.analog_write_pin(AnalogPin.P6, 100)
    elif CMD == "OPEN":
        pins.servo_write_pin(AnalogPin.P7, 180)
    elif CMD == "CLOSE":
        pins.servo_write_pin(AnalogPin.P7, 0)
    elif CMD == "P1":
        pins.digital_write_pin(DigitalPin.P8, 1)
    elif CMD == "P0":
        pins.digital_write_pin(DigitalPin.P8, 0)
serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)

Gas = 0
temperature = 0
CMD = ""
# pin 19 20 lcd
I2C_LCD1602.lcd_init(39)
I2C_LCD1602.backlight_on()
# fan
pins.digital_write_pin(DigitalPin.P5, 0)
pins.digital_write_pin(DigitalPin.P4, 0)
# buzzer 1 = on, 0 = off
pins.digital_write_pin(DigitalPin.P6, 0)
# servo close = 90, open = 180
pins.servo_write_pin(AnalogPin.P7, 0)
# relay 1 = on, 0 = off
pins.digital_write_pin(DigitalPin.P8, 0)

def on_forever():
    global temperature, Gas
    temperature = input.temperature()
    Gas = pins.analog_read_pin(AnalogPin.P1)
    basic.show_string("" + str((temperature)))
    I2C_LCD1602.show_string("Temp: ", 0, 0)
    I2C_LCD1602.show_string("Gas: ", 0, 1)
    I2C_LCD1602.show_number(temperature, 10, 0)
    I2C_LCD1602.show_number(Gas, 10, 1)
    serial.write_string("!TEMP:" + ("" + str(temperature)) + "#")
    serial.write_string("!GAS:" + ("" + str(Gas)) + "#")
    if temperature >= 60 or Gas < 500:
        pins.servo_write_pin(AnalogPin.P7, 180)
        pins.digital_write_pin(DigitalPin.P8, 0)
        pins.digital_write_pin(DigitalPin.P6, 1)
        pins.digital_write_pin(DigitalPin.P4, 1)
        pins.digital_write_pin(DigitalPin.P5, 0)
    else:
        pins.servo_write_pin(AnalogPin.P7, 0)
        pins.digital_write_pin(DigitalPin.P8, 1)
        pins.digital_write_pin(DigitalPin.P6, 0)
        pins.digital_write_pin(DigitalPin.P5, 1)
        pins.digital_write_pin(DigitalPin.P4, 0)
    basic.pause(5000)
basic.forever(on_forever)
