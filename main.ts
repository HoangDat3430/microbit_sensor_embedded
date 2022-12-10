let Gas = 0
let temperature = 0
// pin 19 20 lcd
I2C_LCD1602.LcdInit(39)
I2C_LCD1602.on()
I2C_LCD1602.BacklightOn()
// buzzer 1 = on, 0 = off
pins.digitalWritePin(DigitalPin.P5, 0)
// relay 1 = on, 0 = off
pins.digitalWritePin(DigitalPin.P8, 0)
// relay 1 = on, 0 = off
pins.digitalWritePin(DigitalPin.P2, 0)
basic.forever(function () {
    temperature = input.temperature()
    Gas = pins.analogReadPin(AnalogPin.P1)
    basic.showString("" + temperature)
    I2C_LCD1602.ShowString("!1:TEMP:", 0, 0)
    I2C_LCD1602.ShowString("!1:GAS: ", 0, 1)
    I2C_LCD1602.ShowNumber(temperature, 10, 0)
    I2C_LCD1602.ShowNumber(Gas, 10, 1)
    serial.writeString("!TEMP:" + ("" + temperature) + "#")
    serial.writeString("!GAS:" + ("" + Gas) + "#")
    if (temperature >= 60) {
        pins.digitalWritePin(DigitalPin.P5, 1)
        pins.digitalWritePin(DigitalPin.P2, 1)
    } else if (Gas > 650) {
        pins.digitalWritePin(DigitalPin.P5, 1)
        pins.digitalWritePin(DigitalPin.P8, 1)
    } else {
        pins.digitalWritePin(DigitalPin.P8, 0)
        pins.digitalWritePin(DigitalPin.P2, 0)
        pins.digitalWritePin(DigitalPin.P5, 0)
    }
    basic.pause(5000)
    I2C_LCD1602.clear()
})
