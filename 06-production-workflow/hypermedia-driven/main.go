package main

import (
	"fmt"
	"net/http"

	"github.com/a-h/templ"
)

func main() {
	// Serve static files (JS, etc.)
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("static"))))

	// Routes
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		templ.Handler(home()).ServeHTTP(w, r)
	})
	http.HandleFunc("/increment", func(w http.ResponseWriter, r *http.Request) {
		count := r.URL.Query().Get("count")
		newCount := 0
		fmt.Sscanf(count, "%d", &newCount)
		newCount++
		templ.Handler(counter(newCount)).ServeHTTP(w, r)
	})

	fmt.Println("Server running on :8080")
	http.ListenAndServe(":8080", nil)
}

// Home template (defined in home.templ)
func home() templ.Component {
	return Home()
}

// Counter template (defined in counter.templ)
func counter(count int) templ.Component {
	return Counter(count)
}