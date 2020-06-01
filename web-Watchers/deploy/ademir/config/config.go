package config

import (
	"github.com/kelseyhightower/envconfig"
)

// Config is a strutcture to set the server behavior
type Config struct {
	Port       string `envconfig: "PORT"`
	Flag       string `envconfig: "FLAG" required: "true"`
	BaseURL    string `envconfig: "BASEURL" required: "true"`
	Instances  int    `envconfig: "INSTANCES"`
	UseWebhook bool   `envconfig: "USEWEBHOOK" required:"true"`
	Debug      bool   `envconfig: "DEBUG"`
	Stay       int    `envconfig: "STAY"`
}

// Setup initialize bot configuration vars
func Setup() (*Config, error) {
	var c Config
	if err := envconfig.Process("", &c); err != nil {
		return &c, err
	}

	return &c, nil
}
