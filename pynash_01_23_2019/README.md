# PyNash Presentation 01-23-2019
### Notes
 - You can run the Flask app directly with `python src/app.py`
 - You can build the Docker image with `docker build -t {tag_name} .`
 - Once built, you can run the Flask app in Docker with `docker run -p 5000:5000 --name={friendly_name} {tag_name}`
	- `{friendly_name}` is an optional parameter, otherwise docker will assign one
	- `-p 5000:5000` maps your localhost port to the containers, otherwise you can't access it over the network
	- Add a `-d` after `run` to run the image in a detached state
 - You can run `docker stop {friendly_name} & docker rm {friendly_name}` to kill the instance
 - You can run `docker-compose build` to build both the example Flask app and an NGINX image
 - You can run `docker-compose up` to start both the Flask app and NGINIX app
	- The settings in `nginx.conf` map `localhost:1337` to the Flask app
	- You can add `-d` after `up` to start them in a detached state
 - You can run `docker-compose down` to tear down the instances, or press `Ctrl+C` if not in detached mode
 - You can always use `docker ps -a` to see container instances on your machine


### Useful Reads
 - [Docker Docs](https://docs.docker.com/)
 - [Docker Hub for Public Image Repos](https://hub.docker.com/)

### Example Deployment
 - Given you have:
	- A public IP mapped to a running server ( Like an [Elastic IP](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) associated with an [EC2 Instance](https://aws.amazon.com/ec2/) )
	- Change the `ports` configuration in `docker-compose.yml` to `80:80`
- Build and stand up the `docker-compose.yml` file