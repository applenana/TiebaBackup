<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>

<meta name="viewport" content="width=device-width, initial-scale=1" />  

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<title>检测</title>

<style type="text/css">

<!--

.STYLE1 {

	font-size: x-large;

	font-weight: bold;

}

.STYLE2 {

	font-size: 36px;

	font-family: "等线 Light";

	font-weight: bold;

}

-->

</style>

</head>
<body>

<h1 align="center" class="STYLE2"><img src="a111.png" width="117" height="117" /></h1>

<?php

$myfile = fopen("./留言/saying.txt", "a") or die("Unable to open file!");
$txt = $_GET["message"];
fwrite($myfile, $txt);
fwrite($myfile,"\n");
fclose($myfile);

$myfile = fopen("tmp.txt", "w") or die("Unable to open file!");
$txt =$_POST["url"];
fwrite($myfile, $txt);
fclose($myfile);

echo(system("cd /www/wwwroot/story.applenana.top/&&PYTHONIOENCODING=utf-8 python3 compare.py")); 

?> 
<p align="center" class="STYLE2"><a href="/HL.php">点击我继续提交！</a></p>';


<body background="bg.png">


</body>

</html>

