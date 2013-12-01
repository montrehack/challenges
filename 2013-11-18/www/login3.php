<?php
require_once('ua.php');
session_start();
$info = (object)array();
$info->username = "login3";
$info->password = "u7wp1Yqv812pVo3";
$info->database = "login3";
$info->level	= "login3";
$error = "";
if(isset($_POST['username']) && isset($_POST['password'])) {
	$link = mysql_connect("127.0.0.1", $info->username, $info->password);
	mysql_select_db($info->database, $link);
	if(filter($_POST['username'])) {
		$result = mysql_query('SELECT * FROM users WHERE (username = \'' . $_POST['username'] . '\')');
		if(mysql_num_rows($result) != 0) {
			$errorContent = '';
			while(($user = mysql_fetch_assoc($result))) {
				if($user['password'] == $_POST['password']) {
					$_SESSION[$info->level] = true;
				}
			}
			$error = '<div class="error">Invalid username / password.</div>';
		} else {
			$error = '<div class="error">No user found.</div>';
		}
	} else {
		$error = '<div class="error">Illegal characters detected.</div>';
	}
}

function filter($string) {
	if(preg_match('/(union|char|sleep|benchmark)/i', $string)) {
		return false;
	}
	return true;
}
?>

<!DOCTYPE html>
<html>
	<head>
		<title>Login 3</title>	
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
			echo '<div class="flag">FLAG-vgnvokjmi3fgx0s23iv5x8n2w2</div>';
		} else { ?>	
		<section>
			<div class="title">
			Login portal 3			
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
