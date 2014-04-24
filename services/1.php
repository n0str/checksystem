<?php
	if (isset($_GET['registration']))
	{
		$login = $_GET['user'];
		$f = fopen($login,"wb");
		echo $login;
		fclose($f);
	}
	if (isset($_GET['get']))
	{
		$login = $_GET['user'];
		$f = fopen($login,"rb");
		if ($f)
		{
			$qwe = fread($f,filesize($login));
			echo "flag is :".$qwe;
		}
		else
		{
			echo "No such user";
		}
		fclose($f);
	}
	if (isset($_GET['put']))
	{
		$login = $_GET['user'];
		$flag = $_GET['flag'];
		$f = fopen($login,"a+");
		if ($f)
		{
			fwrite($f,$flag);
			echo "done";
		}
		else
		{
			echo "No such user";
		}
	}
?>

