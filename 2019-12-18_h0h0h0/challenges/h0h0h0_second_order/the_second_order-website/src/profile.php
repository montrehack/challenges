<?php session_start();
include("includes/userpage.php");
?>

<html>
<head>
	<link rel="icon" type="image/png" sizes="16x16" href="/img/favicon-16x16.png">
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="css/hero.css">
	<script src="/js/jquery.min.js"></script>
	<script src="/js/bootstrap.min.js"></script>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <a class="navbar-brand" href="index.php">
	<img src="/img/second-order_logo.png" width="40" height="40" alt="">
	The Second Order
  </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" href="index.php">Join Us</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="connect.php">Connect</a>
      </li>
      <li class="nav-item active">
        <a class="nav-link" href="profile.php">My Profile</a><span class="sr-only">(current)</span>
      </li>
    </ul>
  </div>
</nav>
<div class="hero-img hero-image3">
  <div class="hero-text">
    <h1>Starkiller Online</h1>
    <p>All remaining systems will bow to the Second Order! (well, those not already bowing to the first one at least)</p>
  </div>
</div>

<div id="main" class="mt-5 container">
<?php
if($logged_in !== True) {
	echo "<h2 class='alert alert-danger'>You must <a href='/connect.php'>login</a> to access this page</h2>";
}
else {
	echo "<h2>Welcome $username</h2>
		<form>
			<input type=hidden name=logout id=logout value=logout></input>
			<input type=submit class='btn btn-warning' value='Log Out'></input>
		</form>
     	  <h3>Here are your messages</h3>
		  <div class='mt-4 justify-content-center col-md-6'>";
	foreach($messages as $message) {
		echo "<div class='card bg-secondary mb-4 border-primary'>
				<h4 class='card-header'>$message[1]</h4>
			  	<div class='card-body'>
					<p class='card-text'>$message[2]</p>
  				</div>
			    <div class='card-footer text-muted'>$message[0]</div>
		    </div>";
	}
	echo "</div>";
}
?>
</div>
</body>
</html>
