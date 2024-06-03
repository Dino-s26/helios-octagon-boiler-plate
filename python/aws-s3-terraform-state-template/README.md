## How to use the script

1. Install requirement library on `requirements.txt`, use:

``` 
pip install -r requirements.txt 
```

2. To generate the `.tf` file, use:

```
python3 s3-tfstate.py <name_of_the_module> <module_version> <s3_name> <environment> <name_of_the_backend_file>

Example:
> python3 s3-tfstate.py s3_tf_state_module 1.4.1 s3_tfstate dev se_tfstate
```

3. Check the template on `backend` folder and use it to create the new S3 Backend