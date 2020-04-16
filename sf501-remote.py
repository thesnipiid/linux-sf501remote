import time
import pigpio

DATA_PIN    = 25     # BROADCOM number of the gpio pin connected to the 433.9MHz RX
PULSE_LEN   = 185    # the length of the pulse used in the SF501R protocol
PROTOCOL_ID = 0x1035 # ID used by the protocol, to be changed with yours ID.

class SF501R:
    frame_preamble = [pigpio.pulse(1<<DATA_PIN,0,1*PULSE_LEN),
                      pigpio.pulse(0,1<<DATA_PIN,14*PULSE_LEN)]

    frame_end      = [pigpio.pulse(1<<DATA_PIN,0,1*PULSE_LEN),
                      pigpio.pulse(0,1<<DATA_PIN,100*PULSE_LEN)]

    frame_bit_high = [pigpio.pulse(1<<DATA_PIN,0,1*PULSE_LEN),
                      pigpio.pulse(0,1<<DATA_PIN,7*PULSE_LEN),
                      pigpio.pulse(1<<DATA_PIN,0,1*PULSE_LEN),
                      pigpio.pulse(0,1<<DATA_PIN,2*PULSE_LEN)]

    frame_bit_low  = [pigpio.pulse(1<<DATA_PIN,0,1*PULSE_LEN),
                      pigpio.pulse(0,1<<DATA_PIN,2*PULSE_LEN),
                      pigpio.pulse(1<<DATA_PIN,0,1*PULSE_LEN),
                      pigpio.pulse(0,1<<DATA_PIN,7*PULSE_LEN)]

    def __init__(self):
        self.gpio = pigpio.pi() #create localhost connection with pigpiod daemon
        self.gpio.set_mode(DATA_PIN,pigpio.OUTPUT)

    def send_command(self,onoff,channel,repeat):
        id  = [0]*16
        cmd = [0]*4
        ch  = [0]*4

        # create the repeat loop
        start_loop = [255,0]
        # PREAMBLE
        self.gpio.wave_add_generic(self.frame_preamble)
        preamble = self.gpio.wave_create()

        # ID
        for i in range (0,16):
            if((PROTOCOL_ID >> (15 - i)) & 1):
                self.gpio.wave_add_generic(self.frame_bit_high)
                id[i] = self.gpio.wave_create()
            else:
                self.gpio.wave_add_generic(self.frame_bit_low)
                id[i] = self.gpio.wave_create()
        # RESERVED (8 bits at 0)
        self.gpio.wave_add_generic(self.frame_bit_low)
        reserved = self.gpio.wave_create()

        # CMD
        if onoff:
            for i in range(3):
                self.gpio.wave_add_generic(self.frame_bit_low)
                cmd[i] = self.gpio.wave_create()
            self.gpio.wave_add_generic(self.frame_bit_high)
            cmd[3] = self.gpio.wave_create()
        else:
            for i in range(4):
                self.gpio.wave_add_generic(self.frame_bit_low)
                cmd[i] = self.gpio.wave_create()

        # CHANNEL
        for i in range (0,4):
            if((channel >> (3 - i)) & 1):
                self.gpio.wave_add_generic(self.frame_bit_high)
                ch[i] = self.gpio.wave_create()
            else:
                self.gpio.wave_add_generic(self.frame_bit_low)
                ch[i] = self.gpio.wave_create()

        # END 
        self.gpio.wave_add_generic(self.frame_end)
        end = self.gpio.wave_create()
        # concatenate the entire frame

        # end the repeat loop
        end_loop = [255,1,repeat,0]
        command = start_loop + [preamble] + id + [255,0] + [reserved] + [255,1,8,0] + cmd + ch + [end] + end_loop 

        # send the command
        self.gpio.wave_chain(command)
        
        while self.gpio.wave_tx_busy():
            time.sleep(0.1)

        # clear the chained waveformes
        self.gpio.wave_clear()

        time.sleep(0.5)


tester = SF501R()
print("ON ch 1")
tester.send_command(True,1,2)
print("ON ch 2")
tester.send_command(True,2,2)
time.sleep(1)
print("OFF ch 1")
tester.send_command(False,1,2)
print("OFF ch 2")
tester.send_command(False,2,2)
