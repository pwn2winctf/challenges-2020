<?php
    include('../secrets.php');
    include('../weaponlyzer.php');

    # receive JSON POST
    $_POST = json_decode(file_get_contents('php://input'), true);
    
    if ($_POST['home'] && $_POST['about'] && $_POST['contact']){ // && ($_POST['g-recaptcha-response'] || $_POST['token'])) {

        # Check recaptcha
        // if (!($_POST['token'] && $_POST['token'] === $secret_admin)) {
        //     # Check recaptcha
        //     $response = file_get_contents(
        //         "https://www.google.com/recaptcha/api/siteverify?secret=" . $recaptcha_secret . "&response=" .  $_POST['g-recaptcha-response'] . "&remoteip=" . $_SERVER['REMOTE_ADDR']
        //     );
        //     $response = json_decode($response);

        //     # Captcha avaliation
        //     if ($response->success !== true) {
        //         echo 'invalid captcha'; 
        //         die();
        //     }
        // }

        # Create user sandboxed directory
        if (!file_exists($dir))
            mkdir($dir, 0777, true); 

        # Limit content size
        if (strlen($_POST['home']) > 1500 || strlen($_POST['about']) > 1500 || strlen($_POST['contact']) > 1500) {
            echo 'content is too long';

        # Block meta refresh tags
        } else if ((strpos(strtolower($_POST['home']), "refresh") !== false) || 
                        (strpos(strtolower($_POST['about']), "refresh") !== false) || 
                        (strpos(strtolower($_POST['contact']), "refresh") !== false)) {

            echo 'redirects are not allowed';
            
            die();
        } else {

            # create sandboxed files
            touch($file_home);
            $home = '<html><head><meta http-equiv="Content-Security-Policy" content="default-src \'none\';"></head><body>' . $_POST['home'] . '</body></html>';
            $handle = fopen($file_home, 'w+');
            fwrite($handle, $home);
            fclose($handle);

            touch($file_about);
            $about = '<html><head><meta http-equiv="Content-Security-Policy" content="default-src \'none\';"></head><body>' . $_POST['about'] . '</body></html>';
            $handle = fopen($file_about, 'w+');
            fwrite($handle, $about);
            fclose($handle);

            touch($file_contact);
            $contact = '<html><head><meta http-equiv="Content-Security-Policy" content="default-src \'none\';"></head><body>' . $_POST['contact'] . '</body></html>';
            $handle = fopen($file_contact, 'w+');
            fwrite($handle, $contact);
            fclose($handle);

            # retrieve wappalyzer result
            $json = weaponlyzer('http://localhost/' . $file_home, 'http://localhost/' . $file_about, 'http://localhost/' . $file_contact);

            # check if it fails
            if (strpos($json, 'Couldn\'t analyze your file') !== false) {
                echo $json;
            
                die();
            }


            echo $json;
            die();
        }
    } else {
       
        echo 'invalid captcha'; 
        die();
    }