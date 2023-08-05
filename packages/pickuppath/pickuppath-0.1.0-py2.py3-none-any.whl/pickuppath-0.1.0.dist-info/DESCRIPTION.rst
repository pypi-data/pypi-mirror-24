pickuppath
========================================

pickup file path.

detail
----------------------------------------

The stragegy of finding file path, following below.

.. code-block:: bash

  $ pwd
  $HOME/vboxshare/venvs/work
  $ pickuppath --debug .config.ini
  DEBUG:pickuppath:check: $HOME/vboxshare/venvs/work/.config.ini
  DEBUG:pickuppath:check: $HOME/vboxshare/venvs/.config.ini
  DEBUG:pickuppath:check: $HOME/vboxshare/.config.ini
  DEBUG:pickuppath:check: $HOME/.config.ini
  $HOME/.config.ini


if file path is not found, then, lookup `~/.config.ini`.

as python function
----------------------------------------

.. code-block:: python

  from pickuppath import pickup_path

  print(pickup_path("config.ini", current="~/venv/py/work/"))






