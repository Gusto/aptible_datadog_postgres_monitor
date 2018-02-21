# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

"""
Disabled unix system checks.
"""

from checks import Check


class IO(Check):
    def check(self, agentConfig):
        return False


class FileHandles(Check):
    def check(self, agentConfig):
        return False


class Load(Check):
    def check(self, agentConfig):
        return False


class Memory(Check):
    def check(self, agentConfig):
        return False


class Processes(Check):
    def check(self, agentConfig):
        return False


class Cpu(Check):
    def check(self, agentConfig):
        return False


class System(Check):
    def check(self, agentConfig):
        return False


def main():
    print("System metrics are disabled on this system")


if __name__ == '__main__':
    main()
