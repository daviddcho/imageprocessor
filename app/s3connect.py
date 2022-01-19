import boto3
from os import path
from PIL import Image, ImageOps, ImageFilter

def upload_file(filename, bucket):
  output = f"uploads/{filename}"
  client = boto3.client('s3')
  response = client.upload_file(output, bucket, filename)
  return response 

def download_file(filename, bucket):
  s3 = boto3.resource('s3')
  output = f"downloads/{filename}"
  s3.Bucket(bucket).download_file(filename, output)
  return output

def list_files(bucket):
  s3 = boto3.client('s3')
  contents = []
  try:
    for item in s3.list_objects(Bucket=bucket)['Contents']:
      contents.append(item)
  except Exception as e:
    pass
  return contents

def apply_filter(filename, preset, bucket):
  s3 = boto3.resource('s3')
  inp = f"downloads/{filename}"
  if path.exists(inp) != True:
    download_file(filename, bucket)
  
  im = Image.open(inp)
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
    im = ImageOps.autocontrast(im)
    im.putpalette(sepia)

  name = filename.split(".")[0]
  outname = f"{name}-{preset}.jpeg"
  outf = f"uploads/{outname}"

  im = im.convert("RGB")
  im.save(outf, format="JPEG")
  upload_file(outname, bucket)
  return outname

def delete_objects(objects, bucket):
  client = boto3.client('s3')
  response = client.delete_objects(Bucket=bucket, Delete=objects)
  return response

