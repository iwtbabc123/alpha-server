#socket fd type
FD_TYPE_ACCEPT		= 1  #accept client socket
FD_TYPE_CLIENT		= 2  #read or write client socket
FD_TYPE_CLOSE		= 3  #close socket
FD_TYPE_TIMER		= 4
FD_TYPE_CONNECT		= 5  #connect to server
FD_TYPE_SERVER		= 6  #read or write server socket
FD_TYPE_SERVER_CLOSE	= 7

#server type
PROCESS_TYPE_CLIENT = 101
PROCESS_TYPE_SERVER = 102

#mongodb operation
FIND_DOC_OP = 1
UPDATE_DOC_OP = 2
INSERT_DOC_OP = 3