<?php
require_once('ua.php');
session_start();
$info = (object)array();
$info->username = "login6";
$info->password = "S33OAgWlJ9ks3ap";
$info->database = "login6";
$info->level	= "login6";
$error = "";
$username = "";
if(isset($_POST['username']) && isset($_POST['password'])) {
	$link = mysql_connect("127.0.0.1", $info->username, $info->password);
	$username = htmlspecialchars($_POST['username'], ENT_QUOTES);
	mysql_select_db($info->database, $link);
	if(filter($username)) {
		$result = mysql_query('SELECT * FROM users WHERE (username = \'' . urldecode($username) . '\')');
		if(mysql_num_rows($result) != 0) {
			$errorContent = '';
			while(($user = mysql_fetch_assoc($result))) {
				if($user['password'] == $_POST['password']) {
					$_SESSION[$info->level] = true;
				}
			}
		}
		$error = '<div class="error">Invalid username "' . urldecode($username) . '" / password.</div>';
	} else {
		$error = '<div class="error">Illegal characters detected.</div>';
	}
}

function filter($string) {
	if(preg_match('/(union|char|and|or\s\S|\s\S|sleep|sha1|md5|=)/i', $string)) {
		return false;
	}
	return true;
}
?>

<!DOCTYPE html>
<html>
	<head>
		<title>Login 6</title>	
	</head>
	<body>
		<style type="text/css">
			body {
				background-color: black;
			}	
			
			section {
				margin: auto;
				margin-top: 50px;				
				width: 533px;
				height: 310px;
				background-image: url(login.png);
				box-shadow: 0 0 10px white;
				border-radius: 5px;
				text-align: center;
			}	

			section .title {
				color: white;
				margin-left: 20px;
				padding-top: 20px;
				font-size: 0.50cm;
				font-weight: bold;			
			}

			.error {
				background-color: #950909;
				border: 3px solid #DB0000;
				padding: 7px;
				color: white;
				width: 500px;
				margin: auto;
				margin-top: 20px;
				text-align: center;
			}	

			section form {
				text-align: center;
				margin: auto;
				margin-top: 70px;
				width: 400px;
			}

			section form input {
				margin-bottom: 10px;
				padding: 7px;
				width: 350px;
			}
			
			section footer {
				margin-top: 25px;
				color: white;
				font-size: 0.3cm;
			}

			.flag {
				color: #65be00;
				width: 400px;
				margin: auto;
				margin-top: 50px;
				text-align: center;
			}
		</style>
		<?php if(isset($_SESSION[$info->level])) {
			echo '<div class="flag">FLAG-rqodljmved35lzrcwtxl2gnf57<br /><br /><font style="color: #a80000">Your done!  All challenges has been solved! Your a real SQL Injection ninja</font></div>';
		} else { ?>	
		<section>
			<div class="title">
			Login portal 6			
			</div>
			<form action="" method="post">
				<input type="text" placeholder="Username" name="username">
				<input type="password" placeholder="Password" name="password">
				<input type="Submit" value="Login">
			</form>
			<footer>Hackfest &copy; 2013</footer>
		</section>
		<?php echo $error; ?>
		<?php } ?>
	</body>
</html>
