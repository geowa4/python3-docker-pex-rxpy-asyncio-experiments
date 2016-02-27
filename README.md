Python 3 + Docker + pex + RxPy + asyncio
========================================

Why?
----

Recently, I had to extend a console script written in Python 3 that I needed to turn into something more reactive.
Since I have experience with [ReactiveX](http://reactivex.io/) in other languages, I knew it would be a great fit.
But I'm using Python 3, which has [asyncio](https://docs.python.org/3/library/asyncio.html).
How does that fit with RxPY?

OK, let's assume I figure out all that asynchrony.
As a believer of running what you build, I needed to figure out a way to simplify Python deployments.
I have a Docker infrastructure so that's a given.
The issue with that though is that the resulting Python images are ~750MB.

Enter [pex](https://github.com/pantsbuild/pex).
Using pex, I can encapsulate all my dependencies and custom modules into a single executable.
This allows me to use a much smaller base image.
While I could just build the pex file on my computer, I'd really like to keep the build contained in Docker so the casual hacker or my CI pipeline doesn't need to set up any virtual environments.

How?
----

Assuming you have Docker running, you can run this image and send it data with netcat.

```
# First terminal
docker run -it --rm -p 8888:8888 geowa4/python-pex-rxpy-asyncio-experiment
```

```
# Second terminal
echo foo | nc <docker-ip> 8888
```

The commands to build that image are located in `./build.sh`.
It might look complicated, but it's not that bad.
The fundamental piece of knowledge you must have is that the Docker build context doesn't need to be a path to a directory;
it can also be a `tar` stream.

To start, I use the `python:on-build` image that automatically pulls in my source and installs all the dependencies.
Then, I build the pex file.
Before anything else happens, I have a perfectly good Docker image that can run our project.
The default command is to `tar` out the current working directory, but that could be changed to run `bash`, `python`, or that pex file that was created.
The reason I'm not stopping here is that the image is way too large.
To get that, I need to build from `python:slim`, which has almost nothing in it besides `python`, and have as few layers as possible.
Luckily, all my dependencies and source code are encapsulated in a single pex file whose only dependency is `python`.
To get it, I run the big image I just made which sends the current working directory to standard out as a `tar` stream and pipe it into a `docker build` command that is set to take its build context from standard input.
This stream must contain a Dockerfile like all good build contexts, which it does.
If you want to see what's in that stream, redirect the builder image's standard out to a file and unarchive it with `tar`.

After all this, we're left with an image that's one-third the size.
I call that a success.

