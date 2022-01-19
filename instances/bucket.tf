resource "aws_s3_bucket" "b" {
  bucket = var.bucket_name
  acl = var.bucket_acl
}

resource "aws_s3_bucket_policy" "allow_access_from_another" {
  bucket = aws_s3_bucket.b.id
  policy = data.aws_iam_policy_document.allow_access_from_another.json
}

data "aws_iam_policy_document" "allow_access_from_another" {
  statement {
    principals {
      type = "AWS"
      identifiers = ["892573513811"]
    }

    actions = [
      "s3:PutObject",
      "s3:GetObject"
    ]

    resources = [
      aws_s3_bucket.b.arn,
      "${aws_s3_bucket.b.arn}/*",
    ]
  }
}

