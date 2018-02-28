#!/bin/bash

my_test () {
    echo 'hello, how are you?'
    echo 'this is an error' 1>&2
}

my_b () {
    tee b 1>&2
}

my_c () {
    tee c
    echo 'error' >&2
}

{ { { my_test 2>&3 | my_b; } 2>&4 3>&1 1>&5 | my_c; } 4>&1 | tee d; } 5>&1