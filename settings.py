
teams = [
    (0, 'Yozik', '127.0.0.1'),
    (1, 'keva', '10.53.255.3')
]

services = [
	(0, 'php', 80),
	(1, 'perl', 40),
	(2, 'python', 9001)
]

db_settings = {
	"host" : "localhost",
	"user" : "root",
	"password" : "byrfgcekzwbz",
	"db" : "classic-ctf"
}

queues_names = ['q1', 'q2', 'q3']
queue_len = 3

checker_work_timeout = 15 * 1000


ROUND_DURATION = 30
FLAG_DURATION = ROUND_DURATION * 5
CHECKER_TIMEOUT = 15

GAME_FINISH_TIME = 10