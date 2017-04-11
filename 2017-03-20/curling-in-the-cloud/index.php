<?php
    //On prend le url de donner
    $location=$_GET['host'];
    $curl = curl_init();
    //aucune validation sur se qui est donner par l'utilisateur :)
    curl_setopt ($curl, CURLOPT_URL, $location);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_MAXREDIRS, 0);
    $datas = htmlentities(htmlspecialchars(curl_exec ($curl)));
    curl_close ($curl);
?>
<html>
<!DOCTYPE HTML>
<html>
 <head>
    <!--[if lt IE 9]><script type="text/javascript" src="excanvas.js"></script><![endif]-->
    <script src="tagcanvas.js" type="text/javascript"></script>
    <script type="text/javascript">
      window.onload = function() {
        try {
          TagCanvas.Start('myCanvas','tags',{
            textColour: '#ff0000',
            outlineColour: '#ff00ff',
            reverse: true,
            depth: 0.8,
            maxSpeed: 0.05
          });
        } catch(e) {
          // something went wrong, hide the canvas container
          document.getElementById('myCanvasContainer').style.display = 'none';
        }
      };
    </script>
  </head>

    <body>
        <div id=myCanvasContainer>
                <canvas width="300" height="300" id="myCanvas">
                </canvas>
        </div>
        <div id=tags>
                <?php
                        $i = 0;
                        $tags = preg_split('/\s+/',$datas);
                        foreach($tags as $tag){
                                if ($i++ > 10) break;
                                echo "<li><a> $tag </a></li>";
                        }
                ?>
        </div>
        <div>
        <div>
            <p>Enter a URL to fetch</p>
            <form method="GET" action="#">
            <span>URL:
                <input  name="host" id="host" value ="csir.dept-info.crosemont.quebec/ctf/">
                <input type="submit" />
            </span>

            </form>

        </div>
  </body>
</html>
		

