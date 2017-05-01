<?php
session_start();
if ($_SERVER['REQUEST_METHOD'] === 'POST'){
//echo $_SESSION['captcha'];
	if (isset($_POST['captcha'])){
		if ($_POST['captcha'] == $_SESSION['captcha']){
		echo 'Congrats, the flag is Bring_back_szechuan_sauce' ;
		//var_dump($_POST['captcha']);   
		} else {
		echo 'You have a wrong captcha. You are not a human. Try again later.';
}
	} else {
   header( 'Location: /form3.php' ) ;
}

}
else {
   header( 'Location: /form3.php' ) ;
}

?>
