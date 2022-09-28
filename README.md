# BDD Behave Test Examples

## Clone the repo

## Navigate to your local repo and setup virtual env

    python -m venv bdd_env 
    . bdd_env/bin/activate
	pip install -r requirements.txt


### Populate .env
    
Create a file called `.env` in the root of repo add envvars for, at least:

    USER_NAME=<user_name>
    USER_PASSWORD=<pass>

Available envvars include:
    HOST=qwiki.nixsolutions.com
    PORT=443
    SCHEME=https

### Run All tests 
    behave main/features/tests


### Run a specific feature
	behave main/features/tests/user_profile.feature

### Run test and display anything sent to stdout
	behave --no-capture main/features/tests/user_profile.feature

### Run test and display debug logging
    behave --logging-level=DEBUG --no-logcapture main/features/tests/user_profile.feature

### Run test matching a tag, ex: @smoke tags the tests of all our certified 2019 measures
    behave --tags=@smoke --logging-level=DEBUG --no-logcapture main/features/tests/user_profile.feature

### Run test and export the result in a file
    It is convenient when you run a long suite of tests in which the stdout logs exceed your terminal buffer.
    
    behave --junit --junit-directory=<your folder path> main/features/tests/user_profile.feature

### Run a targeted set of scenarios; does not support some un-escaped characters such as "(", ")"
    behave -n "<scenario starting with>" main/features/tests/user_profile.feature
    ex: behave -n "POST profile photo via UI" main/features/tests/user_profile.feature

## Troubleshooting
TBD
Will see what can be wrong and add solutions here
Check environment variables in your `.env` 
