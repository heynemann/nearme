help:
	@echo "Available Targets:"
	@cat Makefile | egrep '^(\w+?):' | sed 's/:\(.*\)//g' | sed 's/^/- /g'

test:
	@env PYTHONPATH=.:$$PYTHONPATH pyvows vows/

requirements:
	@pip install -r requirements.txt

mongodb:
	@mkdir -p /tmp/cities
	@mongod --cpu --dbpath /tmp/cities --port 20000 --bind_ip 0.0.0.0 -rest
