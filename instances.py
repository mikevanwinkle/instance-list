#!env/bin/python
import argparse, pprint, sys, os
import boto3
import messager as msg
from terminaltables import AsciiTable

# parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("command", help="Commands {list}")
parser.add_argument('--region', help="Set the region to get instances from")
parser.add_argument('--order-by', help="Which field should be used to order results, must be in the list of fields")
parser.add_argument('--fields', help="Specify fields to return in a comma seperated list.")
args = parser.parse_args()
pprint.pprint(args)

region = args.region if args.region is not None else os.environ['AWS_REGION']

ec2 = boto3.client('ec2', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], 
						  aws_secret_access_key=os.environ['AWS_ACCESS_SECRET_KEY'],
						  region_name=region)

msg.info("Checking region {}".format(region))

class Instances():
	def __init__(self):
		""" Initializes variables for use later """
		self.instances = []
		self.fields = ['InstanceId','Owner','InstanceType', 'LaunchTime']
		if args.fields is not None:
			for field in args.fields.split(','): 
				self.fields.append(field)
		self.fields = set(self.fields) # drop duplicates
		self.normalized_instances = []
		self.order_by = args.order_by if args.order_by is not None else 'Owner'

	def main(self):
		""" Invokes the specified command and prints the output """
		result = getattr(self, args.command)()
		self.output()

	def list(self):
		""" List instances """
		response = ec2.describe_instances()
		for resv in response['Reservations']:
			for instance in resv['Instances']: 
				self.instances.append(instance)

	def normalize(self):
		""" Normalize data in preparation for printing """
		data = []
		for instance in self.instances:
			normalized_instance = {}
			for key in self.fields:
				if key in instance.keys():
					normalized_instance[key] = instance[key]
				# also check the tags
				for tag in instance['Tags']:
					if tag['Key'] == key:
						normalized_instance[key] = tag['Value']

				# if the key has not been found, set it to unknowm		
				if key not in normalized_instance.keys(): 
						normalized_instance[key] = 'Unknown'
			self.normalized_instances.append(normalized_instance)

	def order(self):
		""" Order the instances """
		self.normalized_instances = sorted(self.normalized_instances, key=lambda k: k[self.order_by])

	def output(self):
		""" normalize, order and print output """
		self.normalize()
		self.order()
		data = [self.fields]
		for instance in self.normalized_instances:
			row = [instance[key] for key in self.fields] 
			data.append(row)
		table = AsciiTable(data)
		print table.table

if __name__ == '__main__':
  app = Instances()
  app.main()