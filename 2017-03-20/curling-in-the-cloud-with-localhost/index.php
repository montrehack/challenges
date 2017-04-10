<?php
require_once("function.php");
if(isset($_POST['r']) &&  $_POST['r'] != "") {
        $datas =  htmlspecialchars(get_contents($_POST['r']));
	$datas =  htmlentities($datas);
}
?>

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

		    
		 <p>Enter a URL to fetch</p>

		 <form method="POST" action="#">
		 	<span>URL:
				<input name="r" type="text" value="http://csir.dept-info.crosemont.quebec/" />
				<input type="submit" />
		    	</span>

		</form>
        </div>
	<!---parse_url-->
        <!---debug=false-->
   </body>
</html>

