import RPi.GPIO as GPIO

from time import sleep
from modules import read_dht11_dat, LED, destroy, get_logger
from utils import compute_discomfort_index

GREEN_LED_PIN = 17
YELLOW_LED_PIN = 5
RED_LED_PIN = 26

YELLOW_THRESH = 75
RED_THRESH = 85

logger = get_logger(__name__)


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
                discomf_idx = compute_discomfort_index(temp, humid)

            logger.info('discomfort index: {}'.format(discomf_idx))

            if discomf_idx >= RED_THRESH:
                red_led.on()
                green_led.off()
                yellow_led.off()
            elif discomf_idx >= YELLOW_THRESH:
                yellow_led.on()
                green_led.off()
                red_led.off()
            else:
                green_led.on()
                red_led.off()
                yellow_led.off()

            sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()

