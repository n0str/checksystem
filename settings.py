
teams = [
    (1, 'one half of the yozik', '127.0.0.1'),
    (2, 'another half of the yozik', '192.168.0.71'),
]

services = [
	(1, 'perl', './checkers/checker_perl.py'),
	#(2, 'python', 'checkers/checker.py'),
]

db_settings = {
	"host" : "localhost",
	"user" : "root",
	"password" : "byrfgcekzwbz",
	"db" : "classic-ctf"
}

queues_names = ['q1', 'q2', 'q3']
queue_len = 2

ROUND_DURATION = 60
FLAG_DURATION = ROUND_DURATION * 5
CHECKER_TIMEOUT = 15

GAME_FINISH_TIME = 1398755548 #timestamp