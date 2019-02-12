from __future__ import print_function
import boto3
import subprocess
import os
import sys
import uuid
import urllib
import urllib2
import ctypes
import logging
import glob
import hashlib

from PIL import Image
import PIL.Image

s3_client = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.error('Starting conversion')

#create lib if it does not exist
args = ("mkdir", "-vp",  "/var/task/lib/")
popen = subprocess.Popen(args, stdout=subprocess.PIPE)
popen.wait()
output = popen.stdout.read()
sys.stderr.write(output)

#copy all files to /var/task/lib/
for d, dirs, files in os.walk('lib'):
    for f in files:
        if f.endswith('.so'):
          args = ("cp", "-v", os.path.join(d, f), "/var/task/lib/")
          popen = subprocess.Popen(args, stdout=subprocess.PIPE)
          popen.wait()
          output = popen.stdout.read()
          sys.stderr.write("\nCopying file: " + output)

# reseize the image
def resize_image(image_path, resized_path, size):
  with Image.open(image_path) as image:
    width, height = image.size
    ratio=width/height
    if size=='small':
      if width>90:
        width=90
        height=height*90/width
      if height>=90:
        height=90
        width=width*90/height
    if size=='medium':
      if width > height:
        height=180
        width=180*width/height
      if height >= width:
        width=180
        height=180*height/width
    if size=='large':
      if width > height:
        height=270
        width=270*width/height
      if height >= width:
        width=270
        height=270*height/width

    image.thumbnail((width, height))
    image.save(resized_path)

# hook for lambda
def handler(event, context):
  for record in event['Records']:
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    sys.stderr.write("\nKey: " + key)
    sys.stderr.write("\nBucket: " + bucket)

    download_path = '/tmp/{}'.format(uuid.uuid4())
    png_path = '/tmp/resized-{}.png'.format(uuid.uuid4())

    sys.stderr.write("\nDownload path:" +  download_path)
    sys.stderr.write("\nPNG path: "  + png_path)
    s3_client.download_file(bucket, key, download_path)
    resize_image(download_path, png_path, 'medium')
    s3_client.upload_file(png_path, '{}-medium'.format(bucket), key )
    
    resize_image(download_path, png_path, 'small')
    s3_client.upload_file(png_path, '{}-small'.format(bucket), key )

    resize_image(download_path, png_path, 'large')
    s3_client.upload_file(png_path, '{}-large'.format(bucket), key )

    os.remove(png_path)

