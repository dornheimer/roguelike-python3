import libtcodpy as libtcod

import textwrap


class Message:
    """Class for basic text message with a color."""

    def __init__(self, text, color=libtcod.lightest_sepia):
        self.text = text
        self.color = color


class MessageLog:
    """Message log with a buffer."""

    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height
        self.previous_message_color = libtcod.black

    def add_message(self, message):
        """
        Add message to log.

        Wraps messages to width and deletes lines when buffer is full.
        """
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        if message.color == self.previous_message_color:
            message.color = message.color * libtcod.light_grey
            self.previous_message_color = libtcod.black
        else:
            self.previous_message_color = message.color

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and color
            self.messages.append(Message(line, message.color))
