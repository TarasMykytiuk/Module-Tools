#!/bin/bash

set -euo pipefail

# The input for this script is the events-with-timestamps.txt file.
# TODO: Write a command to show how many times anyone has entered and exited.
awk '{print $3}' events-with-timestamps.txt | tail -n+2 | sort | uniq -c
# It should be clear from your script's output that there have been 5 Entry events and 4 Exit events.
# The word "Event" should not appear in your script's output.
