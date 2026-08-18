# Python Async and Environment Basics

Python's asyncio library provides a way to write concurrent code using the
async/await syntax. An async function, when called, returns a coroutine
object rather than running immediately. Coroutines need to be scheduled on
an event loop, either by awaiting them inside another async function or by
running them with asyncio.run().

The difference between concurrency and parallelism matters here: asyncio
gives you concurrency on a single thread, meaning tasks can yield control
while waiting on I/O (like a network request), but it does not use
multiple CPU cores. For CPU-bound work, Python's multiprocessing module is
generally a better fit than asyncio.

Virtual environments isolate a project's dependencies from the system-wide
Python installation. The built-in venv module creates a self-contained
folder with its own Python interpreter and package directory. Activating a
virtual environment changes the shell's PATH so that "python" and "pip"
point to the isolated copies instead of the system ones.

Dependency files like requirements.txt list the exact packages (and
often exact versions) a project needs, so that "pip install -r
requirements.txt" recreates a consistent environment on another machine.
Pinning versions avoids the common "it works on my machine" problem caused
by different contributors having different package versions installed.

Environment variables are commonly used to store configuration values that
change between environments, such as database URLs or API keys, without
hardcoding them into source code. A .env file combined with a library like
python-dotenv is a common pattern for loading these variables during local
development.
