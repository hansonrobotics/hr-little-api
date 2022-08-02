#!/usr/bin/env python3
import atexit
import cmd
import logging
import os
import readline

from hr_little_api.robot import Robot

logger = logging.getLogger(__name__)


class CLI(cmd.Cmd, object):

    HISTFILE_SIZE = 1000

    def __init__(self):
        self.prompt = "robot > "
        super(CLI, self).__init__()
        self.api = Robot()
        self._user_dir = os.path.expanduser("~/.peclient")
        self.histfile = os.path.join(self._user_dir, ".history")
        self.input_lines = []
        if not self.api.connect():
            raise RuntimeError("Can't connect to the robot")
        self.robot_connected = True

    def default(self, line):
        try:
            if line:
                try:
                    self.api.say(line)
                except Exception as ex:
                    logger.error("Error %s", ex)
                self.stdout.write("\n")
        except Exception as ex:
            logger.exception(ex)

    def emptyline(self):
        pass

    def preloop(self):
        if readline and os.path.exists(self.histfile):
            readline.read_history_file(self.histfile)

    def postloop(self):
        if readline:
            readline.set_history_length(self.HISTFILE_SIZE)
            dir = os.path.dirname(self.histfile)
            if not os.path.isdir(dir):
                os.makedirs(dir)
            readline.write_history_file(self.histfile)

    def postcmd(self, stop, line):
        if not stop:
            self.input_lines.append(line)
        return stop

    def do_q(self, line=None):
        """
        Quit interactive console
        """
        if self.robot_connected:
            self.api.disconnect()
            print("Bye")
        return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cli = CLI()
    atexit.register(cli.do_q)
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        cli.postloop()
    except Exception as ex:
        cli.postloop()
        logger.exception(ex)
