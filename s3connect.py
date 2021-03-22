import boto3
from os import path
from PIL import Image, ImageOps, ImageFilter


def upload_file(file_name, bucket):
  object_name = file_name
  output = f"uploads/{file_name}"
  s3_client = boto3.client('s3')
  response = s3_client.upload_file(output, bucket, object_name)
  return response 

def download_file(file_name, bucket):
  s3 = boto3.resource('s3')
  output = f"downloads/{file_name}"
  s3.Bucket(bucket).download_file(file_name, output)
  return output

def list_files(bucket):
  s3 = boto3.client('s3')
  contents = []
  try:
    for item in s3.list_objects(Bucket=bucket)['Contents']:
      print(item) 
      contents.append(item)
  except Exception as e:
    pass
  return contents


def apply_filter(file_name, preset, bucket):
  s3 = boto3.resource('s3')
  inputfile = f"downloads/{file_name}"
  if path.exists(inputfile) != True:
    download_file(file_name, bucket)
  
  im = Image.open(inputfile)
  im = im.convert("RGB")
  if preset == 'Gray':
    im = ImageOps.grayscale(im)
  elif preset == 'Edge':
    im = ImageOps.grayscale(im)
    im = im.filter(ImageFilter.FIND_EDGES)
  elif preset == 'Poster':
    im = ImageOps.posterize(im,3)
  elif preset == 'Solar':
    im = ImageOps.solarize(im, threshold=80) 
  elif preset == 'Blur':
    im = im.filter(ImageFilter.BLUR)
  elif preset == 'Sepia':
    sepia = []
    r, g, b = (255, 240, 192)
    for i in range(255):
      sepia.extend((r*i//255, g*i//255, b*i//255))
    im = im.convert("L")
    print(im.mode)
    im = ImageOps.autocontrast(im)
    im.putpalette(sepia)

  f = file_name.split(".")
  outputfilename = f"{f[0]}-{preset}.jpeg"
  outputfile = f"uploads/{outputfilename}"

  im = im.convert("RGB")
  im.save(outputfile, format="JPEG")
  upload_file(outputfilename, bucket)
  return outputfilename

def delete_objects(objects, bucket):
	s3_client = boto3.client('s3')
	response = s3_client.delete_objects(Bucket=bucket, Delete=objects)
	return response

