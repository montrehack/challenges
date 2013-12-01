<?php
if(isset($_SERVER['HTTP_USER_AGENT'])) {
	if(preg_match('/(sqlmap|havij)/i', $_SERVER['HTTP_USER_AGENT'])) {
		header('HTTP/1.0 404 Not Found');
		die();
	}
}
?>
