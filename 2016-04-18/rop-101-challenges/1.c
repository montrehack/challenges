#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <signal.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>

/* The service you have to exploit */
void service() {
	char data[0x100];

	printf("Enter your data : ");
	gets(data);
}

void secret() {
	FILE* fd = fopen("flag.txt", "rb");
	char data[1024];
	fread(data, 1, 1023, fd);
	printf("%s", data);
}

/* Server forking logic, not part of the actual challenge */
void auto_kill (int sig) {
	raise(SIGKILL);
}

int main() {
	int server_sockfd, client_sockfd;
	int server_len, client_len;
	struct sockaddr_in server_address;
	struct sockaddr_in client_address;

	signal (SIGALRM, auto_kill);

	server_sockfd = socket(AF_INET, SOCK_STREAM, 0);
	server_address.sin_family = AF_INET;
	server_address.sin_addr.s_addr = htonl(INADDR_ANY);
	server_address.sin_port = htons(1235);
	server_len = sizeof(server_address);
	bind(server_sockfd, (struct sockaddr *)&server_address,server_len);

	/* Create a connection queue, ignore child exit details and wait for clients. */
	listen(server_sockfd, 5);
	signal(SIGCHLD, SIG_IGN);

	while(1) {
		printf("server waiting\n");

		/* Accept connection. */
		client_len = sizeof(client_address);
		client_sockfd = accept(server_sockfd,(struct sockaddr *)&client_address, &client_len);

		/* Fork to create a process for this client and perform a test to see
		whether we're the parent or the child. */

		if(fork() == 0) {
			printf("Accepted connection\n");
			alarm(300);
			dup2(client_sockfd, STDOUT_FILENO);
			dup2(client_sockfd, STDERR_FILENO);
			dup2(client_sockfd, STDIN_FILENO);
			setbuf(stdout, NULL);

			service();
			
			close(client_sockfd);
			return;
		} else {
			close(client_sockfd);
		}
	}
}