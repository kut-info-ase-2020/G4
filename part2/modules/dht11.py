import RPi.GPIO as GPIO
import time
from .logger import get_logger


logger = get_logger(__name__)


class DHT11():
    STATE_INIT_PULL_DOWN = 1
    STATE_INIT_PULL_UP = 2
    STATE_DATA_FIRST_PULL_DOWN = 3
    STATE_DATA_PULL_UP = 4
    STATE_DATA_PULL_DOWN = 5

    def __init__(self, pin, max_unchange=100):
        self.pin = pin
        self.max_unchange = max_unchange

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.02)
        GPIO.setup(self.pin, GPIO.IN, GPIO.PUD_UP)

    def preprocess(self):
        self.setup()

    def read(self):
        self.preprocess()
        unchanged_count = 0
        last = -1
        data = []
        while True:
            current = GPIO.input(self.pin)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > self.max_unchange:
                    break

        state = self.STATE_INIT_PULL_DOWN

        lengths = []
        current_length = 0

        for current in data:
            current_length += 1

            if state == self.STATE_INIT_PULL_DOWN:
                if current == GPIO.LOW:
                    state = self.STATE_INIT_PULL_UP
                else:
                    continue
            if state == self.STATE_INIT_PULL_UP:
                if current == GPIO.HIGH:
                    state = self.STATE_DATA_FIRST_PULL_DOWN
                else:
                    continue
            if state == self.STATE_DATA_FIRST_PULL_DOWN:
                if current == GPIO.LOW:
                    state = self.STATE_DATA_PULL_UP
                else:
                    continue
            if state == self.STATE_DATA_PULL_UP:
                if current == GPIO.HIGH:
                    current_length = 0
                    state = self.STATE_DATA_PULL_DOWN
                else:
                    continue
            if state == self.STATE_DATA_PULL_DOWN:
                if current == GPIO.LOW:
                    lengths.append(current_length)
                    state = self.STATE_DATA_PULL_UP
                else:
                    continue
        if len(lengths) != 40:
            logger.info("Data not good, skip")
            return False

        shortest_pull_up = min(lengths)
        longest_pull_up = max(lengths)
        halfway = (longest_pull_up + shortest_pull_up) / 2
        bits = []
        the_bytes = []
        byte = 0

        for length in lengths:
            bit = 0
            if length > halfway:
                bit = 1
            bits.append(bit)
        logger.info("bits: %s, length: %d" % (bits, len(bits)))
        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if ((i + 1) % 8 == 0):
                the_bytes.append(byte)
                byte = 0
        logger.info(the_bytes)
        checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
        if the_bytes[4] != checksum:
            logger.info("Data not good, skip")
            return False

        return the_bytes
