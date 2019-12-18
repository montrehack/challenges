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
      <p>Here is your sweet sweet debugging data:</p>
    </div>
  </div>

  <div class="row">
    <div class="col-lg-12">
      <div class="snippet">
      <pre><code class="hljs"><?php

include "/app/output/" . basename($_GET['filename']);

?></code></pre>
      </div>
    </div>
  </div>

  <footer class="my-5 pt-5 text-muted text-center text-small">
    <p class="mb-1">© 1999-2000 Ping Corp</p>
  </footer>

</div>
</body>
</html>
