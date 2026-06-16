#!/bin/bash

set -euo pipefail

# The input for this script is the person.json file.
# TODO: Write a command to output the address of the person, all on one line, with a comma between each line.
jq -r '.address | join(", ")' ./person.json
# Your output should be exactly the string "35 Fashion Street, London, E1 6PX", but should not contain any quote characters.
