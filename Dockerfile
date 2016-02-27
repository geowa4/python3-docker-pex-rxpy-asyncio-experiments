FROM python:3.5-onbuild
RUN pex -r requirements.txt . -m experiment -o pex.pex && \
    mv Dockerfile.runtime Dockerfile && \
    mv .dockerignore.runtime .dockerignore
CMD [ "tar", "-cf", "-", "." ] 
