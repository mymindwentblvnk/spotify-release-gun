docker-build:
	make docker-clean
	sudo docker build -t gun-image --no-cache=true .

docker-clean:
	-sudo docker rm -f gun-container;
	-sudo docker rmi gun-image

docker-run:
	sudo docker run --rm -a stdout -a stderr --name gun-container -v $(shell pwd):/gun -i gun-image /bin/bash -c "python gun.py"

docker-build-and-run:
	make docker-build
	make docker-run
	make docker-clean
