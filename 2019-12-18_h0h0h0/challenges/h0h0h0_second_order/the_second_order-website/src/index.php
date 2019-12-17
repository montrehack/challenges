<?php session_start();
include("includes/register.php");
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
      <li class="nav-item active">
        <a class="nav-link" href="index.php">Join Us<span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="connect.php">Connect</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="profile.php">My Profile</a>
      </li>
    </ul>
  </div>
</nav>
<div class="hero-img hero-image">
  <div class="hero-text">
    <h1>The Second Order</h1>
    <p>We got sick of Kylo Ren's teenage tantrums, so we started our own order!</p>
    <a href="#join-form" class="btn btn-primary">Join Us!</a>
  </div>
</div>

<div id="join-form" class="mt-5 container">
<h2>I want you to join us</h2>
<div class="mt-5 justify-content-center col-md-6">
<?php if(isset($ERROR)) {
	echo "<p class='alert alert-danger'>$ERROR</p>";
} else if (isset($SUCCESS)) {
	echo "<p class='alert alert-success'>Welcome to the Second Order, you may now <a href=/connect.php>connect</a></p>";
}
?>
<form method="post">
  <div class="form-group">
    <label for="userID">User ID</label>
    <input type="text" class="form-control" id="userID" name="userID" aria-describedby="idHelp" placeholder="FN-9999" maxlength=256>
  </div>
  <div class="form-group">
    <label for="password">Password</label>
    <input type="password" class="form-control" id="password" name="password" placeholder="Password" maxlength=256>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
</div>
</div>
</body>
</html>
