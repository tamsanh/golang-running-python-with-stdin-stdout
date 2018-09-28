# Golang Running Python Examples

Examples of golang running python scripts via `exec.Command`.

Apologies in advance for the bad code.

## Silly Lessons Learned

1. `stdin` needs to be manually flushed on the python side

2. New lines need to be manually written to `stdin` to make sure the `readline` in python works.

## Running

Navigate to the chosen example, and simply run `go run main.go`.

All examples require `python3` on the executable `PATH`.

All webserver examples can be accessed by opening a webbrowswer, and navigating to `http://localhost:12001/`.

## Examples

### 1-basic-command

  This a simple example that demonstrates how to use golang to run `python3`, as well as consume its output.

### 2-command-arguments

This example implements a webservice wrapper around running a python script, passing webdata down into the python script via command-line arguments.

**Python Requirements**: `tkinter`


### 3-stdin-and-stdout

This example shows how one can communicate between python and golang, using standard in and out. A user can ask a question, and the question pops up in a long running python window. The user can then action on the window, and the response from the window is sent back to the original requesting webpage.

**Python Requirements**: `tkinter`

### 4-buffered-json-stdin

This example shows requests being buffered in golang, aggregated, and then submitted down into python via stdin to control a simple snake-clone.

**Python Requirements**: `tkinter` `Pillow`

## Next Step Ideas

1. Package `virtualenv` within built golang executables using something like `packr`.

2. Implement a simple system for continuous deployment of cron jobs.
