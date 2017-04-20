<?php
session_start();


include("./simple-php-captcha/simple-php-captcha.php");
if (isset($_POST['captcha'])){
    
    if ($_POST['captcha'] === $_SESSION['captcha']['code']){
	$_SESSION['535b6975b3554bcce7d0c7f8966bbb5eb158c852_success'] += 1;
		if ($_SESSION['535b6975b3554bcce7d0c7f8966bbb5eb158c852_success'] > 2000){
			include('header.php'); ?>
			<strong>The flag is PNG_with_an_additional_R'; </strong>
			<?php
			include('footer.php');
	} else { 
	include('header.php');
	print '<strong>You have '.$_SESSION['535b6975b3554bcce7d0c7f8966bbb5eb158c852_success'].' success so far. You need 2000 for a flag</strong>';
	$_SESSION['captcha'] = simple_php_captcha( array(
		'min_length' => 5,
		'max_length' => 9,
		'backgrounds' => array('./backgrounds/45-degree-fabric.png','./backgrounds/cloth-alike.png','./backgrounds/grey-sandbag.png','./backgrounds/kinda-jean.png','./backgrounds/polyester-lite.png','./backgrounds/stitched-wool.png','./backgrounds/white-carbon.png','./backgrounds/white-wave.png'),
		'fonts' => array('./fonts/times_new_yorker.ttf'),
		'characters' => 'ABCDEFGHJKLMNPRSTUVWXYZabcdefghjkmnprstuvwxyz23456789',
		'min_font_size' => 28,
		'max_font_size' => 28,
		'color' => '#666',
		'angle_min' => 0,
		'angle_max' => 20,
		'shadow' => true,
		'shadow_color' => '#fff',
		'shadow_offset_x' => -1,
		'shadow_offset_y' => 1
	));
	include('footer.php');
} } else {
	include('header.php');
	echo '<strong>Bad Captcha.</strong>';
	include('footer.php');
        }} else {
$_SESSION['captcha'] = simple_php_captcha( array(
	'min_length' => 5,
	'max_length' => 9,
	'backgrounds' => array('./backgrounds/45-degree-fabric.png','./backgrounds/cloth-alike.png','./backgrounds/grey-sandbag.png','./backgrounds/kinda-jean.png','./backgrounds/polyester-lite.png','./backgrounds/stitched-wool.png','./backgrounds/white-carbon.png','./backgrounds/white-wave.png'),
	'fonts' => array('./fonts/times_new_yorker.ttf'),
	'characters' => 'ABCDEFGHJKLMNPRSTUVWXYZabcdefghjkmnprstuvwxyz23456789',
	'min_font_size' => 28,
	'max_font_size' => 28,
	'color' => '#666',
	'angle_min' => 0,
	'angle_max' => 20,
	'shadow' => true,
	'shadow_color' => '#fff',
	'shadow_offset_x' => -1,
	'shadow_offset_y' => 1
));

?>
<html>
	<head>
		<title>Owny Pictures</title>
	<style>
		body {
			font-family: monospace;
			color: white;
			background-color: black;
			max-width: 70%;
			padding: 5%;
		}
		
		#warning {
			padding:5%;
			text-align: center;	
		}

		#center {
			text-align: center;
		}
	</style>
	</head>
	<body>
		<h1>Welcome to </h1><img src='owny_3_white_s.png' />
		<br/>
		<div id='warning'>
                        <i>At Owny, we are proud of our 'security'. You need 2000 captchas to get the flag. 
                           We are so sure of our security that the captcha generation php code is available
                        <a href="/simple-php-captcha.txt">here</a></i><bl>
			</div>
		<img srx='x'/>
<form  method='post'>
<img src='<?php echo $_SESSION['captcha']['image_src']; ?>'><br>
Captcha <input id='captcha' name='captcha' />
<input type='submit'></form>
</body> </html>
<?php 
//print_r($_SESSION);

}

?>
