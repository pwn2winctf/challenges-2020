package app

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/vrechson/ademir/config"
	"github.com/vrechson/ademir/worker"
)

// AdemirBot is the principal bot structure
type AdemirBot struct {
	conf    *config.Config
	browser *worker.Handler
}

// CreateApp initiates AdemirBot
func CreateApp(c *config.Config, t chan string) *AdemirBot {
	b := worker.Setup(t)

	return &AdemirBot{c, b}
}

// Navigate function handles http post
func (AdemirBot *AdemirBot) Navigate(w http.ResponseWriter, req *http.Request) {
	if req.Method == "POST" {
		if err := req.ParseForm(); err != nil {
			fmt.Fprintf(w, "ParseForm() err: %v", err)
			return
		}
		url := req.FormValue("address")
		AdemirBot.browser.AddQueue(url)

	}

}

// Start inializes Application
func (AdemirBot *AdemirBot) Start() {
	if AdemirBot.conf.UseWebhook == false {
		if len(os.Args) < 2 {
			log.Fatal("Usage: ./ademir url")
			os.Exit(0)
		}

		AdemirBot.browser.Navigate(os.Args[1], AdemirBot.conf)
		os.Exit(0)

	} else {
		go AdemirBot.browser.WorkController(AdemirBot.conf)
		http.HandleFunc("/ademir/dashboard", AdemirBot.Navigate)
		http.ListenAndServe(":"+AdemirBot.conf.Port, nil)

	}
}
