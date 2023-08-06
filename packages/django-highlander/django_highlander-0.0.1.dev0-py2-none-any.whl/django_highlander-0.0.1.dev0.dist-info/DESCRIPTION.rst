django-highlander
=================

There can be only one!

This is a Django `manage.py` Command class for long running tasks stated from crontab.

This will assure there is only one instance running at any time, so crontab will not be able to start a second
instance unless the previous one finished.

How to use
----------

Just inherit from Highlander instead of BaseCommand:

    from djangohighlander.command import Highlander

    class Command(Highlander):
        def handle(self, *args, **options):
            ...





