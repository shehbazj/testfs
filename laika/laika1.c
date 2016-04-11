/*
This file scans through a file system image and checks for integer or string data types. 

- INTEGER TYPES - If the data in a word trails with 00 , and / or contains non-ASCII characters for eg. characters not between 0-9 (ASCII - 30-39), a-z (ASCII - ), A-Z (ASCII - ), then the word is deemed as an Integer value.

- STRING TYPES - If the data is non-word aligned, and continues for more than 2 bytes with characters between A-Z, a-z, 0-9 and few other special characters "\n,\t,' ' etc.", then the buffer is deemed string type.

*/

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<stdbool.h>

void usage(){
	printf("./laika1 <file_image>");
}

int printString(FILE *fimage, int pos){
	size_t start,end;
	int ch;
	start=pos;
	end=pos;
	while((ch =fgetc(fimage)) != '\0'){
		pos++;
		end=pos;
	}
	pos++;
	printf("%zu %zu -> string\n",start,end);
	return pos;
}

int printInt(FILE *fimage, int pos){
	size_t start, end;
	int ch;
	start=pos;
	pos+=4;	// next position
	fseek(fimage, 3, SEEK_CUR);
	end = pos-1;	// round off int
	printf("%zu %zu -> int\n",start,end);
	return pos;
}

// checks if character is ASCII 0-9,A-Z,a-z 
// all possible statements with which a buffer can begin
bool isStringStart(int ch){
	if(ch >= 48 && ch <= 57)	// 0-9
		return true;
	if(ch >= 65 && ch <= 90)	// A-Z
		return true;
	if(ch >= 97 && ch <= 122)
		return true;
	return false;
}

int main(int argc, char *argv[])
{
	FILE *fimage;

	if(argc !=2){
		usage();
		exit(1);
	}
	
	if((fimage = fopen(argv[1], "r+")) == NULL){
		printf("File %s does not exist\n", argv[1]);
		exit(1);
	}

	int ch = fgetc(fimage);
	size_t pos=0;
	while(ch != EOF){
		if(ch == '\0'){
			pos++;
		}else{
			if(pos % 4){
				pos = printString(fimage, pos);
			}else{
				if(!isStringStart(ch)){
					pos = printInt(fimage, pos);
				}else{
					pos = printString(fimage, pos);
				}		
			}	
		}
		ch = fgetc(fimage);			
	}	
	fclose(fimage);		
}
