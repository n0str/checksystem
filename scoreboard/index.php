<?php 
error_reporting(E_ALL);
ini_set('display_errors', 1);
$data = include "score.php";

function getClass($state){
	if($state != "OK")
		return " class='warning' ";
	return;
}

function getSpan($state){
	if($state != "OK")
		return "<span style='color:red;' class='glyphicon glyphicon-remove' title='".$state."'></span>";
	return "<span class='glyphicon glyphicon-ok'></span>";
}

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="language" content="en" />

	
	<link href="./css/bootstrap.min.css" rel="stylesheet">
	<link href="./css/cover.css" rel="stylesheet">
	<script src="./js/jquery-1.11.0.min.js"/></script>
	<script src="./js/bootstrap.min.js"></script>
	<script src="./js/score.js"></script>
	
	
	<title>Scoreboard</title>
</head>
<body>

<div class="site-wrapper">

  <div class="site-wrapper-inner">

    <div class="cover-container">

      <div class="masthead clearfix">
        <div class="inner">
          <h3 class="masthead-brand">Scoreboard</h3>
          <ul class="nav masthead-nav">
            <li class="active"><a href="#">Home</a></li>
            <li><a href="flag.php">Submit</a></li>
            <li><a href="advisory.php">Advisory</a></li>
          </ul>
        </div>
      </div>

      <div class="inner cover">
        <h1 class="cover-heading">Scoreboard. <span class="lead">Siberian CTF training #2</span></h1>        
      </div>

	  	<input type="hidden" id="up-down" value="-1">
		<table class="table table-hover">
			<tr class="info"><td>TEAM</td><td>Defence</td><td>Attack</td><td>Advisory<td>PHP</td><td>Perl</td><td>Python</td><td>Score</td></tr>
			<?php foreach($data as $item): ?>
			<tr id="team-<?=$item['team_id']?>">
				<td><?=$item['team']?></td>
				<td><?=$item['defence']?></td>
				<td><?=$item['attack']?></td>
				<td><?=$item['advisory']?></td>
				<td ><?=getSpan($item['php'])?></td>
				<td ><?=getSpan($item['perl'])?></td>
				<td ><?=getSpan($item['python'])?></td>
				<td><?=$item['score']?></td>
			</tr>
			<?php endforeach; ?>
		</table>
	  

      <div class="mastfoot">
        <div class="inner">
          <p>by Yozik-team</p>
        </div>
      </div>

    </div>

  </div>

</div>


</body>
</html>
