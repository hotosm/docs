# AWS Roles And Permissions (IAM)

This can be a deep rabbit hole to go down - we will try and keep it simple!

In general, we can consider these access options:

- **IAM User**: for _people_. Long-term access keys. Generally for manual
  user usage.
- **IAM Role**: for _code_. Temporary credentials via OIDC, STS, etc,
  for usage in things like Github workflows.
- **Resource Policy**: permissions directly on a _service_ (e.g. S3 bucket).
- Other AWS-specific ways to login such as EC2 instance profiles
  (granting an EC2 machine access to certain things by default),
  or IAM roles for service accounts used with Kubernetes.

It may be possible to use a bit of the above, and conflict can occur,
so it's key to be consistent for what type of configuration you set.

## S3 Bucket Permissions

- There are two key things to consider:
  1. Bucket permissions: which bucket, and what permissions.
  2. CORS policy: which websites can access the bucket.

### Bucket Permissions

- The simplest way to access a bucket (e.g. from AWS CLI):
  - Create an IAM user.
  - Grant the user permission to read/write the specific bucket.

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": ["s3:GetObject", "s3:PutObject"],
          "Resource": "arn:aws:s3:::my-example-bucket/*"
        }
      ]
    }
    ```

  - Generate access credentials for the IAM user.
  - Login to your terminal or app using the provided credentials.

- For pushing to buckets from CI/CD workflows, it might be best
  to use temporary credentials granted via
  [OIDC & roles](https://aws.amazon.com/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws).
- For accessing a bucket from an EC2 instance,
  [EC2 instance profiles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html)
  may be best.
- Example policy written **directly on the bucket** instead:

  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "NameThePolicyWhateverYouWant",
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::123456789012:role/my-ci-role"
        },
        "Action": ["s3:GetObject", "s3:PutObject"],
        "Resource": "arn:aws:s3:::my-example-bucket/*"
      }
    ]
  }
  ```

### Bucket CORS Policy

To simply allow access from all sites, use:

```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedHeaders": ["*"]
    }
  ]
}
```

To grant specific access to different sites, use:

```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://example.com", "https://app.example.org"],
      "AllowedMethods": ["GET", "HEAD", "PUT"],
      "AllowedHeaders": ["Authorization", "Content-Type"],
      "ExposeHeaders": ["ETag"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```
