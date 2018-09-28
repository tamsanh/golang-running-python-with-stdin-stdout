package main

import (
	"bufio"
	"html/template"
	"io"
	"log"
	"net/http"
	"os/exec"
	"strings"
	"sync"
)

func generateAskQuestionHandler(writeQuestion func(string, http.ResponseWriter, chan struct{})) func(http.ResponseWriter, *http.Request) {
	submitQuestion := func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "POST" {
			questionText := r.FormValue("question_text")
			if strings.Trim(questionText, " ") != "" {
				responseWasWritten := make(chan struct{})
				writeQuestion(questionText, w, responseWasWritten)
				<-responseWasWritten
			}
		} else {
			t, _ := template.ParseFiles("templates/ask_question.html")
			var empty interface{}
			t.Execute(w, empty)
		}
	}
	return submitQuestion
}

func main() {

	writeQuestion := runQuestionAnswerer()
	askQuestionHandler := generateAskQuestionHandler(writeQuestion)
	http.HandleFunc("/ask_question", askQuestionHandler)
	http.HandleFunc("/", askQuestionHandler)
	log.Fatal(http.ListenAndServe("0.0.0.0:12001", nil))
}

type resp struct {
	Writer             http.ResponseWriter
	ResponseWasWritten chan struct{}
}

func runQuestionAnswerer() func(string, http.ResponseWriter, chan struct{}) {
	cmd := exec.Command("python3", "python/ask.py")

	responseWriters := make(chan *resp, 1000)

	stdin, err := cmd.StdinPipe()
	if err != nil {
		panic(err)
	}

	var askQuestionLock = sync.Mutex{}

	writeQuestion := func(question string, rw http.ResponseWriter, responseWasWritten chan struct{}) {
		askQuestionLock.Lock()
		defer askQuestionLock.Unlock()
		stdin.Write([]byte(question + "\n"))
		responseWriters <- &resp{
			Writer:             rw,
			ResponseWasWritten: responseWasWritten,
		}
	}

	stdout, err := cmd.StdoutPipe()
	receiveQuestion := func(stdout io.ReadCloser) {
		scanner := bufio.NewScanner(stdout)
		for scanner.Scan() {
			res := <-responseWriters
			type PageAnswer struct {
				Answer string
			}
			pa := &PageAnswer{
				Answer: scanner.Text(),
			}
			t, _ := template.ParseFiles("templates/ask_question.html")
			t.Execute(res.Writer, pa)
			res.ResponseWasWritten <- struct{}{}
		}
	}

	go receiveQuestion(stdout)

	go func(cmd *exec.Cmd) {
		var err = cmd.Start()
		if err != nil {
			panic(err)
		}

		err = cmd.Wait()
		if err != nil {
			panic(err)
		}
	}(cmd)

	return writeQuestion
}
