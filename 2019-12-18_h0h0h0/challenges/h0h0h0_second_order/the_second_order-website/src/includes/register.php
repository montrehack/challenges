<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$id = $_POST["userID"];
	$pass = $_POST["password"];
	if (isset($id) && isset($pass)
		&& 2 <= strlen($id) && strlen($id) <= 256
		&& 2 <= strlen($pass) && strlen($pass) <= 256) {

		include("mysql_connection.php");
		$mysqli = getConnection();
		if ($mysqli->connect_errno) {
			echo "Errno: " . $mysqli->connect_errno . "\n";
			echo "Error: " . $mysqli->connect_error . "\n";
			die();
		}
		$query = $mysqli->prepare("INSERT INTO users(username, password, ip, session) VALUES (?, ?, ?, ?);");
		$query->bind_param("ssss", $id, password_hash($pass, PASSWORD_BCRYPT), $_SERVER['REMOTE_ADDR'], session_id());
		$query->execute();
		$query->close();
		$mysqli->close();
		$SUCCESS = true;
	} else {
		$ERROR = "You must enter a username and password to register.";
	}
}

?>
