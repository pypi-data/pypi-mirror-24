AWS SAML Authorization Script.
==============================

This is a tool to authenticate to Amazon Web Services using the ADFS
SAML provider and create temporary tokens for use with AWS API clients.

Two approaches
--------------

If you have Docker installed on your workstation, you can run the
pre-built docker image directly from Quay. Since this approach requires
a number of parameters to be passed in as environment variables, you
will probably want to create a set of shell aliases, functions, or
scripts; we give examples below, and the git repo
(https://github.com/turnerlabs/samlkeygen) includes a file
``docker-aliases.bash`` setting up the commands refrenced below; the
definitions may also be found at the bottom of this README.

If you have Python installed on your workstation and prefer to run the
script locally, you can install the module from ``PyPI`` with
``pip install samlkeygen``. This installs scripts corresponding to the
docker aliases, so you will automatically have a ``samld`` command in
your $PATH once you install the module - even on Windows.

Of course, you can also always clone the git repository and use the
source directly. Pull requests with improvements are always welcome!

MacOS Note
~~~~~~~~~~

On modern versions of MacOS, the stock Python install doesn't include
``pip``. Even if you install pip (e.g. with ``easy_install``), it will
wind up trying to overwrite some readonly system files when installing
some of the packages required by samlkeygen. So for this to work under
MacOS you should install a separate instance of Python, via Homebrew,
MacPorts, virtualenv, or pyenv.

Required information
~~~~~~~~~~~~~~~~~~~~

The script requires some parameters that are specific to your
environment in order to work; if you don't understand what these are,
then ask someone in cloud operations or administration in your
organization. The easiest approach is probably to set these in the
environment in your shell startup files and then forget about them.

+------------+------------------------+----------------------------------------------+
| Option     | Environment Variable   | Description                                  |
+============+========================+==============================================+
| --url      | ADFS\_URL              | Complete URL to ADFS SAML endpoint for AWS   |
+------------+------------------------+----------------------------------------------+
| --domain   | ADFS\_DOMAIN           | Active Directory/ADFS domain name            |
+------------+------------------------+----------------------------------------------+
| --user     | USER                   | Your Active Directory sAMAccountName         |
+------------+------------------------+----------------------------------------------+

Depending on your environment, you may also have to be on your corporate
LAN or VPN in order to authenticate. Once you have keys for a profile,
though, those should work from anywhere until they expire.

Quick start
~~~~~~~~~~~

``samlkeygen`` has two basic functions: the primary one is
authentication mode, which connects to the ADFS endpoint, authenticates,
and gets authorization tokens for the user's defined SAML roles. The
secondary function is a set of mechanisms for easily selecting a profile
from the AWS credentials file for a command, without having to specify
the full profile name.

Authentication
^^^^^^^^^^^^^^

SAML-based credentials are only good for an hour (a hard AWS-imposed
limit). To make this limit less inconvenient, ``samlkeygen`` provides a
mode of operation that requests your password once, then runs
continually and automatically requests new credentials every hour before
the old ones expire. The supplied aliases/ entry points include
``samld``, which can be run without arguments if the environment
variables are set properly, or with just ``-u sAMAccountName`` if that
isn't the same as your local ``$USER`` on your workstation. Example:

::

    $ samld -u gpburdell
    ...
    Writing credentials for profile aws-shared-services:aws-shared-services-admin
    Writing credentials for profile aws-shared-services:aws-shared-services-dns
    Writing credentials for profile aws-ent-prod:aws-ent-prod-admin
    Writing credentials for profile cdubs:aws-cdubs-admin
    58 minutes till credential refresh

Profile selection
~~~~~~~~~~~~~~~~~

The authentication tokens will be written out to your credentials file
with a separate profile for each SAML role, named
``$ACCOUNT_ALIAS:$ROLE_NAME``. You can get a list of your profiles by
running the ``list-profiles`` subcommand, which takes an optional
parameter to restrict the output to those profiles matching a substring
(really a regular expression). There's an ``awsprofs`` alias/entry point
for this functionality:

::

    $ awsprofs shared-services
    aws-shared-services:aws-shared-services-admin
    aws-shared-services:aws-shared-services-dns-cnn

These are normal AWS profiles and can be used like any other, by
supplying the ``--profile`` option to whatever AWS CLI command you are
running, or setting the ``AWS_PROFILE`` environment variable (or
``AWS_DEFAULT_PROFILE`` for some older tools).

However, since the autogenerated names are somewhat long, the script
also has a subcommand that lets you select a profile via substring or
regular expression match: ``select-profile`` works just like
``list-profiles``, but requires that the pattern match exactly one
profile. The supplied aliases/entry points include one called
``awsprof`` (singular) for this use case:

::

    $ awsprof shared-services
    samlkeygen.py: Pattern is not unique. It matches these profiles:
            aws-shared-services:aws-shared-services-admin
            aws-shared-services:aws-shared-services-dns-cnn

If the pattern does match one profile, that profile's full name is
output by itself; the intent is to use the command in
command-substitution:

::

    $ aws --profile $(awsprof shared-services-admin) iam list-account-aliases
    {
        "AccountAliases": [
            "aws-shared-services"
        ]
    }

Finally, if you are running the local Python version, you can ask the
script to run a command for you under a given profile. The pip-installed
entry poitns include one called ``awsrun`` for this function; there's no
corresponding Docker alias because the Docker container would have to
include the AWS command-line tool you wanted to run this way.

That lets me replace the above example with this:

::

    $ awsrun shared-services-admin aws iam list-account-aliases
    {
        "AccountAliases": [
            "aws-shared-services"
        ]
    }

You can get detailed help about the various options by running
``samlkeygen`` directly (via Docker or Python) with the ``--help`` flag.

The Docker aliases
^^^^^^^^^^^^^^^^^^

::

    alias samld='docker run -it --rm -v "${AWS_DIR:-$HOME/.aws}:/aws" -e "USER=$USER" \
                 -e "ADFS_DOMAIN=$ADFS_DOMAIN" -e "ADFS_URL=$ADFS_URL" \
                 quay.io/turner/samlkeygen authenticate --all-accounts --auto-update'
    alias awsprofs='docker run --rm -v ~/.aws:/aws quay.io/turner/samlkeygen list-profiles'
    alias awsprof='docker run --rm -v ~/.aws:/aws quay.io/turner/samlkeygen select-profile'
