Django eXtra Test Cases
^^^^^^^^^^^^^^^^^^^^^^^

Django's test cases focus on test cases for use with a database.

This is excellent as it is the hardest thing to do right. Yet, when creating
(reusable) apps that do not have any models or testing views that do not use
any models, you often find yourself doing the same thing with SimpleTestCase.

This issue is the focus of Django XTC.

TemplateTestCase
^^^^^^^^^^^^^^^^

The core test case for testing templates. Requires a template test directory
which can be set on the class level and will fall back to TEMPLATE_TEST_DIR
using Django's settings_.

Below this directory, at least two subdirectories are used:

    - ``src``: The template code
    - ``expect``: The expected output of that template code
    - ``actual``: (optional) Used if the output is to be saved for post-mortem
        analysis.

At the core is the test method `assertTemplateEqual`, which compares the
expected template code with the actual. The template context (the variables)
can be manipulated using the `template_context` attribute.

.. _settings: https://docs.djangoproject.com/en/1.11/topics/settings/
