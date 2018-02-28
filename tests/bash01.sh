#!/bin/bash

# File descriptors:
# &0 stdin
# &1 stdout
# &2 stderr
# &3 to &9 for additional files

echo 'This is a test'
echo 'How does it do?'
echo 'error' >&2
echo 'This should not be printed' >&2