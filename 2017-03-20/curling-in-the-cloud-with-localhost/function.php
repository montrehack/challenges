<?php

function in_cidr($cidr, $ip) {
        list($prefix, $mask) = explode("/", $cidr);

        return 0 === (((ip2long($ip) ^ ip2long($prefix)) >> $mask) << $mask);
}

function get_contents($url) {
        $disallowed_cidrs = [ "127.0.0.1/24", "169.254.0.0/16", "0.0.0.0/8" ];

        do {
                $url_parts = parse_url($url);

                if ($_POST['debug'] == "true"){
                        var_dump($url_parts);
                }
                if (!array_key_exists("host", $url_parts)) {
                        die("<p><h3 >There was no host in your url!</h3></p>");
                }

                $host = $url_parts["host"];

                if (filter_var($host, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
                        $ip = $host;
                } else {
                        $ip = dns_get_record($host, DNS_A);
                        if (count($ip) > 0) {
                                $ip = $ip[0]["ip"];
                        } else {
                                die("<p><h3 >Your host couldn't be resolved man...</h3></p>");
                        }
                }

                foreach ($disallowed_cidrs as $cidr) {
                        if (in_cidr($cidr, $ip)) {
                                die("<p><h3>That IP is a blacklisted cidr ({$cidr})!</h3></p>");
                        }
                }

                // all good, curl now
                $curl = curl_init();
                curl_setopt($curl, CURLOPT_URL, $url);
                curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
                curl_setopt($curl, CURLOPT_MAXREDIRS, 0);
                curl_setopt($curl, CURLOPT_TIMEOUT, 3);
                curl_setopt($curl, CURLOPT_PROTOCOLS, CURLPROTO_ALL
                        & ~CURLPROTO_FILE
                        & ~CURLPROTO_SCP); // no files plzzz
                curl_setopt($curl, CURLOPT_RESOLVE, array($host.":".$ip)); // no dns rebinding plzzz	
                $data = curl_exec($curl);

                if (!$data) {
                        die("<p><h3 style=color:red>something went wrong....</h3></p>");
                }

                if (curl_error($curl) && strpos(curl_error($curl), "timed out")) {
                        die("<p><h3 style=color:red>Timeout!! thats a slowass  server</h3></p>");
                }

                // check for redirects
                $status = curl_getinfo($curl, CURLINFO_HTTP_CODE);
                if ($status >= 301 and $status <= 308) {
                        $url = curl_getinfo($curl, CURLINFO_REDIRECT_URL);
                } else {
                        return $data;
                }

        } while (1);
}
?>
