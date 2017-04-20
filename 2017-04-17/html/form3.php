<?php session_start(); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<head>
    <title>Human Verification Step I </title>
<style type="text/css">
captcha { font-family: sans-serif; font-size: 0.8em; padding: 20px; }
#result { border: 1px solid green; width: 300px; margin: 0 0 35px 0; padding: 10px 20px; font-weight: bold; }
#change-image { font-size: 0.8em; }
</style>
</head>
<body onload="document.getElementById('captcha-form').focus()">
This flag is only availlable to humans <p />
Please prove you are a human to obtain your flag<p />
<br><br><br><br><br><br>
<p><strong>Write the following word:</strong></p>

<form method="POST" id="Form1" action="captcha2.php">
<img src="captcha/captcha.php?new" id="captcha" /><br/>
<a href="#" onclick="
    document.getElementById('captcha').src='captcha/captcha.php';
    document.getElementById('captcha-form').focus();"
    id="change-image">Not readable? Change text.</a><br/><br/>


<input type="text" name="captcha" id="captcha-form" value='Write here' /><br/>
<input type="submit" />
</form>
<a href="/captcha2.txt">Code</a>
</body>
</html>
