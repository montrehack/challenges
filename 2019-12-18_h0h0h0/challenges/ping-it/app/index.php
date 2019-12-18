<!DOCTYPE html>
<html lang="en"><head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <title>Ping it !</title>

    <!-- Bootstrap core CSS -->
    <link href="/css/bootstrap.min.css" rel="stylesheet" />

    <link href="/css/styles.css" rel="stylesheet" />
    <link href="/css/highlightjs/github.min.css" rel="stylesheet" />
    <script src="/js/highlight.pack.js"></script>
  </head>
  <body class="bg-light">
    <div class="container">
  <div class="py-5 text-center">
    <h1>&gt;_</h1>
    <h2>Ping it !</h2>
    <p class="lead">This tool can be used to debug ping requests. It uses strace to look at the network for extra juicy debugging info.</p>
  </div>

  <div class="row">
    <div class="col-lg-12">
      <form method="GET">
        <div class="row text-center">
          <div class="col-md-2 mt-5 mb-3 ml-auto">
            <label for="host">Host IP</label>
          </div>
          <div class="col-md-4 mt-5 mb-3">
              <input type="text" name="host" id="host"/>
          </div>
          <div class="col-md-3 mt-5 mb-3 ml-3 mr-auto">
            <button class="btn btn-primary btn-block" type="submit">Ping it !</button>
          </div>
        </div>
      </form>
    </div>
  </div>

  <?php
    if(isset($_GET['host'])) :
        $cmd = escapeshellcmd($_GET['host']);
        $file_name = uniqid('', true);
        exec("sudo /app/strace -f -e trace=network -s 5000 ping -W 5 -c 1 $cmd > output/$file_name 2>&1");
  ?>
    <div class="row">
      <div class="col-lg-12">
        <b>
          <?php echo "To view the results of your ping, go to https://ping-it.owoups.org/check.php?filename=$file_name"; ?>
        </b>
      </div>
    </div>

  <?php endif; ?>

  <br/>
  <br/>

  <div class="row">
    <div class="col-lg-12">
      <p>Dont waste your time trying to inject commands. I escaped it !</p>
    </div>
  </div>

  <div class="row">
    <div class="col-lg-12">
      <div class="snippet">
      <pre><code class="hljs php">&lt;?php
$cmd = escapeshellcmd($_GET['host']);
$file_name = uniqid('', true);
exec("sudo /app/strace -f -e trace=network -s 5000 ping -W 5 -c 1 $cmd > output/$file_name 2>&1");
[...]</code></pre>
      </div>
    </div>
  </div>

  <footer class="my-5 pt-5 text-muted text-center text-small">
    <p class="mb-1">© 1999-2000 Ping Corp</p>
  </footer>

</div>
</body>
</html>
