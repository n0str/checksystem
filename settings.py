
teams = [
    (1, 'Yozik', '127.0.0.1'),
    (2, 'keva', '127.0.0.2')
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

checker_work_timeout = 15 * 1000


ROUND_DURATION = 30
FLAG_DURATION = ROUND_DURATION * 5
CHECKER_TIMEOUT = 5