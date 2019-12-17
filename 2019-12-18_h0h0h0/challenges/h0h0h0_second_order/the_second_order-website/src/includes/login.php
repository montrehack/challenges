<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	unset($_SESSION["user_row_id"]);

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
		$query = $mysqli->prepare("SELECT id,username,password FROM users WHERE username=? AND ip=? AND session=? LIMIT 1;");
		$query->bind_param("sss", $id, $_SERVER['REMOTE_ADDR'], session_id());
		$query->execute();
		$result = $query->get_result();
		$query->close();
		$mysqli->close();
		if ($result->num_rows > 0) {
			$row = $result->fetch_assoc();
			if (password_verify($pass, $row["password"]) === True) {
				$_SESSION["user_row_id"] = $row["id"];
				$SUCCESS=True;
			} else {
				$ERROR = "You must enter a valid username and password.";
			}
		} else {
			password_hash($pass, PASSWORD_BCRYPT);
			$ERROR = "You must enter a valid username and password.";
		}
	} else {
		$ERROR = "You must enter a valid username and password.";
	}
}

?>
