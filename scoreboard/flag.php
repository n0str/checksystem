<?php

$ROUND_DURATION = 60;
$FLAG_DURATION = $ROUND_DURATION * 5;
$TEAMS = array(array(-1,'your_team'),);
$dblink = mysql_connect("localhost","root","***");
if(!$dblink)
	return ($flag_was_not_accepted." (not connected to database)");
$db_selected = mysql_select_db("classic-ctf");

if(!$db_selected)
	return ($flag_was_not_accepted." (not selected database)");
mysql_query("SET NAMES utf8");
?>

<?php
	$result = mysql_query("SELECT id,name FROM teams");
	while ($row = mysql_fetch_array($result))
	    $TEAMS[] = array($row["id"], $row["name"]);

?>

<?php

function check_fl()
{
	global $ROUND_DURATION,$FLAG_DURATION,$TEAMS;
	$flag_was_not_accepted = "FLAG WAS NOT ACCEPTED";

	if(!isset($_GET['team']) && !isset($_GET['flag']))
		return ($flag_was_not_accepted." (input something)");

	$team = intval($_GET['team']);
	$flag = mysql_real_escape_string(strtolower($_GET['flag']));

	if ($team <= 0 || $team >= count($TEAMS))
		return ($flag_was_not_accepted." (name of team has wrong format )");

	if (!preg_match("/^[a-f0-9]*$/", $flag))
		return ($flag_was_not_accepted." (flag has wrong format)");


	$result = mysql_query("select * from flags where flag = '".$flag."'");
	$flag_db = mysql_fetch_array( $result );

	if (!$result)
		return ($flag_was_not_accepted." (flag isn't found)");

	if ($flag_db["team_id"] == $team)
		return ($flag_was_not_accepted." (it is your flag)");


	$result = mysql_query("select * from sended_flags where flag_id = '".$flag_db["id"]."' AND team_id = '". $team ."'");
	$result = mysql_fetch_array( $result );
	if ($result)
		return ($flag_was_not_accepted." (flag has already passed)");

	$now = date("Y-m-d H:i:s");
	$flag_post = $flag_db["post_timestamp"];

	$datetime1 = strtotime($now);
	$datetime2 = strtotime($flag_post);

	if ($datetime1 - $datetime2 > $FLAG_DURATION)
		return ($flag_was_not_accepted." (9 - flag is old)");

	$result = mysql_query("INSERT INTO sended_flags VALUES ('".$flag_db["id"]."','".$team."',NULL)");
	if($result)
		return "FLAG ACCEPTED";
	else
		return ($flag_was_not_accepted." (10 - I don't know)");
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
            <li class="active"><a href="flag.php">Submit</a></li>
            <li><a href="advisory.php">Advisory</a></li>
          </ul>
        </div>
      </div>

      <form  style="color:black;"   name="flags_submit" method="GET">
		<select style="color:black;" name="team">
			<?php foreach ($TEAMS as $value): ?>
				<?php echo "<option value=".$value[0].">". $value[1]. "</option>"; ?>
			<?php endforeach; ?>
		</select>
		<input type="text" name="flag">
		<input type="submit" style="color:black;" value="Send">
	</form>


	<?php
		echo check_fl();
	?>

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








