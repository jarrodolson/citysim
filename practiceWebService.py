import boto

key1 = "AKIAJINOAUFOPSFUJWSQ"
key2 = "TXOXxMuXq/c+h3lRRwoL/2By1SU6A+vpg/UuJy5V"
######aws_access_key_id = {AKIAJINOAUFOPSFUJWSQ}
######aws_secret_access_key = {TXOXxMuXq/c+h3lRRwoL/2By1SU6A+vpg/UuJy5V}
##s3 = boto.connect_s3(key1,key2)
##bucket = s3.create_bucket('message_pump.testing')
####key = bucket.new_key('examples/first_file.csv')
####key.set_contents_from_filename('C:\\Users\\jarrodanderin\\Documents\\2012_Spring\\SOC519\\_WHAT_PRICE\\test.csv')
####key.set_acl('public-read')

import json
import uuid
##sqs = boto.connect_sqs(key1,key2)
##q = sqs.create_queue('my_message_pump')
##data = json.dumps("\"foobar")
##print data
##s3 = boto.connect_s3(key1,key2)
##bucket = s3.get_bucket('message_pump.testing')
##key = bucket.new_key('2010-03-20/%s.json' % str(uuid.uuid4()))
##key.set_contents_from_string(data)
##message = q.new_message(body=json.dumps({'bucket':bucket.name,'key':key.name}))
##q.write(message)

##sqs = boto.connect_sqs("AKIAJINOAUFOPSFUJWSQ","TXOXxMuXq/c+h3lRRwoL/2By1SU6A+vpg/UuJy5V")
##q = sqs.get_queue('my_message_pump')
##message2 = q.read()
##print message2
##if message2 is not None:
##    msg_data = json.loads(message.get_body())
##    key = boto.connect_s3(key1,key2).get_bucket(msg_data['bucket']).get_key(msg_data['key'])
##    data = json.loads(key.get_contents_as_string())
##    print data
##    q.delete_message(message2)

import time
##ec2 = boto.connect_ec2(key1,key2)
####key_pair = ec2.create_key_pair('ec2-sample-key')
##reservation = ec2.run_instances(image_id='ami-bb709dd2', key_name="ec2-sample-key")
##time.sleep(120)
##for r in ec2.get_all_instances():
##    if r.id == reservation.id:
##        break
##print r.instances[0].public_dns_name

conn = boto.connect_ec2(key1,key2)
print "Connection made"
##images = conn.get_all_images()
##print images
image = "Image:ami-bb
##reservation = conn.run_instances(image_id='ami-bb709dd2',key_name="ec2-sample-key")
print reservation.instances
instance = reservation.instances[0]
while instance.state!="running":
    instance.update()
    print instance.state
    time.sleep(60)
print instance.dns_name
instance.stop()
while instance.state!="terminated":
    instance.update()
    print instance.state
    time.sleep(60)
print instance.state
