
# 🚀 Guide: Deploying EC2 Infrastructure with Docker & Terraform  
### 💡 Course: Continuous Integration and Delivery

This guide will walk you through using **AWS** and a pre-built **Docker image** to automatically create a launch template and SSH key for EC2 — without needing to learn or write any Terraform code.

---

## 📋 Prerequisites

- An AWS account → [https://aws.amazon.com](https://aws.amazon.com)
- Docker installed → [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- Basic terminal knowledge

---

## 🛡️ Step 1: Create an IAM Admin User in AWS

1. Go to the [IAM Console](https://console.aws.amazon.com/iam/home#/users)
2. Click **“Add users”**
3. Enter a username (e.g. `terraform-admin`) and click **Next**
4. Select **Attach policies directly**
5. Search for `AdministratorAccess` and ✅ check it
6. Click **Next → Create user**

---

## 🔐 Step 2: Generate Access Keys

1. Click on the user you just created (`terraform-admin`)
2. Go to the **Security credentials** tab
3. Scroll to **Access keys**, and click **“Create access key”**
4. Choose **“Application running outside AWS”**
5. Click **Next → Create access key**
6. ✅ **Save your Access Key ID and Secret Access Key** — this is your only chance to copy them

---

## 🐳 Step 3: Run the Docker Image to Create Infrastructure

Paste this command into your terminal (replace credentials with your own):

```bash
docker run --rm \
  -e AWS_ACCESS_KEY_ID=your-access-key-id \
  -e AWS_SECRET_ACCESS_KEY=your-secret-access-key \
  -e AWS_DEFAULT_REGION=eu-central-1 \
  stefan5andonov/kiii-terraform-aws-ec2-template:latest > terraform-log.txt
```

> 💡 This runs Terraform inside Docker and automatically creates a launch template, security group, IAM profile, and key pair.

---

## 🔑 Step 4: Save Your SSH Private Key

Terraform will print an SSH private key into the logs. Run this to extract it:

```bash
awk '/^-----BEGIN RSA PRIVATE KEY-----/,/^-----END RSA PRIVATE KEY-----/' terraform-log.txt > kiii-key.pem
chmod 400 kiii-key.pem
```

---

## 🖥️ Step 5: Launch an EC2 Instance from the Template

1. Go to the [EC2 Console](https://console.aws.amazon.com/ec2/home)
2. In the left menu, click **Launch Templates**
3. Locate the template called `kiii-template-ac`
4. Click **Actions → Launch instance from template**
5. Accept defaults and click **Launch**

---

## 🌐 Step 6: Connect to Your EC2 Instance via SSH

1. Go to **EC2 → Instances**
2. Copy the **Public IPv4 address**
3. Connect from terminal using:

```bash
ssh -i kiii-key.pem ec2-user@<your-instance-ip>
```

Example:
```bash
ssh -i kiii-key.pem ec2-user@3.123.45.67
```

---

## 🔧 Preinstalled Tools on the Instance

- Docker 🐳
- Docker Compose ⚙️
- Git ✅
- AWS SSM Agent (for Systems Manager access)

---

## 🧹 Step 7: Cleanup

To avoid AWS charges:
- Go to **EC2 → Instances** → Terminate unused instances

---

## ❗ Common Issues

| Problem | Solution |
|--------|----------|
| `Permission denied (publickey)` | Ensure you’re using the correct `.pem` file and correct IP |
| SSH timeout | Make sure port 22 is open and instance is running |
| Docker permission error | Use `sudo docker` or adjust Docker Desktop permissions |
| AWS permission error | Confirm the IAM user has `AdministratorAccess` |

---

Created by [@stefan5andonov](https://hub.docker.com/r/stefan5andonov)  
Docker image: `stefan5andonov/kiii-terraform-aws-ec2-template:latest`
