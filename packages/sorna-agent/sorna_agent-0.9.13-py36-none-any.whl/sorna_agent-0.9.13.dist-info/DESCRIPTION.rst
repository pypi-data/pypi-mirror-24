Sorna Agent
===========

Package Structure
-----------------

 * sorna
   * agent: The agent server implementation

Installation
------------

Sorna Agent requires Python 3.5 or higher.  We highly recommend to use
`pyenv <https://github.com/yyuu/pyenv>`_ for an isolated setup of custom Python
versions that might be different from default installations managed by your OS
or Linux distros.

.. code-block:: sh

   pip install sorna-agent

Due to limitation in current version (9.0.1) of pip, you may encounter errors
while installing **aiodocker**.  In that case, run ``pip install -r
requirements.txt`` and try again.

For development:
~~~~~~~~~~~~~~~~

We recommend to use an isolated virtual environment.
This installs the current working copy and sorna-common as "editable" packages.

.. code-block:: sh

   git clone https://github.com/lablup/sorna-agent.git
   python -m venv venv-sorna
   source venv-sorna/bin/activate
   pip install -U pip setuptools wheel  # ensure latest versions
   pip install -r requirements-dev.txt

Deployment
----------

Running from a command line:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To handle uploads of generated files to AWS S3, you need to set several
environment variables.  If they are not set, the file upload feature is
disabled.  Currently we only support S3-based uploads.

.. code-block:: sh

   export AWS_ACCESS_KEY_ID="..."
   export AWS_SECRET_ACCESS_KEY="..."
   export AWS_REGION="..."     # e.g., ap-northeast-2
   export AWS_S3_BUCKET="..."  # e.g., my-precious-sorna
   python -m sorna.agent.server --manager-addr tcp://localhost:5001 --max-kernels 15

For details about arguments, run the server with ``--help``.

Example supervisord config:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: dosini

   [program:sorna-agent]
   stopsignal = TERM
   stopasgroup = true
   command = /home/sorna/run-agent.sh
   environment = AWS_ACCESS_KEY_ID="...",AWS_SECRET_ACCESS_KEy="...",AWS_REGION="...",AWS_S3_BUCKET="..."

TCP Port numbers to open:
~~~~~~~~~~~~~~~~~~~~~~~~~

 * 6001: ZeroMQ-based internal agent control protocol
 * Docker REPL containers will use automatically-mapped host-side port numbers,
   and they do not need to be open to other hosts (localhost-only).
   Inside containers, the REPL daemons use the fixed port numbers: 2000-2003.


