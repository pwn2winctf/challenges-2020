<style>
:root{
	color:white;
}
canvas {
  position: absolute;
	top: 0;
	left: 0;
  z-index: -3 !important;
}
</style>

<form action="/" method="post">
	<label for="url">URL :</label>
	<input name="url" id="url" type="text" value="https://google.com"><br>
	<input type="submit" value="Go">
</form>

<a href="/?source">source plz</a>

<script src="https://cdn.jsdelivr.net/npm/p5@1.0.0/lib/p5.min.js"></script>
<script src="trippy.js"></script>
<!-- g0t sh3ll ? -->

<?php

if ( isset($_GET['source']) ) {
	show_source('index.php');
}

if ( strpos($_POST['url'],'http://') === 0 || strpos($_POST['url'],'https://') === 0 ) {
	echo system('timeout 8s wappalyzer ' . escapeshellarg(escapeshellcmd($_POST['url'])));
	// npm install wappalyzer@5.9.34
}

?>


