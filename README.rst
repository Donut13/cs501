Create venv
===========

.. code-block:: bash

   python3 -m venv venv

Activate venv
=============

.. code-block:: bash

   . venv/bin/activate

Install Dependencies
====================

.. code-block:: bash

   pip install -r requirements.txt

Initialize Database
===================

.. code-block:: bash

   env FLASK_ENV=development flask init-db

Run Web Server in Development Mode
=======================

.. code-block:: bash

   env FLASK_ENV=development flask run
