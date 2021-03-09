import subprocess
import sys

MAX_READLINES = 1000


class Sinks:

    def __init__(self, sink_commands):
        self.sinks = []
        self.lines_sent = 0
        for param in sink_commands:
            print(f'Executing: {param}')
            self.sinks.append(subprocess.Popen(param.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT))

    def write_lines(self, lines):
        self.lines_sent += len(lines)
        encoded_lines = [line.encode('utf-8') for line in lines]
        [sink.stdin.writelines(encoded_lines) for sink in self.sinks]


sinks = Sinks(sys.argv[1:])

input_lines = sys.stdin.readlines(MAX_READLINES)
while input_lines:
    sinks.write_lines(input_lines)
    input_lines = sys.stdin.readlines(MAX_READLINES)

print(f"{sinks.lines_sent} lines sent")
