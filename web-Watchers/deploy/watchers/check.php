<?php   
    include('../secrets.php');

    # receive JSON POST
    $_POST = json_decode(file_get_contents('php://input'), true);

    # commenting all captcha stuff 
    if ($_POST['url']) { //&& ($_POST['g-recaptcha-response'] || $_POST['token'])) {
        $message = 'bot check';
        
        # as my bot doesn't know how to solve captchas i had to use this bypass
        // if (!($_POST['token'] && $_POST['token'] === $secret_admin)) {
            # Check recaptcha
            // $response = file_get_contents(
            //     "https://www.google.com/recaptcha/api/siteverify?secret=" . $recaptcha_secret . "&response=" .  $_POST['g-recaptcha-response'] . "&remoteip=" . $_SERVER['REMOTE_ADDR']
            // );
            // $response = json_decode($response);

            // # Captcha avaliation
            // if ($response->success !== true) {
            //     echo 'invalid captcha'; 
            //     die();
            // }

            // $message = 'user check';
    
        // }

        # Limit content size
        if (strlen($_POST['url']) > 100) {

            echo 'content is too long';
            die();

        } else {
            # filter strange chars
            $url = preg_replace( '/.html$/', '', $_POST['url']);
            $url = preg_replace( '/[^0-9A-z-\/]/', '', $url) . '.html';

            # retrieve wappalyzer result
            $json = check('http://localhost/' . $_POST['url']);

            # check if it fails
            if (strpos($json, 'Couldn\'t analyze your file') !== false) {
                echo $json;
                //die();

                die();
            }

            echo $json;
        
            die();
        }
    } else {       
        echo 'invalid captcha';
        
        die();
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