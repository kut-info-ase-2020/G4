from time import sleep
from modules import read_dht11_dat, LED, destroy

GREEN_LED_PIN = 17
YELLOW_LED_PIN = 5
RED_LED_PIN = 26

YELLOW_THRESH = 75
RED_THRESH = 85


def main():
    green_led = LED(GREEN_LED_PIN)
    yellow_led = LED(YELLOW_LED_PIN)
    red_led = LED(RED_LED_PIN)

    try:
        discomf_idx = 0
        while True:
            result = read_dht11_dat()
            if result:
                humid, temp = result

            discomf_idx = 0.81 * temp + 0.01 * humid * (0.99 * temp - 14.3) + 46.3

            if discomf_idx >= RED_THRESH:
                red_led.blick()
            elif discomf_idx >= YELLOW_THRESH:
                yellow_led.blick()
            else:
                green_led.blick()

            sleep(1)

    except KeyboardInterrupt:
        green_led.destroy()
        yellow_led.destroy()
        red_led.destroy()
        destory()

if __name__ == '__main__':
    main()

