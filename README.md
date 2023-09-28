

### Setup env
#### Step 1: Install pyenv
#### Step 2: Setup env
```
    # Setup a virtual env
    pyenv virtualenv 3.8.13 lab-hcl
    # Install library
    pip install -r requirements.txt

```

### Build Dockerfile
```shell
    docker build -t huypham/data-integration:lastest -f Dockerfile .
```

### Start services
```shell

    cd path/env
    docker-compose up
    #docker-compose up --force-recreate

```
