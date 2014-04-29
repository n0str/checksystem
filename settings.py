
teams = [
    (1, 'one half of yozik', '192.168.0.100'),
    (2, 'another half of yozik', '192.168.0.101'),
]

services = [
	(1, 'php', 80),
	(2, 'perl', 40),
	(3, 'python', 9001)
]

db_settings = {
	"host" : "localhost",
	"user" : "root",
	"password" : "byrfgcekzwbz",
	"db" : "classic-ctf"
}

queues_names = ['q1', 'q2', 'q3']
queue_len = 3

ROUND_DURATION = 60
FLAG_DURATION = ROUND_DURATION * 5
CHECKER_TIMEOUT = 15

GAME_FINISH_TIME = 1398755548 #timestamp