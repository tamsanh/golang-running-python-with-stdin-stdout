package main

import (
	"bufio"
	"fmt"
	"io"
	"os/exec"
)

func main() {
	cmd := exec.Command("python3", "--version")

	stdout, err := cmd.StdoutPipe()

	if err != nil {
		panic(err)
	}

	stderr, err := cmd.StderrPipe()

	err = cmd.Start()

	if err != nil {
		panic(err)
	}

	go copyOutput(stdout)
	go copyOutput(stderr)
	err = cmd.Wait()
	if err != nil {
		panic(err)
	}
}

func copyOutput(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
}
