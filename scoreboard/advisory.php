<?php

$ROUND_DURATION = 30;
$FLAG_DURATION = 30 * 5;
$TEAMS = array(array(-1,'your_team'),);
$avd_send = 0;
$dblink = mysql_connect("localhost","root","***");
if(!$dblink)
	die($flag_was_not_accepted." (not connected to database)");
$db_selected = mysql_select_db("classic-ctf");

if(!$db_selected)
	die($flag_was_not_accepted." (not selected database)");
mysql_query("SET NAMES utf8");

?>

<?php
$result = mysql_query("SELECT id,name FROM teams");
while ($row = mysql_fetch_array($result))
    $TEAMS[] = array($row["id"], $row["name"]);
 
if ($_POST['team'])
{
	$adv = mysql_real_escape_string($_POST['adv']);
	$team = intval($_POST['team']);
	if ($team > 0 && $team < count($TEAMS))
	{
		mysql_query("INSERT INTO advisory VALUES('','$team','$adv','','0')");
		$avd_send = 1;
	}
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
            <li><a href=".">Home</a></li>
            <li><a href="flag.php">Submit</a></li>
            <li class="active"><a href="advisory.php">Advisory</a></li>
          </ul>
        </div>
      </div>

		<form name="adv_submit" method="POST">
			<div class="inner cover">
				<h1 class="cover-heading">Advisory.</h1>   

				<select style="color:black;" name="team">
				<?php foreach ($TEAMS as $value): ?>
				<?php echo "<option value=".$value[0].">". $value[1]. "</option>"; ?>
				<?php endforeach; ?>
				</select><br>
				
				
			</div>

			<div class="inner cover">
				<textarea name="adv" style="color:black;" rows=16 cols=64></textarea>      
			</div>
			<div class="inner cover">
				<input type="submit" style="color:black;"  value="Send">     
				<?php if ($avd_send == 1) echo "<br><br>Sent"; ?>  
			</div>
		</form>


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
