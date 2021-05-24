Object Storage
--------------

By default, Pulp uses the local filesystem for storage. If you want to use another storage backend such as Amazon Simple Storage Service (S3) or Azure, you’ll need to configure Pulp. To add an Amazon S3 or Azure backend for Pulp using the installer, in your playbook, you must set the necessary variables for your cloud storage in the `pulp_settings` variable of the `pulp_common` role.

1. Create and configure your Amazon S3 or Azure account and gather the credentials that you need to configure the storage backend with Pulp. Follow the instructions in [our Pulpcore storage docs](https://docs.pulpproject.org/pulpcore/installation/storage.html).
2. View the [example playbooks](https://github.com/pulp/pulp_installer/tree/master/playbooks) and note the `pulp_settings` variables for your chosen storage type. Add an entry for each of the variables for your deployment.
3. Use the following examples to populate your own variables in your playbook:

Azure example:
```yaml
pulp_settings:
  secret_key: secret
  content_origin: "{{ pulp_webserver_disable_https | default(false) | ternary('http', 'https') }}://{{ ansible_fqdn }}"
  azure_account_name: 'Storage account name'
  azure_container: 'Container name (as created within the blob service of your storage account)'
  azure_account_key: 'Key1 or Key2 from the access keys of your storage account'
  azure_url_expiration_secs: 60
  azure_overwrite_files: 'True'
  azure_location: 'the folder within the container where your pulp objects will be stored'
  default_file_storage: 'storages.backends.azure_storage.AzureStorage'
```

Amazon S3 example:
```yaml
pulp_settings:
  secret_key: secret
  content_origin: "{{ pulp_webserver_disable_https | default(false) | ternary('http', 'https') }}://{{ ansible_fqdn }}"
  aws_access_key_id: 'AWS Access Key ID'
  aws_secret_access_key: 'AWS Secret Access Key'
  aws_storage_bucket_name: 'pulp3'
  aws_default_acl: "@none None"
  s3_use_sigv4: True
  aws_s3_signature_version: "s3v4"
  aws_s3_addressing_style: "path"
  aws_s3_region_name: "eu-central-1"
  default_file_storage: 'storages.backends.s3boto3.S3Boto3Storage'
  media_root: ''
```
