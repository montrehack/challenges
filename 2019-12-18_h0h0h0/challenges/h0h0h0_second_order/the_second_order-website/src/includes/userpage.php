<?php
$logged_in=False;

if(isset($_REQUEST["logout"])) {
	unset($_SESSION["user_row_id"]);
}

if (isset($_SESSION["user_row_id"])) {
	include("mysql_connection.php");
	$mysqli = getConnection();
	$query = $mysqli->prepare("SELECT username FROM users WHERE id=? AND ip=? and session=?;");
	$query->bind_param("sss", $_SESSION["user_row_id"], $_SERVER['REMOTE_ADDR'], session_id());
	$query->execute();
	$result = $query->get_result();
	$query->close();
	$mysqli->close();
	if ($result->num_rows > 0) {
		$row = $result->fetch_assoc();
		$logged_in=True;
		$username = $row["username"];
		$mysqli = getComection();
		$query = $mysqli->prepare(sprintf("SELECT user,subject,content FROM messages WHERE visibility='public' OR ((user='%s') AND visibility='self');", $username));
		if ($mysqli->connect_errno) {
			echo "Errno: " . $mysqli->connect_errno . "<br>";
			echo "Error: " . $mysqli->connect_error . "<br>";
			die();
		}
		$query->execute();
		$result = $query->get_result();
		$query->close();
		$mysqli->close();
		$messages = $result->fetch_all();
	}
}
?>
