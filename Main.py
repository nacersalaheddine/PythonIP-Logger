import os,requests,socket,time
from datetime import date,datetime


what_is_my_ip_address = 'http://bot.whatismyipaddress.com/'
loggs_file_name = 'ip_loggs.log'
log_header = '------------------------------------------------------------------------\n'\
			 'PC Uptime IP Loggs By / Salah eddine Nacer\n'\
		     '------------------------------------------------------------------------\n'\
			 'Current Machine User:{}\n'\
		     '------------------------------------------------------------------------\n'
			

log_data_str = '------------------------------------------------------------------------\n'\
	  '{} / {}\n'\
	  '{} / {}\n'
	  
log_error_str = '----------------------------------ERROR---------------------------------\n'\
	  '{} / {} / {}\n'

today = date.today()
now = datetime.now()
working_directory_path = os.getcwd()
env_username = os.getenv('username')


def get_public_address(api_url):
	return requests.get(api_url, stream=True)
	

def init_logs_file():
	#Check if the loggs file exists then initiate it with the header, else leave it.
	if not(os.path.isfile(loggs_file_name)):
		f = open('{}\\{}'.format(working_directory_path,loggs_file_name),"a+");
		f.write(log_header.format(env_username))
		f.close()
	
def log_data(ip):
	f = open('{}\\{}'.format(working_directory_path,loggs_file_name),"a+");
	if(not(f.closed)):
		f.write(log_data_str.format(today.strftime("%A"),today.strftime("%B %d, %Y"),now.strftime("%H:%M:%S %p"),str(ip)))	
		f.close
	

def log_error():
	f = open('{}\\{}'.format(working_directory_path,loggs_file_name),"a+");
	if(not(f.closed)):
		f.write(log_error_str.format(today.strftime("%A"),now.strftime("%H:%M:%S %p"),today.strftime("%B %d, %Y")))	
		f.close


def internet(host="8.8.8.8", port=53, timeout=3):
  """
  Host: 8.8.8.8 (google-public-dns-a.google.com)
  OpenPort: 53/tcp
  Service: domain (DNS/TCP)
  """
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    return True
  except socket.error as ex:
    print(ex)
    return False

if('__main__' == __name__):

	init_logs_file()

	#Keep checking for internet connection every x seconds
	while(not(internet())):
		time.sleep(30)

	response = get_public_address(what_is_my_ip_address)
	if response.status_code == 200:
		print("The IP is ({})".format(response.text))
		log_data(response.text)
	else:
		print("Error Response is:",response.status_code)
		log_error()
