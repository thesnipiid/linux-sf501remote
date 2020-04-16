import time
import pigpio

PULSE_LEN   = 185    # the length of the pulse used in the SF501R protocol

class SF501R:
    max_devices = 4

    def __init__(self,id,pin=25):
        self.protocol_id = id
        self.data_pin = pin
        self.gpio = pigpio.pi()                         #create localhost connection with pigpiod daemon
        self.gpio.set_mode(self.data_pin,pigpio.OUTPUT) # Set the data pin as output
        self._init_precompiled_frames()

    def set_max_devices(max):
        self.max_devices = max

    def _init_precompiled_frames(self):
        """
        This function is not supposed to be called by user.
        It compute some "pre-compiled" waves.
        """
        self.frame_preamble = [pigpio.pulse(1<<self.data_pin,0,1*PULSE_LEN),
                               pigpio.pulse(0,1<<self.data_pin,14*PULSE_LEN)]

        self.frame_end      = [pigpio.pulse(1<<self.data_pin,0,1*PULSE_LEN),
                               pigpio.pulse(0,1<<self.data_pin,100*PULSE_LEN)]

        self.frame_bit_high = [pigpio.pulse(1<<self.data_pin,0,1*PULSE_LEN),
                               pigpio.pulse(0,1<<self.data_pin,7*PULSE_LEN),
                               pigpio.pulse(1<<self.data_pin,0,1*PULSE_LEN),
                               pigpio.pulse(0,1<<self.data_pin,2*PULSE_LEN)]

        self.frame_bit_low  = [pigpio.pulse(1<<self.data_pin,0,1*PULSE_LEN),
                               pigpio.pulse(0,1<<self.data_pin,2*PULSE_LEN),
                               pigpio.pulse(1<<self.data_pin,0,1*PULSE_LEN),
                               pigpio.pulse(0,1<<self.data_pin,7*PULSE_LEN)]

    def send_command(self,onoff,channel,repeat=4):
        """
        This is the main function used to send command to a
        socket.
        onoff   -> Boolean -> True : ON , False : OFF
        channel -> 4 bits  -> the socket to command
        repeat  -> int     -> the number of time that the entire command need to be repeated
        """
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
            if((self.protocol_id >> (15 - i)) & 1):
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

    def switch_all(self,onoff,repeat=4):
        for y in range(repeat):
            for i in range(0,self.max_devices):
                self.send_command(onoff,i,1)


