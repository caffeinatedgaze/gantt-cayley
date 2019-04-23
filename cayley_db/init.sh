dropdb -U postgres quads
createdb -U postgres quads
./cayley init -c config.yml
./cayley load -c config.yml -i generated_db.nq
./cayley http -c config.yml --host=:64210
