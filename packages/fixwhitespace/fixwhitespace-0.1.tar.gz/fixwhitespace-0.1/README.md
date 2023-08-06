# fixwhitespace
Trim whitespace or convert tabs to spaces in a file or files in a directory.

run the tests in a container:
> $ docker run --rm -v $(pwd):/code --entrypoint python fixwhitespace -m pytest /code/tests

run them without a container:
> $ pytest

run the script:
> $ python -m fixwhitespace /path/to/dir extensions
