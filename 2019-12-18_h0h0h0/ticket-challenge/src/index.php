<?php

$title="MontréHack h0h0h0day edition";

if(isset($_POST['name']) && isset($_POST['email']) && isset($_POST['ishacker'])) {

    $log = json_encode(["name"=>$_POST['name'],"email"=>$_POST['email']]);
    $log .= "\n";
    file_put_contents('/var/log/apache2/real_hackers.log', $log, FILE_APPEND);
    session_start();
    $_SESSION['ishacker'] = true;
    header("Location: success.php");
    exit();
}
?><!DOCTYPE html>
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

    <link href="css/bootstrap.min.css" rel="stylesheet" type="text/css">
    <link href="css/montrehack.css" rel="stylesheet" type="text/css">
</head>
<body>


<br/>

<div class="container">
    <div class="row">
        <div class="col col-lg-6 col-md-6 col-sm-12 well">
                <div  class="">

                    <h2 class="section-heading"><?= $title ?></h2>

                    <div class="alert alert-warning" role="alert">Étant donné les places limités, l'enregistrement requiert un paiement symbolique de 5$ pour réduire l'impact des absents. <br/>//<br/> Due to limited space, registration requires a 5$ symbolic fee to avoid the impact of no-show.</div>

                    <div>Attention, nous avons un système d'accréditation sophistiqué afin de permettre seulement aux vrais pirates de s'enregistrer! <br/>//<br/> Beware we have a sophisticated accreditation system to allow only real hackers to register!</div>

<br/>
                    <form action="" method="post" class="form-registration">
                        <div class="form-group">
                            <label for="name">Nom / Name</label>
                            <input type="text" class="form-control" id="name" name="name" aria-describedby="nameHelp" placeholder="" required>
                            <small id="nameHelp" class="form-text text-muted">Utiliser votre nom ou pseudo / Use your full name or nickname.</small>
                        </div>
                        <div class="form-group">
                            <label for="email">Courriel / Email</label>
                            <input type="email" class="form-control" id="email" name="email" aria-describedby="emailHelp" placeholder="" required>
                        </div>

                        <div class="form-group">
                          <label for="email">Verification</label>

                          <div id="rc-anchor-container" class="rc-anchor rc-anchor-normal rc-anchor-light">            
                            <div class="rc-anchor-content">
                              <div class="rc-inline-block"><div class="rc-anchor-center-container">
                                <div class="rc-anchor-center-item rc-anchor-checkbox-holder"><input type="checkbox" id="ishacker" class="hacker-checkbox" name="ishacker" onchange="this.checked=false" required/></div></div></div><div class="rc-inline-block"><div class="rc-anchor-center-container">
<label for="ishacker" class="rc-anchor-center-item rc-anchor-checkbox-label">I'm a hacker</label></div>
                                </div>
                              </div>
                              <div class="rc-anchor-normal-footer">
                                <div class="rc-anchor-logo-portrait" aria-hidden="true" role="presentation">
                                  <div class="rc-anchor-logo-img rc-anchor-logo-img-portrait"></div>
                                  <div class="rc-anchor-logo-text">montréHack</div>
                                </div>
                              </div>
                            </div>
                          </div>
                          <div class="mx-auto">
                        <button type="submit" class="btn btn-primary text-right">Submit</button></div>
                    </form>
                </div>
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
