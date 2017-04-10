 <form action="" method="get">
    <div class="col-xs-4">
        <label for="host">Host:</label>
        <input type="text" class="form-control" name="host" id="host">
        <button type="submit" class="btn btn-default">Submit</button>
    <div>
</form>

<?php
    $host = $_GET['host'];
    $output = exec('ping -c 1 '.$host, $output, $result);
    if($result == 0){
        echo "up :)";
    }
    else {
        echo "down :(";
    }

?>

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

