USER_KEY="keys/Final_proj.pem"
DNS="ec2-34-212-20-123.us-west-2.compute.amazonaws.com"
ssh -i ${USER_KEY} ubuntu@${DNS}
