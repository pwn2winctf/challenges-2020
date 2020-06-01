package worker

import (
	"fmt"
	"log"
	"net/http"
	"net/url"
	"sync"
	"time"

	"github.com/sclevine/agouti"
	"github.com/vrechson/ademir/config"
)

// Handler handles pages navigation
type Handler struct {
	targets *chan string
}

// Setup instantiate a new Handler
func Setup(t chan string) *Handler {
	return &Handler{&t}
}

// Navigate access a new URL
func (H *Handler) Navigate(target string, c *config.Config) {

	u, err := url.Parse(target)
	if err != nil {
		log.Fatal(err)
	}

	// Instantiate a Chrome Driver
	driver := agouti.ChromeDriver(
		agouti.ChromeOptions("args", []string{"--headless", "--no-sandbox"}),
	)

	// Start the Driver
	if err := driver.Start(); err != nil {
		log.Fatal("Failed to start driver:", err)
	}

	// Create new page
	page, err := driver.NewPage()
	if err != nil {
		log.Fatal("Failed to open page:", err)
	}

	// Navigate to the challenge base to set cookies
	if err := page.Navigate(u.Scheme + "://" + u.Host + "/"); err != nil { // the only way i could set cookies
		log.Fatal("Failed to navigate:", err)
	}

	// Set page load timeout
	page.SetPageLoad(15000)

	// Set the cookies
	page.SetCookie(&http.Cookie{
		Name:  "FLAG",
		Value: c.Flag,
	})

	if c.Debug == true {
		fmt.Println("[Worker " + (time.Now()).String() + " ] Navigating to " + target)
	}

	// Navigate to XSS vulnerable page
	if err := page.Navigate(u.String()); err != nil {
		log.Fatal("Failed to navigate:", err)
	}

	if c.Debug == true {
		fmt.Println("[Worker " + (time.Now()).String() + " ] Navigation ended to " + target)
	}

	// Stay in page for some time
	time.Sleep(time.Duration(c.Stay) * time.Second)

	// Close web driver
	if err := driver.Stop(); err != nil {
		log.Fatal("Failed to close pages and stop WebDriver:", err)
	}

}

// worker is a function to receive and navigate into multiples urls
func (H *Handler) worker(jobs <-chan string, c *config.Config) {
	for u := range jobs {
		H.Navigate(u, c)
	}

}

// WorkController is a function that control workers in order to navigate to pages with concorrence
func (H *Handler) WorkController(c *config.Config) {
	var wg sync.WaitGroup
	wg.Add(1)
	defer wg.Done() // remains open forever

	for i := 0; i < c.Instances; i++ {
		go H.worker(*H.targets, c)
	}

	wg.Wait()
}

// AddQueue add an url to process queue
func (H *Handler) AddQueue(url string) {
	*H.targets <- url
}
