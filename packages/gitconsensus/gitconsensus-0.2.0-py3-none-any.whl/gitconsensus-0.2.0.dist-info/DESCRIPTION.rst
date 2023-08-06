GitConsensus
============

This simple project allows github projects to be automated. It uses
"reaction" as a voting mechanism to automatically merge (or close) pull
requests.

Consensus Rules
---------------

The file ``.gitconsensus.yaml`` needs to be placed in the repository to
be managed. Any rule set to ``false`` or ommitted will be skipped.

.. code:: yaml


    # Add extra labels for the vote counts and age when merging
    extra_labels: false

    # Minimum number of voters
    quorum: 5

    # Required percentage of "yes" votes (ignoring abstentions)
    threshold: 0.65

    # Only process votes by contributors
    contributors_only: false

    # Only process votes by collaborators
    collaborators_only: false

    # When defined only process votes from these github users
    whitelist:
      - alice
      - bob
      - carol

    # Number of days after last action (commit or opening the pull request) before issue can be merged
    mergedelay: 3

    # Number of days after last action (commit or opening the pull request) before issue is autoclosed
    timeout: 30

Voting
------

Votes are made by using reactions on the top level comment of the Pull
Request.

+--------------+-----------+
| Reaction     | Vote      |
+==============+===========+
| |+1|         | Yes       |
+--------------+-----------+
| |-1|         | No        |
+--------------+-----------+
| |confused|   | Abstain   |
+--------------+-----------+

Label Overrides
---------------

Any Pull Request with a ``WIP`` or ``DONTMERGE`` label (case
insensitive) will be skipped over.

Commands
--------

Authentication
~~~~~~~~~~~~~~

.. code:: shell

    gitconsensus auth

You will be asked for your username, password, and 2fa token (if
configured). This will be used to get an authentication token from
Github that will be used in place of your username and password (which
are never saved).

Merge
~~~~~

Merge all pull requests that meet consensus rules.

.. code:: shell

    gitconsensus merge USERNAME REPOSITORY

Close
~~~~~

Close all pull requests that have passed the "timeout" date (if it is
set).

.. code:: shell

    gitconsensus close USERNAME REPOSITORY

Info
~~~~

Get detailed infromation about a specific pull request and what rules it
passes.

.. code:: shell

    gitconsensus info USERNAME REPOSITORY PR_NUMBER

Force Close
~~~~~~~~~~~

Close specific pull request, including any labels and comments that
normally would be sent.

.. code:: shell

    gitconsensus forceclose USERNAME REPOSITORY PR_NUMBER

Force Merge
~~~~~~~~~~~

Merge specific pull request, including any labels and comments that
normally would be sent.

.. code:: shell

    gitconsensus forcemerge USERNAME REPOSITORY PR_NUMBER

.. |+1| image:: https://assets-cdn.github.com/images/icons/emoji/unicode/1f44d.png
.. |-1| image:: https://assets-cdn.github.com/images/icons/emoji/unicode/1f44e.png
.. |confused| image:: https://assets-cdn.github.com/images/icons/emoji/unicode/1f615.png



