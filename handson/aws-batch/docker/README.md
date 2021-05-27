# docker image for training mnist

Read the following to debug or customize the program.

1. Edit Python libraries

    If you need other python libraries, edit `Dockerfile`.
    Then build the image by
    ```
    docker build -t mymnist .
    ```

1. Edit `main.py` and `simple_mnist.py`

    Launch the docker container with an interactive mode.
    We use `--gpus device=0` flag so that the container can access the host GPU.
    Also, we mount the current directory in the container so that the edits to the files are directly reflected in the container:
    ```
    docker run -it --gpus device=0 -v ${PWD}:/data mymnist
    ```
    In side the container, go to `/data` and run `main.py`.
    For example,
    ```
    $ cd /data
    $ python3 main.py
    ```

1. Repeat 1 and 2 until the code runs successfully.
