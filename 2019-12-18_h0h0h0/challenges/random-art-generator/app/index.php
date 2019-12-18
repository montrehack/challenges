<?php
	ini_set('display_errors', 1);
	session_start();
	
	$image = "";
	shell_exec("python3 /app/image.py ". session_id());

	// Avoid path traversal and bad voodoo stuff
	if(preg_match('/^[a-zA-Z0-9,-]+$/', session_id()) !== 0){
		$image = file_get_contents("/tmp/".session_id().".txt");
		if(!empty($image)){
			unlink("/tmp/".session_id().".txt");
		}
	}
?>
<!DOCTYPE html>
<html>
<head>
	<title></title>
</head>
<body>
	<h1>Python Random Art Generator Seeded with a Magical ID (that you control):</h1>
	<img src="<?php echo $image; ?>" alt="Something went wrong">
</body>
</html>
