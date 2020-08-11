import socket
SERVER = "127.0.0.1"
serveradd = 'ec2-34-216-237-202.us-west-2.compute.amazonaws.com'
PORT = 10006
i=1000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serveradd, PORT))
client.sendall(bytes("This is from dummy Client",'UTF-8'))
while True:
  #in_data =  client.recv(1)
  #print("From Server :"+str(in_data))
  i=+1
  print(i)
  client.sendall(bytes(i))
  #out_data = input()
  #if out_data == 'bye':
    #break
client.close()
