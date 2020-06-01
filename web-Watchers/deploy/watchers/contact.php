<?php

    # Includes
    include_once('../secrets.php');

    # receive JSON POST
    $_POST = json_decode(file_get_contents('php://input'), true);

    # Receive page to check
    if ($_POST['page']){ // && ($_POST['g-recaptcha-response'] || $_POST['token'] )) {

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

        # Get page
        $url = $_POST['page'];

        if ($url > 100)
            die();

        # filter strange chars
        $url = preg_replace( '/.html$/', '', $url);
        $url = preg_replace( '/[^0-9A-z-\/]/', '', $url) . '.html';
        
        # Send page to Ademir
        $ch = curl_init();
        $fields = [
            'address' => 'http://watchers/check?token=' . $secret_admin . '&url=' . $url
        ];
        $fields_string = http_build_query($fields);
        
        curl_setopt($ch, CURLOPT_URL, "http://ademir:8080/ademir/dashboard");
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $fields_string);

        curl_exec($ch);

    } else {
       
        echo 'invalid captcha'; 
        
        die();
    }
    die();