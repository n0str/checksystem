<?php
#error_reporting(E_ALL);
#ini_set('display_errors', 'On');

$ROUND_DURATION = 60;
$FLAG_DURATION = 60 * 5;
$TEAMS = array();
$SERVICES = array();
$A = 6;

$dblink = mysql_connect("localhost","root","***");
if(!$dblink)
    die("not connected to database");
$db_selected = mysql_select_db("classic-ctf");


$result = mysql_query("SELECT id,name FROM teams");
while ($row = mysql_fetch_array($result))
    $TEAMS[] = array($row["id"], $row["name"]);

$result = mysql_query("SELECT id,name FROM services");
while ($row = mysql_fetch_array($result))
    $SERVICES[] = array($row["id"], $row["name"]);

function compare($a, $b)
{
    return $a['score'] < $b['score'];
}

function get_attack_defence()
{
    global $TEAMS, $A, $SERVICES;
    $result = array();
    $teams_defence = array();
    $teams_attack = array();
    $teams_advisory = array();

    foreach ($TEAMS as $team_id)
    {
        $teams_defence[$team_id[0]] = 0;
         $teams_attack[$team_id[0]] = 0;
          $teams_advisory[$team_id[0]] = 0;
    }

    
    $defence_query = mysql_query("SELECT team_id, put_status, check_status FROM flags");
    while ($row = mysql_fetch_array($defence_query))
        if ($row['check_status']==1)
            $teams_defence[$row['team_id']] += 0.5 * $A;
            
    $advisory_query = mysql_query("SELECT team_id, SUM(score) as sc from advisory GROUP BY team_id");
    while ($row = mysql_fetch_array($advisory_query))
        $teams_advisory[$row['team_id']] += intval($row['sc']);

    
    $attack_query = mysql_query("SELECT flag_id, team_id FROM sended_flags");
    while ($row = mysql_fetch_array($attack_query))
    {
        $get_flags_count_query = mysql_query("SELECT COUNT(team_id) AS flag_count FROM sended_flags WHERE flag_id = ".$row['flag_id']);
        $flag_count = mysql_fetch_array($get_flags_count_query);
        $flag_count = $flag_count['flag_count'];

        $teams_attack[$row['team_id']] += $A / $flag_count;
    }

    foreach ($TEAMS as $team_id)
    {
        $new_row = array(
            "team_id" => $team_id[0],
            "team" => $team_id[1],
            "defence" => $teams_defence[$team_id[0]], 
            "attack" =>$teams_attack[$team_id[0]],
            "advisory" => $teams_advisory[$team_id[0]],
            "score" => $teams_attack[$team_id[0]] + $teams_defence[$team_id[0]] + $teams_advisory[$team_id[0]]
            );

        foreach ($SERVICES as $serv) {
            $status = mysql_query("SELECT put_status, check_status FROM flags WHERE put_status<>'-10' AND team_id='".$team_id[0]."' AND service_id='".$serv[0]."' ORDER BY post_timestamp DESC LIMIT 1");
            if ($status)
            {
                $status = mysql_fetch_array($status);
                if ($status["put_status"] == 0)
                    $new_row[$serv[1]] = "put error";
                elseif ($status["check_status"] == 0)
                    $new_row[$serv[1]] = "corrupt";
                else
                    $new_row[$serv[1]] = "OK";
            }
            else
                $new_row[$serv[1]] = "starting";
        }

        $result[] = $new_row;
    }
    usort($result,'compare');    
    return $result;
}

return get_attack_defence();
