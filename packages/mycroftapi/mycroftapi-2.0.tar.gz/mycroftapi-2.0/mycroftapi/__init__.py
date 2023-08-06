from websocket import create_connection, WebSocket


class MycroftAPI(object):
    def __init__(self, mycroft_ip):
        self.mycroft_ip = mycroft_ip
        self.url = "ws://" + self.mycroft_ip + ":8181/core"
        try:
            self._ws = create_connection(self.url)
        except OSError:
            print("Could not connect, verify ip.")
            return None

    def speak_text(self, text):
        mycroft_speak = ('"{}"'.format(text))
        mycroft_type = '"speak"'
        mycroft_data = '{"expect_response": false, "utterance": %s}, ' \
                       '"context": null' % mycroft_speak
        message = '{"type": ' + mycroft_type + \
                  ', "data": ' + mycroft_data + '}'
        self._ws.send(message)
        response = "Message Sent to Mycroft Instance: {}"\
            .format(self.mycroft_ip)
        return response

    def blink_eyes(self, side):
        """
        Used to blink eyes on a mark1 device, side can be values of:

        Args:
            side (str): 'r', 'l', or 'b' for 'right', 'left' or 'both'

        """
        mycroft_type = '"enclosure.eyes.blink"'
        mycroft_data = '{"side": "%s"}, ' \
                       '"context": null' % side
        message = '{"type": ' + mycroft_type + \
                  ', "data": ' + mycroft_data + '}'
        print(message)
        self._ws.send(message)
        response = "Sent command to mycroft to blink eye on side %s" % side
        return response

    def eyes_off(self):
        """
        Used to turn off eyes on mark1 device
        """
        mycroft_type = '"enclosure.eyes.off"'
        message = '{"type": ' + mycroft_type + '}'
        print(message)
        self._ws.send(message)
        response = "Sent command to mycroft to turn off  mark1 eyes"
        return response

    def eyes_on(self):
        """
        Used to turn on eyes on mark1 device.
        """
        mycroft_type = '"enclosure.eyes.on"'
        message = '{"type": ' + mycroft_type + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to turn on mark1 eyes"
        return response

    def reset_display(self):
        """
        Used to reset display of mark1 back to started state
        """
        mycroft_type = '"enclosure.reset"'
        message = '{"type": ' + mycroft_type + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to reset mark1 screen"
        return response

    def mute_speaker(self, mute):
        """
        Used to mute speaker on enclosure

        Args:
            mute (boolean): True or False - True to mute, False to unmute

        """
        if mute is True:
            mycroft_type = '"enclosure.system.mute"'
            mute_speaker = 'mute'
        else:
            mycroft_type = '"enclosure.system.unmute"'
            mute_speaker = 'unmute'
        message = '{"type": ' + mycroft_type + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to %s speaker" % mute_speaker
        return response

    def squint_eyes(self):
        """
        Used to make mark1 eyes look like a squint
        """
        mycroft_type = '"enclosure.eyes.narrow"'
        message = '{"type": ' + mycroft_type + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to squint eyes on mark1"
        return response

    def eyes_look(self, side):
        """
        Used to make eyes look to the given side:

        Args:
            side (str): 'r', 'l', 'u', 'd', or 'c' for

             'right', 'left' 'up', 'down' or 'crossed',

        """
        mycroft_type = '"enclosure.eyes.look"'
        mycroft_data = '{"side": "%s"}, ' \
                       '"context": null' % side
        message = '{"type": ' + mycroft_type + \
                  ', "data": ' + mycroft_data + '}'
        print(message)
        self._ws.send(message)
        response = "Sent command to mycroft have eyes look on side %s" % side
        return response

    def eyes_color(self, r, g, b):
        """
        Used to change color of eyes on mark1

        Args:
            r (int): 0-255, red value
            g (int): 0-255, green value
            b (int): 0-255, blue value
        """
        mycroft_type = '"enclosure.eyes.color"'
        mycroft_data = '{"r": %s, "g": %s, "b": %s}, ' \
                       '"context": null' % (r, g, b)
        message = '{"type": ' + mycroft_type + \
                  ', "data": ' + mycroft_data + '}'
        print(message)
        self._ws.send(message)
        response = "Sent command to mycroft have eyes change color"
        return response

    def eyes_brightness(self, level):
        """
        Used to change brightness level of eyes

        Args:
            level (int): 1-30, bigger numbers are brighter
        """
        mycroft_type = '"enclosure.eyes.level"'
        mycroft_data = '{"level": %s}, ' \
                       '"context": null' % level
        message = '{"type": ' + mycroft_type + \
                  ', "data": ' + mycroft_data + '}'
        print(message)
        self._ws.send(message)
        response = "Sent command to mycroft to adjust eye brightness"
        return response

    def eyes_reset(self):
        """
        Used to restore the eyes to their default state
        """
        mycroft_type = '"enclosure.eyes.reset"'
        message = '{"type": ' + mycroft_type + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to reset eyes"
        return response

    def mouth_reset(self):
        """
        Used to reset mouth to standard state
        """
        mycroft_type = '"enclosure.mouth.reset"'
        message = '{"type": ' + mycroft_type + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to reset mouth"
        return response

    def mouth_talk(self):
        """
        Used to show a generic talking animation
        """
        mycroft_type = '"enclosure.mouth.talk"'
        message = '{"type": ' + mycroft_type + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to start talk animation"
        return response

    def mouth_think(self):
        """
        Used to show thinking animation
        """
        mycroft_type = '"enclosure.mouth.think"'
        message = '{"type": ' + mycroft_type + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to start think animation"
        return response

    def mouth_listen(self):
        """
        Used to show listen animation
        """
        mycroft_type = '"enclosure.mouth.listen"'
        message = '{"type": ' + mycroft_type + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to start listen animation"
        return response

    def mouth_smile(self):
        """
        Used to show smile animation
        """
        mycroft_type = '"enclosure.mouth.smile"'
        message = '{"type": ' + mycroft_type + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to start smile animation"
        return response

    def mouth_text(self, text):
        """
        Used to display text scrolling if needed based on len

        Args:
            text (str): text string to display
        """
        mycroft_type = '"enclosure.mouth.text"'
        mycroft_data = '{"text": %s}, ' \
                       '"context": null' % text
        message = '{"type": ' + mycroft_type + \
                  ', "data": ' + mycroft_data + '}'
        self._ws.send(message)
        response = "Sent command to mycroft to display text %s" % text
        return response
