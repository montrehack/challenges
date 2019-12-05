<?php
$title="MontréHack h0h0h0day edition";

session_start();

if(isset($_SESSION['ishacker']) && $_SESSION['ishacker'] === true)  {
    //All good
}
else {
    header("Location: /");
}
?>
<!DOCTYPE html>
<html lang="en">
<head>

  <title><?= $title ?></title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
<style type="text/css">
@font-face {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 400;
  src: local('Roboto Regular'), local('Roboto-Regular'), url(//fonts.gstatic.com/s/roboto/v18/KFOmCnqEu92Fr1Mu72xKOzY.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
</style>

    <link rel="stylesheet" type="text/css" href="css/montrehack.css">
    <link href="css/bootstrap.min.css" rel="stylesheet">
</head>
<body>


<br/>

<div class="container">
    <div class="row">
        <div class="col col-lg-6 col-md-6 col-sm-12 well">

<h1>C'est presque terminé! / Almost done!</h1>
<p>Vous êtes à une étape de vous enregistrer au party de noël le plus l33t. / You are at one step away from registering to the l33test Christmas party.</p>

<h2>Eventbrite</h2>
<p>
Code: <b>T1ME-T0-PR3P4RE-Y0UR-CHALL3NGE</b><br/>
Lien/Link: <a target="_blank" href="https://www.eventbrite.ca/e/montrehack-h0h0h0-day-party-tickets-85048932647">https://www.eventbrite.ca/e/montrehack-h0h0h0-day-party-tickets-85048932647</a>

</p>

<img src="images/santa-hacking.png" style="width: 100%;"/>

          </div>
    </div>
</div>
<br/>


    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery-slim.min.js"><\/script>')</script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
</body>
</html>
