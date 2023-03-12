# Chronicle

How to run:

-   Rename .env/.local/.django.template to .django
-   Change environment settings value on .django
-   chmod +x do
-   ./do setup

Visit localhost:8090/api/swagger/

Run test case:

-   create Python 3.9.10 virtualenv
-   activate virtualenv
-   cd chronicle
-   pip install -r tests/requirements.txt
-   export PYTHONPATH=/:tests/
-   python -m pytest --ds=component.test_settings tests/component

## FAQs

1. DB port already in used

-   If you have port conflict, change mysql port in local.yaml and change .django settings accordingly
