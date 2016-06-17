# Sopel IRC bot Docker config

Run the Sopel IRC bot in a Docker container.

## Building

```
docker build -t boxbox/sopel .
```

## Running

Create a directory where you want to store the config, log and data files (can
also be a volume container); adjust the name to your likings:

```
mkdir /tmp/mybot
```

This Docker config does use an unprivileged user in the container for increased
security. Therefore you have to give the ownership to the _sopel_ user:

```
chown -R 1000:1000 /tmp/mybot
```

Initialize the bot configuration:

```
docker run --rm -it -v /tmp/mybot:/home/sopel/.sopel boxbox/sopel sopel -w
```

Create and run the bot:

```
docker run -d --name mybot -v /tmp/mybot:/home/sopel/.sopel boxbox/sopel
```

If you want it to autostart, add `--restart=always`.

## Running Sopel commands

You can, at any time, run specific Sopel commands. For example:

```
docker run --rm -it -v ... boxbox/sopel sopel --configure-modules
```
