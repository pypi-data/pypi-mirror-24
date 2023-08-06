daiquiri-rollbar
=================

Easy way to integrate `Rollbar <http://rollbar.com/>`__ into `daiquiri <http://daiquiri.readthedocs.io/en/latest/>`__.

The level of the messages is preserved. So ``logger.info('smth')`` will be registered as ``info`` in Rollbar. If you configure daiquiri to log messages above a certain level, only those messages will be sent to Rollbar.

Exception should be logged with ``logger.exception``. The stacktrace will then be sent to Rollbar with ``report_exc_info``.

To use it, just add ``RollbarOutput`` to the list of daiquiri outputs and use daiquiri normally:

.. code:: python

    from daiquiri_rollbar import RollbarOutput

    rollbar_output = RollbarOutput(access_token='access_token')
    daiquiri.setup(
        level=logging.INFO,
        outputs=(rollbar_output,)
    )
    logger = daiquiri.getLogger(__name__)

    logger.info('Test')

By default, log messages will be logged for production. To change the environment, build ``RollbarOutput`` like this:

.. code:: python

    rollbar_output = RollbarOutput(access_token='access_token', environment='development')
