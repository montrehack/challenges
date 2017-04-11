<?php
if(isset($_SERVER['REMOTE_ADDR']) AND ( $_SERVER['REMOTE_ADDR'] !== $_SERVER['SERVER_ADDR'] )){
	die(' Access Denied, Your IP: ' . $_SERVER['REMOTE_ADDR'] );
	 exit;
}
?>
FLAG-33C3WASFUN
