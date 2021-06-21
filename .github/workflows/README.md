# CI/CD workflows

Currently 3 CI/CD workflows are defined:
- `gh-pages.yml`: This updates the HTML content of the GitHub pages.
- `docker-build.yml`: This builds a docker image to execute handson program and publish it to Docker Hub.
- `docker-build-qabot.yml`: This builds a docker image for question-answering app.

## Set up

- To push newly built images to Docker Hub, set the following parameters in the Action secrets:
  - `DOCKER_USERNAME`
  - `DOCKER_PASSWORD`
