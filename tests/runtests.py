import os
import subprocess

dir = os.path.dirname(__file__)
parser = os.path.abspath(os.path.join(dir, "../src/szopinski-parser.py"))

input_files = [os.path.abspath(os.path.join(dir, f)) for f in os.listdir(dir) if "input" in f]
success_count = 0

for input_file in input_files:
    test_name = os.path.basename(input_file)
    test_name = test_name[:test_name.rfind(".input.txt")]

    grammar_file = input_file.replace("input", "grammar")
    output_file = input_file.replace("input", "output")

    command = ["python3", parser, grammar_file, input_file, "-f"]

    if input_file.endswith(".c.input.txt"):
        test_name = test_name[:test_name.rfind(".")]
        command.append("-c")

    print("Running test {}... ".format(test_name), end="")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = result.stdout.decode("utf-8")

    with open(output_file, "r") as f:
        desired_output = f.read()

    if result == desired_output:
        print("passed")
        success_count += 1
    else:
        print("failed")
        print(result)

if success_count == len(input_files):
    print("All tests passed")
else:
    print("{} out of {} tests passed".format(success_count, len(input_files)))
