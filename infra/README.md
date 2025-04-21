# Infrastructure as Code (IaC) for Embrapa Viticulture API

This directory contains the Terraform configuration for deploying the Embrapa Viticulture API on AWS.

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured with credentials
- Terraform installed locally
- GitHub repository with GitHub Actions enabled
- SSH key pair for EC2 instance access

## Setup Instructions

1. Configure AWS credentials:
   ```bash
   aws configure
   ```

2. Initialize Terraform:
   ```bash
   cd infra
   terraform init
   ```

3. Plan the infrastructure:
   ```bash
   terraform plan
   ```

4. Apply the infrastructure:
   ```bash
   terraform apply
   ```

## GitHub Actions Setup

1. Add the following secrets to your GitHub repository:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `SSH_PRIVATE_KEY`: Your SSH private key for EC2 instance access

2. The GitHub Actions workflow will automatically:
   - Run on pull requests to validate changes
   - Deploy changes when merged to main branch
   - Post plan results as comments on pull requests
   - Deploy the application after infrastructure provisioning

## Deployment Process

The deployment process includes:

1. Infrastructure provisioning (EC2, VPC, etc.)
2. Application deployment:
   - System updates and package installation
   - Python virtual environment setup
   - Application code deployment
   - Systemd service configuration
   - Application service start

The application will be automatically deployed and started after the infrastructure is provisioned.

## Infrastructure Components

- VPC with public subnet
- Internet Gateway
- Route Table
- Security Group (allowing SSH and HTTP)
- EC2 Instance (t2.micro - Free Tier eligible)
  - Ubuntu 22.04 LTS
  - 8GB EBS volume (Free Tier eligible)

## Security Notes

- The security group allows SSH (port 22) and HTTP (port 80) from anywhere
- Consider restricting SSH access to specific IP ranges in production
- Use AWS Systems Manager Session Manager for secure access instead of SSH when possible
- The application runs under a dedicated systemd service
- The application directory is owned by the ubuntu user

## Cost Considerations

This infrastructure uses AWS Free Tier eligible resources:
- t2.micro instance
- 8GB EBS volume
- Basic networking components

Monitor your AWS usage to stay within Free Tier limits.

## Monitoring

To check the application status:
```bash
sudo systemctl status embrapa-viticulture
```

To view application logs:
```bash
sudo journalctl -u embrapa-viticulture -f
``` 