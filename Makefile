TARGETS := imported gamesok referees gamegroups gameschedule scores

default: run_test

run_test:
	rm -f output.txt
	python3 test_project.py $(ARGS) >> output.txt 2>&1

$(TARGETS):
	rm -f output.txt
	python3 test_project.py $@ >> output.txt 2>&1