resource "aws_iam_role" "test_role" {
  name = "test_role"
  
  assume_role_policy = jsonencode ({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    tag-key = "love is the answer"
  }
}

# Allows to attach to EC2 instance
resource "aws_iam_instance_profile" "test_profile" {
  name = "test_profile"
  role = aws_iam_role.test_role.name
}

resource "aws_iam_role_policy" "test_policy" {
  name = "test_policy" 
  role = aws_iam_role.test_role.id 

  policy = jsonencode ({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["s3:*", "ec2:*"]
        Effect = "Allow"
        Resource: "*"
      },
    ]
  })
}
