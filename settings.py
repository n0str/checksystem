
teams = [
    (1, 'yozik', '10.53.1.3'),
    (2, 'keva-mustang', '10.53.3.3'),
    (3, 'brizzz', '10.53.2.3'),
]

services = [
	(1, 'php', './checkers/checker_php.py'),
	(2, 'perl', 'checkers/checker_perl.py'),
	(3, 'python', 'checkers/checker_python.py'),
]

db_settings = {
	"host" : "localhost",
	"user" : "root",
	"password" : "***",
	"db" : "classic-ctf"
}

queues_names = ['q1', 'q2', 'q3']
queue_len = 9

ROUND_DURATION = 60
FLAG_DURATION = ROUND_DURATION * 5
CHECKER_TIMEOUT = 30

GAME_FINISH_TIME = 1398755548 #timestamp