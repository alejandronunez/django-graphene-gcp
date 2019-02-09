#!/usr/bin/env python
import os
import sys


def fixup_paths(path):
    """Adds GAE SDK path to system path and appends it to the google path
    if that already exists.
    Extracted from:
    https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/localtesting/runner.py
    """
    # Not all Google packages are inside namespace packages, which means
    # there might be another non-namespace package named `google` already on
    # the path and simply appending the App Engine SDK to the path will not
    # work since the other package will get discovered and used first.
    # This emulates namespace packages by first searching if a `google` package
    # exists by importing it, and if so appending to its module search path.
    try:
        import google
        google.__path__.append("{0}/google".format(path))
    except ImportError:
        pass

    sys.path.insert(0, path)


def main():
    """Extracted from:
    https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/localtesting/runner.py
    """
    # If the SDK path points to a Google Cloud SDK installation
    # then we should alter it to point to the GAE platform location.
    sdk_path = os.getenv('GAE_SDK_PATH', '/')

    if os.path.exists(os.path.join(sdk_path, 'platform/google_appengine')):
        sdk_path = os.path.join(sdk_path, 'platform/google_appengine')

    # Make sure google.appengine.* modules are importable.
    fixup_paths(sdk_path)

    # Make sure all bundled third-party packages are available.
    import dev_appserver
    dev_appserver.fix_sys_path()

    # Loading appengine_config from the current project ensures that any
    # changes to configuration there are available to all tests (e.g.
    # sys.path modifications, namespaces, etc.)
    try:
        import appengine_config
        (appengine_config)
    except ImportError:
        print('Note: unable to import appengine_config.')

    # Staring stub to use Google App Engine apis outside of dev_appserver.py
    from google.appengine.ext.testbed import Testbed

    testbed = Testbed()
    testbed.activate()

    testbed.init_taskqueue_stub(root_path=os.path.join(os.path.dirname(__file__)))
    testbed.init_app_identity_stub()
    testbed.init_memcache_stub()


if __name__ == "__main__":
    main()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    TEST_MODE = False if os.environ.get('TEST_MODE', 'False') == 'False' else True
    TEST_MODE_COVERAGE = False if os.environ.get('TEST_MODE_COVERAGE', 'False') == 'False' else True

    if TEST_MODE and TEST_MODE_COVERAGE:
        import coverage

        cov = coverage.coverage(
            source=['.'],
            branch=True,
            omit=[
                '*/migrations/*',
                '*/test/*',
                'vendor/*',
                '*/__init__.py',
                'api/wsgi.py',
                'api/urls.py',
                'images/urls.py',
                'accounts/urls.py',
                'manage.py',
                'appengine_config.py',
                '*_dev.*',
                'api/tasks.py',
                'features/*',
                'accounts/indices.py',
            ]
        )
        cov.erase()
        cov.start()

    execute_from_command_line(sys.argv)

    if TEST_MODE and TEST_MODE_COVERAGE:
        cov.stop()
        cov.save()
        cov.report()

        cov.xml_report(outfile='./../dev/cover/coverage.xml')
        cov.html_report(directory='./../dev/cover')
