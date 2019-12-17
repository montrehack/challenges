<?php
function getConnection() {
	$mysqli = new mysqli($_ENV['DB_HOST'], $_ENV['DB_USER1'], $_ENV['DB_USER1_PASS'], $_ENV['DB_NAME']);
	if ($mysqli->connect_errno) {
		echo "Errno: " . $mysqli->connect_errno . "\n";
		echo "Error: " . $mysqli->connect_error . "\n";
		die();
	}
	return $mysqli;
}

function getComection() {
	$mysqli = new mysqli($_ENV['DB_HOST'], $_ENV['DB_USER2'], $_ENV['DB_USER2_PASS'], $_ENV['DB_NAME']);
	if ($mysqli->connect_errno) {
		echo "Errno: " . $mysqli->connect_errno . "\n";
		echo "Error: " . $mysqli->connect_error . "\n";
		die();
	}
	return $mysqli;
}
?>
