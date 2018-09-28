package main

import (
	"encoding/json"
	"html/template"
	"log"
	"net/http"
	"os/exec"
	"sync"
	"time"
)

func wormHTMLHandler(w http.ResponseWriter, r *http.Request) {
	t, _ := template.ParseFiles("templates/worm.html")
	var empty interface{}
	t.Execute(w, empty)
}

func main() {

	http.HandleFunc("/worm-api", wormStateHandler)
	http.HandleFunc("/", wormHTMLHandler)
	runWorm()

	log.Fatal(http.ListenAndServe("0.0.0.0:12001", nil))
}

type wormState struct {
	Directions map[string]string
	Lock       sync.Mutex
}

var ws = wormState{Directions: make(map[string]string)}

func wormStateHandler(w http.ResponseWriter, r *http.Request) {
	newDirection := r.FormValue("direction")
	wormID := r.FormValue("wormID")
	updateWormState(wormID, newDirection)
	w.Write([]byte("ok"))
}

func updateWormState(wormID string, direction string) {
	ws.Lock.Lock()
	defer ws.Lock.Unlock()
	ws.Directions[wormID] = direction
}

func runWorm() {
	cmd := exec.Command("python3", "python/worm.py")

	stdin, err := cmd.StdinPipe()
	if err != nil {
		panic(err)
	}

	writeState := func() {
		for {
			ws.Lock.Lock()
			js, err := json.Marshal(ws.Directions)
			ws.Lock.Unlock()
			if err != nil {
				panic(err)
			}
			stdin.Write(js)
			stdin.Write([]byte("\n"))
			time.Sleep(100 * time.Millisecond)
		}
	}

	go writeState()

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

}
