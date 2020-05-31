#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

struct command {
	long long priority;
	char command[0x180];
};

char name[16];
char filename[60];

void banner() {
	puts("Welcome to the command system");
	puts("=============================");
}

int get_integer() {
	char digits[16];
	memset(digits, 0, 16);

	fgets(digits, 16, stdin);
	return atoll(digits);
}

int get_long_long() {
	char digits[16];
	memset(digits, 0, 16);

	fgets(digits, 16, stdin);
	return atoll(digits);
}

void config() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	if (!getenv("DEBUG")) {
		alarm(60);
	}
}

void options() {
	puts("");
	puts("Choose an option:");
	puts("1. Include command");
	puts("2. Review command");
	puts("3. Delete command");
	puts("4. List commands");
	puts("5. Send commands");
	printf("> ");
}

void error() {
	puts("[ERROR] Unexpected option!!!");
	puts("The system is shutting down");
	exit(1);
}

void add(struct command *commands[]) {
	for (int idx = 0; idx < 10; ++idx) {
		if (!commands[idx]) {
			commands[idx] = malloc(sizeof(struct command));

			printf("Priority: ");
			commands[idx]->priority = get_long_long();
			printf("Command: ");
			size_t len = read(0, commands[idx]->command, 0x170);

			if (len > 0 && commands[idx]->command[len-1] == '\n') commands[idx]->command[len-1] = 0;

			printf("The command has been included at index %d\n", idx);

			return;
		}
	}

	puts("[INFO] The authorized limit has been reached!");
}

void print_command(struct command *comm) {
	printf("Priority: %lld\n", comm->priority);
	printf("Command: %s\n", comm->command);
}

void review(struct command *commands[]) {
	int idx = -1;

	printf("Command index: ");
	idx = get_integer();

	if (idx >= 0 && idx < 10 && commands[idx]) {
		puts("");
		print_command(commands[idx]);
	}
}

void delete(struct command *commands[]) {
	int idx = 0;

	printf("Command index: ");
	idx = get_integer();

	if (idx >= 0 && idx < 10 && commands[idx]) {
		free(commands[idx]);
		commands[idx] = NULL;
		puts("The command has been successfully deleted");
	}
}

void list(struct command *commands[]) {
	for (int idx = 0; idx < 10; ++idx) {
		if (commands[idx]) {
			puts("");
			printf("Index %d\n", idx);
			print_command(commands[idx]);
		}
	}
}

void get_commands(struct command *commands[]) {
	int choice;

	while (1) {
		options();
		choice = get_integer();

		switch(choice) {
			case 1:
				add(commands);
				break;
			case 2:
				review(commands);
				break;
			case 3:
				delete(commands);
				break;
			case 4:
				list(commands);
				break;
			case 5:
				return;
			default:
				error();
		}
	}
}

void send_commands(struct command *commands[], FILE **fp_pointer) {
	char greeting[20];
	char current[16];
	long long rbs_id;

	memset(greeting, 0, 20);
	memset(current, 0, 16);

	puts("Are you sending the commands to which rbs?");
	rbs_id = get_long_long();
	fprintf(*fp_pointer, "Id: %lld\n", rbs_id);

	for (int idx = 0; idx < 10; idx++) {
		if (commands[idx]) {
			fprintf(*fp_pointer, "%lld:%s\n", commands[idx]->priority, commands[idx]->command);
		}
	}

	snprintf(current, 12, name);
	strcpy(greeting, "Mr. ");
	strcat(greeting, current);

	printf("You command %s!\n", greeting);
}

int main () {
	struct command *commands[10];

	config();
	banner();

	printf("Your name: ");
	size_t len = read(0, name, 12);

	if (len > 0 && name[len-1] == '\n') name[len-1] = 0;

	printf("Welcome %s\n", name);

	memset(commands, 0, 10*8);

	get_commands(commands);

	puts("");
	puts("Sending commands...");

	snprintf(filename, 45, "/commands/%ld", time(NULL));
	FILE *fp = fopen(filename, "w");

	if (fp == NULL) {
		printf("[ERROR] An error happened while opening the file");

	       // Program exits if the file pointer returns NULL.
	       exit(2);
	}

	send_commands(commands, &fp);
	
	fclose(fp);

	return 0;
}
