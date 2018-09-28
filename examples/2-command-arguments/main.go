package main

import (
	"html/template"
	"log"
	"net/http"
	"os/exec"
	"strings"
)

func submitAlertHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		alertText := r.FormValue("alert_text")
		if strings.Trim(alertText, " ") != "" {
			go popupAlert(alertText)
		}
	}
	t, _ := template.ParseFiles("templates/submit_alert.html")
	var empty interface{}
	t.Execute(w, empty)
}

func main() {
	http.HandleFunc("/submit_alert", submitAlertHandler)
	http.HandleFunc("/", submitAlertHandler)
	log.Fatal(http.ListenAndServe("0.0.0.0:12001", nil))
}

func popupAlert(message string) {
	cmd := exec.Command("python3", "python/alert.py", message)

	cmd.Start()
	cmd.Wait()
}
