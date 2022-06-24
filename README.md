# Lambda Function to Update Slack Groups with Current Responder on OpsGenie 

[[_TOC_]]

## The idea

The idea is to have this lambda manage groups in slack, according to the mappings file.

The groups will contain up-to-date current on-call member for that group

example: [slack<->opsgenie] -> `mappings.ini`
- oncall-devs: dev-rotation
- oncall-cs: cs-rotation

## API

Uses Slack Bolt API, bundled within the function dir

## Terraform

Terraform provides the lambda, AWS secret and cloudfront schedule and assings correct permissions for each

once deployed, you'll have to manually put json string into secret with the format: `{"slack": APIKEY, "opsgenie": APIKEY}`

`aws secretsmanager update-secret --secret-id $ARN --secret-string $VALUE`

## Future improvements

Move to an internal cluster?
