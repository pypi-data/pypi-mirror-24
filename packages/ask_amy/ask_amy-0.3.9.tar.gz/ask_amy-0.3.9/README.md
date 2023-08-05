# ask_amy
Alex skills development framework for Python
pip install ask_amy -t /path/to/project-dir/dist

Minimize code maximize delivery
with ask_amy accelerators

##### framework promotion commands
* python setup.py register
* python setup.py sdist
* python setup.py sdist upload

ask-amy-cli create_lambda --deploy-json-file cli_config.json
ask-amy-cli deploy_lambda --deploy-json-file cli_config.json
ask-amy-cli logs --log-group-name /aws/lambda/insulin_calc_skill
ask-amy-cli create_template --skill-name alexa_scorekeeper_skill --role-name arn:aws:iam::280056172273:role/alexa_lambda_role --intent-schema-file speech_assets/intent_schema.json

sphinx-apidoc -o ask_amy/ ~/Code/AWS/alexa/ask_amy/ask_amy
find . -type d -name dist -exec rm -rf {} \;



