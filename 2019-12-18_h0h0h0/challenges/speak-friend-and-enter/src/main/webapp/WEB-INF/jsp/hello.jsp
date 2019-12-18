<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Speak friend and enter!</title>
    <link href="/css/main.css" rel="stylesheet">
</head>
<body>
    <style type="text/css">
        body{
            position: fixed;
            height: 100%;
            width: 100%;
            background: url('img/moria.jpg') no-repeat center center fixed; 
            -webkit-background-size: cover;
            -moz-background-size: cover;
            -o-background-size: cover;
            background-size: cover;
        }

        .container{
            padding-left: 30%;
            padding-right: 30%;
            padding-top: 30px;
            padding-bottom: 30px;
            margin-top: 30px;
            margin-bottom: 30px;
            width: 40%;
            background-color: rgba(255, 255, 255, 0.5);;
            text-align: center;
            font-weight: bolder;
        }

        form{
            padding-top: 30px;
        }
    </style>

    <div class="container">
        <p>
            To feed their greed the dwarves dug deep, <br/>
            Into mount Spring like birds pecking. <br/>
            <br />
            By a trimmed oak their pride was soaked, <br />
            So they thought best to drink and rest. <br />
            <br />
            For an old tale foretold of SpeL, <br/>
            Can you prevail and get a shell ?
        </p>

        <form method="GET" action="/enter">
            Speak <input type="text" name="spel" value="'friend'"> and <input type="submit" name="enter" value="enter">
        </form>
    </div>

</body>
</html>
