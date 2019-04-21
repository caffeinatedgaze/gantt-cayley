./cayley init -c config.yml
./cayley load -c config.yml -i data/quads.nq
./cayley http -c config.yml --host=:64210
