# Watchers
Welcome to Static Web Host! During all these years of static website development, Rebellious Fingers found out that the biggest hole in our security is the use of insecure third-party applications. To help our members mitigate this problem, and not be compromised by our enemies, we decided to implement a third-party app to help them identify which technologies their pages are running so they can check whether there is anything vulnerable before deployment.

Our service is still in beta, so please report any problems you find so our developers can analyze them.

weaponlyzer.php:
```PHP
<?php

    function weaponlyzer($home_url, $about_url, $contact_url) {
        # kill puppeteer orphans
        shell_exec("ps -elf | awk '{if ($5 == 1 && $3 != \"root\" && match($15,'puppeteer')) {print $4}}' | xargs kill -9");
        
        $targets = [$home_url, $about_url, $contact_url];
        $applications = [];
        $i = 0;

        for($i = 0; $i < 3; $i++) {
            $output = shell_exec('timeout -k 3s 20s wappalyzer -w 8 ' . escapeshellarg(escapeshellcmd($targets[$i])));
            $json = json_decode($output, true);

            if (json_last_error() === JSON_ERROR_NONE) {
            
                unlink(realpath(substr(parse_url($targets[$i])["path"], 1)));

                foreach ($json['applications'] as $tech) {

                    $entry = new class{};

                    $entry->name = $tech["name"];
                    $entry->version = $tech["version"];

                    $category = array_values($tech["categories"])[0];

                    if (!array_key_exists($category, $applications))
                        $applications[$category] = [];
                    
                        if(!in_array($entry, $applications[$category], false))
                            array_push($applications[$category], $entry);

                } 
            } elseif ($output == '') {
                return 'Couldn\'t analyze your file, please ask the admin to try weaponlyze in your page - URL: ' . substr(parse_url($targets[$i])["path"], 1);
            } else {
                unlink(realpath(substr(parse_url($targets[0])["path"], 1)));
                unlink(realpath(substr(parse_url($targets[1])["path"], 1)));
                unlink(realpath(substr(parse_url($targets[2])["path"], 1)));
            }
        
        }

        $json = json_encode($applications);
        return $json; 
    }

    function check($url) {

        $output = shell_exec('timeout -k 1s 8s wappalyzer -w 8 ' . escapeshellarg(escapeshellcmd($url)));
        $json = json_decode($output, true);
        $applications = [];

        if (json_last_error() === JSON_ERROR_NONE) {
    
            foreach ($json['applications'] as $tech) {

                $entry = new class{};

                $entry->name = $tech["name"];
                $entry->version = $tech["version"];

                $category = array_values($tech["categories"])[0];

                if (!array_key_exists($category, $applications))
                    $applications[$category] = [];
                
                    if(!in_array($entry, $applications[$category], false))
                        array_push($applications[$category], $entry);

            } 
            
        } elseif ($output == '') {
            return 'Couldn\'t analyze your file :(' . substr(parse_url($targets[$i])["path"], 1);
        }

        $json = json_encode($applications);
        return $json; 
    }
```

# Running it
`docker-compose build`

`docker-compose up`

environment will be running at http://localhost:31337