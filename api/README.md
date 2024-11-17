# Python Lambda API

*The code in this section is responsible for handling dataset uploads and processing.*

## Deploy

`prod.tfvars`
```
aws_auth_file = "/home/<user>/.aws/config"
aws_auth_profile = "<Profile>"
```

```bash
$ terraform apply -var-file=prod.tfvars
```
