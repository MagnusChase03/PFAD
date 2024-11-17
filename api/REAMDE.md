## Installation

```
mkdir python
pip3 install pandas scikit-learn -t ./python
zip -9 -r layer.zip python
```

## Deploy

```
terraform apply -var-file=prod.tfvars
```
