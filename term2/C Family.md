C language

/home/jojo/Documents/UNI/term2/images/

-  imperative 
  -  describes: computation in statements that change a program state
  - declarative: describe computation in terms of what it should accomplish (e.g. SQL)
- procedural/functional
- compiled 
- statically , weakly types
  -  statically typed : types are checked before runtime
  - weakly typed : supports implicit type conversions
- portable since its available on every platform
- very fast since very low level
- has explicit memory management
- ANSI/ISO standards

but does *not* have

- runtime error checking , e.g. bounds initial values, etc 
- exception handling 

~~~c
/* "/*" for sample commnet */
#include<stdio.h> /* compiler directive , include files*/

int main() /* main function*/
{ /* start block/scope */
	printf("Hello world!\n"); /*output some text*/
	return 0; /*finish with success*/
} /* end block/scope */
~~~

### Compiling and linking

~~~c
edit
/*source code*/    
myProgram.c 
myProgram.h
    
compile
/*object code*/
myProgram.o (or my Program.obj)
    
link /*executable*/
    Program.exe   
~~~



<u>GNU</u>

GNU: free , UNIX - compatible operating system

GNU system  contain all of the official GNU software packages including 

gcc: the GNU Compiler Collection



### Pointers

- memory addressing
- pointer arithmetic 
- arrays as pointers
- dynamic memory allocation
- valgrind - can help you test memory allocation effectively

pointers are just numbers , that you can perform arithmetic on them.

arrays are equivalent to pointers 

Another base datatype: **pointer**



~~~c
char ch = 'A'; /*variable ch is a character*/
char *p; /* variable p is a pointer to a character */
p = &ch  /* P is a pointer to ch *?

Variable p contains the addresses of where ch is stored in memory
~~~



#### & and *

- if **x** is any data type , then

  **&x** is the location in memory "its address" where x is currently stored

- if **x** is a pointer ,then

  ~~~c
  <datatype> *x;
  ~~~

  declares x to contain the memory address of a variable of type <datatype>

  ***x** says : go to memory address stored in x and bring back the value (of type) stored there

  declare empty memory address space of x
  
  ![image-20220131113425515](/home/jojo/Documents/UNI/term2/images/image-20220131113425515.png)
  
  declare x to memory address of &c[1];
  
  ![image-20220131113652678](/home/jojo/Documents/UNI/term2/images/image-20220131113652678.png)
  
  x* memory address is that of c[1] which is 0x8105
  
  ![image-20220131114144580](/home/jojo/Documents/UNI/term2/images/image-20220131114144580.png)
  
  ~~~c
  char c = 'A'
  char *p = &c;
  printf("c is %c\n",c); /*the value of c*/
  printf("c is %p\n", &c); /*the memory addres of c*/
  printf("p is %c\n",*p); /*the thing pointed to by p (i.e. value of c)*/
  printf("p is %p\n",p);  /*value of p*/
  
  *p = 'B';
  printf("c is %c\n",c);
  c is B
  ~~~
  
  ![image-20220131110906182](/home/jojo/Documents/UNI/term2/images/image-20220131110906182.png)



#### size of a pointer

  The amount of memory used to store a pointer depends on the operating system , compiler setup , etc. Normally :

- 32 bit OS = 4 bytes 
- 64 bit OS = 8 bytes

  

  a pointer has 4 bytes.

#### Pointer arithmetic 

A memory address is just an integer , so we can perform arithmetic on it....

x++; short int *x and short int is 2 bytes ,  Note , the pointer doesn't just add 2 bytes but adds as much to go to the next relevant contiguous information.

![image-20220131114635951](/home/jojo/Documents/UNI/term2/images/image-20220131114635951.png)

  adds 2 points to the current pointed address

####   Arrays (and strings): pointer equivalence

~~~c
char str[20] = "Hello world!";
char *p = str;

printf("str is %s\n", str);   /*str is Hello world!*/
printf("p is %s\n",p);		 /* p is Hello world! */

p+=4;
printf("str is %s\n, str");    /* str is Hellx world!*/

*p = '\0';
printf("str is %s\n,str"); /*Stop here and try these two lines.*/
~~~

#### Void pointers can point to any datatype

~~~c
char c = 'A';
float n = 10.0;	p can point to anything...
void *p;		/* p can point to anything */

p = &c;
printf("p points to %c\n,*(char *)p"); 	/*needs a cast when used*/

p =&n;
printf("p points to %f\n", *(float *)p);
~~~



### Runtime errors using pointers

- Memory fault
- Segmentation fault

##### Caused by

- trying to access memory to which it is not allowed access
- trying to access memory in a way that is not allowed.

e.g. trying to overwrite the operating system

You might not get an error, you might just corrupt your own program

~~~c
char str1[20] = "Goodbye";
char str2[6] = "Hello";
str2[16] = 'x';
printf("str1: %s\n", str1);
printf("str2: %s\n", str2);

~~~

##### Runtime errors using pointers

~~~ c
char str1[20] = "Goodbye";
char str2[6] = "Hello";
str2[16] = 'x';
printf("str1: %s\n, str1");
printf("str2: %s\n, str2");
~~~

str2[16] goes over str2 string and overwrites str1[0] to x

![image-20220131122235521](/home/jojo/Documents/UNI/term2/images/image-20220131122235521.png)

### Dynamic memory allocation

Sometimes you do not know at compile time how much memory you will need at runtime. Possible solutions:

1. Declare an array whose size is decided at runtime.

~~~c
#include <string.h>
#include <limits.h>
int main ()
{
unsigned int n = UINT_MAX;
char ch[n];
strcpy(ch,"Elephant");
return 0;
}
~~~

Memory fault ( core dump ) might occur , because there might not be enough free , contiguous memory to allocate to the array.

Sometimes you do not know at compile time how much memory you will need at runtime. Possible solutions.

1. Declare an array whose size is decided at runtime. But there is no way of knowing how much free contiguous memory is available. And you might not know how much is required before declaring the array.
2. . Process the data in smaller chunks. Possible, but this requires a lot of extra programming.
3. Dynamically allocate memory at runtime using pointers. Here we can check whether memory allocation was successful.

Memory can be allocated to a variable at runtime:

~~~c
#include<stdlib.h>
int *p = Null;
p = (int *)malloc(23);  /*23 bytes*/
p = (int *)malloc(23*sizeof(int)); /*23 integers*/
/*return datatype for malloc is void hence the cast*/

int *p = NULL;
/*allocates 8 bytes (for a 64-bit system) to p*/

p = (int *)malloc(23);
finds 23 free bytes in memory, reserves it for p, and then sets p to the memory address of the first
of those bytes
~~~

There might not be enough memory:

~~~c
p = (int *)malloc(100000000000000*sizeof(int)); not enough memory
printf("p = %p\n", p);
/*p = (nil)*/

/*always trap the fact that memory was not allocated:*/
if ( !( p = (int *)malloc(100000000000000*sizeof(int)) ) )
{
printf("Out of memory\n");
exit(1);
}   

~~~

### Variable and scope

" Normal variables":

~~~c
void myFunction()
{
 	int p = 1000;
}
/* p goes out of scope at the end of the function
and its allocated memory is released*/
~~~

Dynamically allocated variables:

~~~c
void myFunction ()
{
int *p = (int *)malloc(1000000);
}
/* Memory leak
allocated memory is NOT released, even though p goes out of scope.*/
/*The 8 bytes (on a 64-bit system) occupied by p are released, but the 1000000
bytes reserved for p, and to which p points, are not.*/
~~~

### Free your memory

Whenever using malloc , always make sure to explicitly free the memory before the variable goes out of scope:

~~~c
void myFunction() {
	int *p = (int *)malloc(1000000);
	free(p);
}
~~~

- Freeing memory that has already been freed, or memory not allocated by malloc (e.g. “char str[20];”): “behaviour is undefined".

### Function parameters and more pointers

- Function parameters and pointers 
  -  pass by value
  - pass by reference
  - pointers to pointers
- Passing values into the main function at runtime
  -  argc and argv
- Function pointers
  -  example: qsort();

#### Function: pass by value

~~~c
#include<stdio.h>
void myFunctionA (char);

int main() 
{
    char c = 'A';
    printf("Before: c = %c\n",c);
    myFunctionA(c);
    printf("After: c =%c\n",c);
}

void myFunctionA (char ch) 
{ ch = 'B';}
/* Before: c = A
    After: c = A
The value of c is not updated because ch is a copy of c./*    
~~~

#### Functions: pass by reference

~~~c
#include <stdio.h>
void myFunctionA (char *);
int main ()              /* In order to update the value of a*/
{					   /* parameter within a function it must */
char c = 'A';			/* by passed as a pointer*/
printf("Before: c = %c\n",c);
myFunctionA(&c);
printf(" After: c = %c\n",c); /* The value of the thing passed*/
}`							/*cannot be changed*/
void myFunctionA (char *ch)
{ *ch = 'B'; } /*Here the memory address where c is stored is copied (and is not updated) , not c's value*/

/* 
Before: c = A
 After: c = B
/* 
~~~

###### attempt 1

~~~c
#include <stdio.h>
void myFunctionB (char *);
int main ()
{
char *p = NULL;
myFunctionB(p);
printf("p = %s\n",p);
}
void myFunctionB (char *str)
{
strcpy(str,"Hello");
}
/* memory fault(coredump)*/
~~~

![image-20220201092223962](/home/jojo/Documents/UNI/term2/images/image-20220201092223962.png)

![image-20220201092236670](/home/jojo/Documents/UNI/term2/images/image-20220201092236670.png)

###### attempt 2

~~~c
#include <stdio.h>
void myFunctionB (char *);
int main ()
{
char *p = NULL;
myFunctionB(p);
printf("p = %p: %s\n",p,p);
}
void myFunctionB (char *str)
{
if ( !(str = (char *)malloc(6)) )
{
printf("Insufficient memory\n");
exit(-1);
}
strcpy(str,"Hello");
printf("str = %p: %s\n",str,str);
}
~~~

str copies the random code in p  and , malloc reservers free memory

![image-20220201092531558](/home/jojo/Documents/UNI/term2/images/image-20220201092531558.png)

![image-20220201092542140](/home/jojo/Documents/UNI/term2/images/image-20220201092542140.png)



![image-20220201092556288](/home/jojo/Documents/UNI/term2/images/image-20220201092556288.png)

###### attempt 3

~~~c
#include <stdio.h>
void setString (char **);
int main ()
{
char *p = NULL;
setString(&p);
printf("p = %p: %s\n",p,p);
}
void setString (char **str)
{
if ( !(*str = (char *)malloc(6)) )
{
printf("Insufficient memory\n");
exit(-1);
}
strcpy(*str,"Hello");
printf("*str = %p: %s\n",*str,*str);
}
~~~

str points to the memory address of p / doesn't copy p , the pointer of str then is assigned hello which updates both p and str.

![image-20220201095449491](/home/jojo/Documents/UNI/term2/images/image-20220201095449491.png)

#### Pointers to pointers 

A pointer is just another datatype , so you can have a pointer to a pointer

~~~c
char ch = 'A';
char *p = &ch;
char **q = &p;
printf("The value of ch is: %c, %c,%c\n",ch,*p,**q);
/*The value of ch is: A,A,A*/
printf("The memory address of ch is: %p,%p,%p \n",&ch,p*q);
/*The memory address of ch is: 0x7ffe44c2ed4f, 0x7ffe44c2ed4f, 0x7ffe44c2ed4f*/
~~~

#### Function parameters

- Parameters to functions are always passed by value.
- To update the value of a parameter and pass the new value back to the calling function you must use pointers.
  - his gets around the fact that functions in C can only return one value

#### Passing arguments to the main function

~~~c
int main (int argc,char **argv)
~~~

example

~~~c
int main ( int argc, char **argv )
{
int i;
for (i=0; i<argc; i++)
printf("Parameter %d: %s\n", i, argv[i]);
}
~~~

#### Function pointers

~~~c
int Plus (int a, int b) { return a+b; }
int Minus (int a, int b) { return a-b; }
int Multiply (int a, int b) { return a*b; }
int Divide (int a, int b) { return a/b; }
int doFunction (int a, int b, int (*myFunc)(int,int) )
{ return myFunc(a, b); }

/*
printf("1+3 = %d\n", doFunction(1,3,&Plus));
printf("1*3 = %d\n", doFunction(1,3,&Multiply));
*/
~~~



#### Summary

• Function parameters and pointers
• pass by value
• pass by reference
• pointers to pointers
• Passing values into the main function at runtime
• argc and argv
• Function pointers
• example: qsort()

### Structures

**Structures are**

- a type of variable that groups multiple related data items together
- the closest thing C has to a class

Declared like this:

~~~c
struct <structure name>
{
<variable definition>;
<variable definition>;
};
~~~

Struct : examples 

~~~c
struct bookStruct
{
char title[181] = "";
char author[51] = "";
float price;
int numPages;
};
int main ()
{
struct bookStruct myBook;
struct bookStruct anotherBook;
myBook.price = 12.99;
strcpy(myBook.title,"The Joy of Programming in C");
anotherBook = myBook;
return 0;
}
~~~

#### typedef

You can define your own datatypes using the typedef command:

~~~c
typedef struct bookStruct BOOK;
~~~

and can then use this as  a datatype in variable declaration:

~~~c
BOOK myBook;
~~~

which is exactly the same as 

~~~c
struct bookStruct myBook;
~~~

Like any other datatype, a function can accept a structure as a parameter:

~~~c
int getPageCount ( struct bookStruct newBook )
{ return newBook.numPages; }
~~~

or return one;

~~~c
struct bookStruct makeBook (...)
{...}
~~~

or, using the new datatype:

~~~c
BOOK makeBook ( BOOK myBook )
{...}
~~~

and you can have arrays of them:

~~~c
BOOK books[20];
~~~

~~~c
BOOK firstBook; /* not a pointer */
strcpy(firstBook.title, "Hidden Figures");
strcpy(firstBook.author, "Margot Lee Shetterly");
firstBook.price = 8.99;
firstBook.numPages = 384;
~~~

~~~c
BOOK *secondBook; /* a pointer */
if ( ( secondBook = (BOOK *)malloc(sizeof(BOOK)) ) == NULL )
{ /* error: not enough memory */ }
strcpy(secondBook->title, "Hidden Figures");
strcpy(secondBook->author, "Margot Lee Shetterly");
secondBook->price = 8.99;
secondBook->numPages = 384;
~~~

### Linked lists

what is a linked list?

- a data structure
- an ordered sequence of nodes
  -  data , and
  - one or more links to other nodes to record the sequence
- a memory - efficient means of storing large data structures , or where the final size of the large data structure is unknown at compile time
- a speed efficient means of inserting and deleting nodes.

#### Array insert: case 1 

To insert into an ordered array, everything must be shuffled along:

~~~c
char array[5]
~~~

![image-20220201101654998](/home/jojo/Documents/UNI/term2/images/image-20220201101654998.png)

To insert into an ordered array, everything must be shuffled along:

![image-20220201101922863](/home/jojo/Documents/UNI/term2/images/image-20220201101922863.png)

![image-20220201101937442](/home/jojo/Documents/UNI/term2/images/image-20220201101937442.png)

![image-20220201101951511](/home/jojo/Documents/UNI/term2/images/image-20220201101951511.png)

#### Array insert: case 2

If the array is already full, then it has to be expanded first:

![image-20220201102057219](/home/jojo/Documents/UNI/term2/images/image-20220201102057219.png)

![image-20220201102119671](/home/jojo/Documents/UNI/term2/images/image-20220201102119671.png)

![image-20220201102206615](/home/jojo/Documents/UNI/term2/images/image-20220201102206615.png)

### Array list

Remember that arrays are always stored in contiguous memory.

**Advantage** of arrays:

- can go directly to the nth element

**Disadvantages** of arrays:

- insert/delete requires other elements to be moved
- what happens when you want to insert a new element into a full array?
  -  either you stop
  - or will have to extend the array , (often require the whole array to be moved.)

### Dynamic linked lists

Define the structure of one node in the list:

~~~c
struct anode
{
/* some data variables here, e.g.: */
char data;
struct anode *nextNode;
};
typedef struct anode NODE;
~~~

Initialise an empty list:

~~~c
NODE *root = NULL;
~~~

Add the first node to the list

First allocate enough memory:

~~~c
Node *newNode;
if ((newNode = (NODE *)malloc(sizeof(NODE))) == NULL)
{...}
~~~

Then set the new node's values:

~~~c
newNode-> data = 'A';
ndeNode -> nextNode = Null;
~~~

Then add it to the empty list:

~~~c
root = newNode;
~~~

Add a second new node to this list:

![image-20220201102932950](/home/jojo/Documents/UNI/term2/images/image-20220201102932950.png)

#### Dynamic linked lists Advantages and Disadvantages

- Advantages
  -  it does not matter where in memory each node is stored 
  - insert/delete requires only changing the values of 1 or 2 pointers
  - size of linked list is limited only by computer memory
  - one list may be linked in more than one way
- Disadvantage of linked lists:
  -  to find an element, must start from the beginning and follow the pointers 
    -  can add extra pointers to speed this up.

#### Linked list: insert

![image-20220201103044827](/home/jojo/Documents/UNI/term2/images/image-20220201103044827.png)

![image-20220201103058725](/home/jojo/Documents/UNI/term2/images/image-20220201103058725.png)

![image-20220201103110316](/home/jojo/Documents/UNI/term2/images/image-20220201103110316.png)

**Note:** The individual nodes do node need to be in contiguous memory

##### The wrong way

![image-20220201103548953](/home/jojo/Documents/UNI/term2/images/image-20220201103548953.png)

![image-20220201103600432](/home/jojo/Documents/UNI/term2/images/image-20220201103600432.png)

![image-20220201103611517](/home/jojo/Documents/UNI/term2/images/image-20220201103611517.png)

##### insertion cases

There are four cases for inserting a new node:

- add the first node to a new list
- append a node to the end of the list
- insert a node at the beginning of the list
- insert a node into the middle of the list

##### deletion cases

There are four cases for deleting a node from the list:
- delete a node from the middle of the list
- delete the node at the beginning of the list
- delete the node at the end of the list
- delete the last node in the list

### Doubly - linked list

~~~c
struct anode 
{
char monarchName[51];
short int startYear;
struct anode *nextName = Null;
struct anode *nextYear = Null;
}
~~~

![image-20220201103946412](/home/jojo/Documents/UNI/term2/images/image-20220201103946412.png)

### Type of linked lists

Common types of dynamically linked data structures are:

- stacks

- queues 

- circular lists

- trees

### Stacks : LIFO queues

![image-20220201104108685](/home/jojo/Documents/UNI/term2/images/image-20220201104108685.png)

### Queues

![image-20220201104244046](/home/jojo/Documents/UNI/term2/images/image-20220201104244046.png)

![image-20220201104252548](/home/jojo/Documents/UNI/term2/images/image-20220201104252548.png)

![image-20220201104259442](/home/jojo/Documents/UNI/term2/images/image-20220201104259442.png)

![image-20220201104305671](/home/jojo/Documents/UNI/term2/images/image-20220201104305671.png)

![image-20220201104316587](/home/jojo/Documents/UNI/term2/images/image-20220201104316587.png)

### Linux commands

At the Linux command prompt ($) enter the following command:

~~~
$ ls –al ~/
~~~


and you will see a list of files in your home directory (~/), including this one:

~~~
.bash_history
~~~

You can look at the 10 most recent commands you have entered, like this:

~~~
$ history 10
~~~

and you can re-execute the most recent command starting with “cd”, like this:

~~~
$ !cd
~~~

- grep
  -   find text in files using regular expressions
- find 
  -  find files in a directory structure based on different characteristics

### grep

At the Linux command prompt ($) enter the following command in the directory
containing your C programs:

~~~c
$ grep main *.c
~~~

and you will see a list that might look a bit like this 

~~~
checkPointerSize.c:int main ()
helloWorld.c:int main ()
~~~

There are lots of different options you can specify, eg

~~~
$ grep –n main *.c
~~~

shows you which lines the found text is on,

~~~
$ grep –l main *.c
~~~

lists only the file names that containing matching text,

~~~
$ grep –L main *.c
~~~

lists only the file names that do not contain matching text etc.

### find

At the Linux command prompt ($) enter the following command:

~~~
$ find ./ -type f -size +10000k
~~~

This finds all files (-type f) in this directory (./) and all its subdirectories that are bigger than 10000k (-size +10000k).

~~~
$ find ./ -type f -size +10000k -exec ls -lh {} \;
~~~

Finds all those same files and for each one (-exec) lists their full details (ls –lh).

~~~
$ find ./ -type f -size +10000k -name "*.mat"
~~~

Finds all big Matlab .mat files (-name “*.mat”). etc.

#### find and grep together

Find all C program files in the current directory and its subdirectories, and then just select those that have the word “fork” in the name:

~~~
$ find ./ -name "*.c" | grep fork
~~~

which is really just the same as:

~~~
$ find ./ -name "*fork*.c"
~~~

but this one:

~~~
$ find ./ -name "*.c" | xargs -1 grep fork
~~~

finds all C programs which include the word “fork” in the program code.

Check out the xargs command for more details

### File input streams

~~~c
scanf() /* is like the reverse of printf()*/;
int main ()
{
int anInteger;
	printf("Please enter an integer: ");
	if ( scanf("%d", &anInteger) != 1 ) /* returns the number of data items successfully assigned to a value*/
		{
		/* some error processing */
			return EXIT_FAILURE;
		}
	return EXIT_SUCCESS;
}
~~~



#### Console input : control string

![image-20220207130744432](/home/jojo/Documents/UNI/term2/images/image-20220207130744432.png)

Non - white space in the format string

- causes scanf to read , but not store, matching character
- must be entered by the user
- use %% to read a percent sign

~~~c
char yourName[11];
float yourHeight = 0.0;
printf("Please enter your name and height: ");
if ( scanf("%s and %f", yourName, &yourHeight) == 2 )
printf("%s: height %f metres\n", yourName , yourHeight );
else
printf("you entered the wrong thing");
~~~

~~~
Please enter your name and height : Jacq 1.8
you entered the wrong thing
Please enter your name and height : Jacq and 1.8
Jacq: height 1.800000 metres
~~~

Console input: format specifier

~~~c
char yourName[11];
float yourHeight = 0.0;
printf("Please enter your name and height: ");
if ( scanf("%10s and %f", yourName, &yourHeight) == 2 )
printf("%s: height %f metres\n", yourName , yourHeight );
else
printf("you entered the wrong thing");
~~~

~~~
Please enter your name and height : Jacq and 1.8
Jacq: height 1.800000 metres
Please enter your name and height : ABCDEFGHIJJacq and 1.8
you entered the wrong thing
~~~

![image-20220207131430813](/home/jojo/Documents/UNI/term2/images/image-20220207131430813.png)

~~~c
scanf("%d%*c%d",&x,&y)
/*discards any number of any characters between two integers (e.g. "43hello65").*/
~~~

![image-20220207132220349](/home/jojo/Documents/UNI/term2/images/image-20220207132220349.png)

White space in the format string
• causes scanf to read, but not store, a matching character
• is as defined by the isspace() function, e.g. space, tab, newline

### Program output

- **A stream**

  -  is an abstraction of a **file**
    - provides a consistent interface to the programmer, regardless of the actual device

-  is **buffered**

  - data is not necessarily written to the device when the write command is issued
  - you can force the write to happen by flushing a stream

-  may be text or binary

  - text stream = sequence of characters
    character translation may occur, e.g. newline → carriage-return + line-feed
  - binary stream = sequence of bytes
    no character translation occurs

- •need to 

  ~~~c
  #include stdio.h
  ~~~

  ![image-20220207132616398](/home/jojo/Documents/UNI/term2/images/image-20220207132616398.png)

### Using a stream 

~~~c
#include <stdio.h>
#include <stdlib.h>
int main ()
{
FILE *fp;
fp = fopen("myTextFile.lis", "r");
if ( fp == NULL )
{
	printf("Cannot open file for read access\n");
	exit(1); /* return a specific error value to the operating system */
}
/* do some file processing */
fclose(fp);
return EXIT_SUCCESS;
}
~~~

Note : Always test that opening the file was successful:

~~~c
fp = fopen("myTextFile.lis", "r");
if ( fp == NULL )
{
/* do some error processing */
}
~~~

usually compressed into

~~~c
if ( (fp = fopen("myTextFile.lis", "r")) == NULL )
{
/* do some error processing */
}
~~~

![image-20220207140850963](/home/jojo/Documents/UNI/term2/images/image-20220207140850963.png)

### Trapping errors :part 1

~~~c
errno.h defines int errno	
~~~

- value is updated when an error occurs
- you can reset the value

~~~
“The initial value of errno at program startup is zero. Many library functions are
guaranteed to set it to certain nonzero values when they encounter certain kinds
of errors. These error conditions are listed for each function. These functions do
not change errno when they succeed; thus, the value of errno after a
successful call is not necessarily zero, and you should not use errno to
determine whether a call failed. The proper way to do that is documented for
each function. If the call failed, you can examine errno.”
~~~

### Trapping errors : part 2

A call to **ferror(fp)**

- determines whether the most recent operation on the file pointed to by fp produced an error
- returns 1 if an error occurred; 0 if not
- value is reset by each file operation

### Write to a stream

- ~~~c
  - fputc(ch,fp);
    /*- outputs the character in ch to the file pointed to by fp
    */
  
  -  fputs(str,fp);
    /*-  outputs the string in str to the file pointed to by fp
    - the null terminator is not output*/
  
  - fprintf(fp, "Character %c, integer %03d", ch, i);
    /*-  like printf, but the string is output to the file pointed to by fp*/
  ~~~

### Read from a stream 

~~~c
• char ch = fgetc(fp);
	/*• reads a single character from the file pointed to by fp and stores it in ch*/
• fgets(str,count,fp);
/*• reads multiple characters up to and including the next newline character (or a
maximum of count characters) from the file pointed to by fp and stores it in the
string str
• adds a null terminator to str
• cannot distinguish between null character read in and the terminating null 
character */
• fscanf(fp,"%d,%d",&x,&y);
/*like scanf, but the string is input from the file pointed to by fp*/
~~~

### Other common stream functions

~~~c
• fflush(fp);
	/*forces the output buffer to be written to the file*/
• remove("myFile.txt");
	/*deletes the specified file
	returns 0 on success; other integer on failure*/
• rewind(fp);
	/*resets the file position indicator back to the beginning of the file*/
~~~

### (Related string functions)

Just like fprintf and fscanf , we have the following related string functions:

- ~~~c
  • sprintf(str, "Character %c, integer %03d", ch, i);
  /*like fprintf, but the output string is stored in the variable str*/
  • sscanf(str,"%d,%d",&x,&y);
  /* • like fscanf, but the string is input from the variable str
  */
  
  You must:
  #include<string.h>
  for sprint() : allocate sufficient memory to str before you call the function
  ~~~

### Standard streams

There are three standard streams that all programs can use **without** calling **fopen** or **fclose**:

- **stdin** input from the keyboard
- **stdout**  output to the terminal ;  normal program output
- **stderr** output to the terminal ; error and warning messages 

unless redirected

**scanf** reads input from **stdin**; equivalent to **fscanf(stdin,...)**
**printf** sends output to **stdout**; equivalent to fprintf(stdout,...)

### Example file read program

~~~~c
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
int main ()
{
	FILE *fp;
	char ch;
if ( (fp = fopen("myFile.txt", "r")) == NULL )
{
	printf("Unable to open file for read access.\n");
	fprintf(stderr, "error %d: %s\n", errno, strerror(errno));
	exit(1);
}
while ( !feof(fp) )
{
	ch = fgetc(fp);
	printf("%3d: %c\n",ch,ch);
}
fclose(fp);
return EXIT_SUCCESS;
}
~~~~

**Note** : always send error messages to stderr and not stdout

## Compiler directives

• giving your programs access to useful library functions and values
• controlling what code gets compiled
• defining macros to make your code more readable
• defining macros for values that might change some time in the future

Actions taken by the compiler before compilation

![image-20220207145343347](/home/jojo/Documents/UNI/term2/images/image-20220207145343347.png)

### #include: <> vs ""

~~~c
#include <stdio.h>
#include "myFile.h"
~~~

<stdio.h>: search for this file using the path in which the pre-processor expects to find such files

"myFile.h": search for this file firstly in the same directory as this program, and then using the path in
which the pre-processor expects to find such files



### #define

~~~c
#define TRUE 1 
#define FALSE 0
#define ELEPHANT "Size of an elephant!"
~~~

Define a macro and replace any instances of the macro name with its definition

~~~c
printf(ELEPHANT);
printf("This is %d\n", TRUE)
~~~

turns  into

~~~c
printf("Size of an elephant!");
printf("This is %d\n", 1);
~~~

#define can be used to create macros, but care needs to be taken:
1. Definitions are substituted before the compiler compiles the source code, so
an error introduced is hard to trace.
2. The direct substitution can lead to unexpected results.

### #define :unexpected results

Consider the following definition:

~~~
#define MAX(a,b) a>b?a:b
~~~

and this piece of code:

~~~
int i = MAX(2,3)+5;
int j = MAX(3,2)+5;
~~~

The compiler substitution leads to this:

~~~
int i = 2>3?2:3+5;
int j = 3>2?3:2+5; 
~~~

#define unexpected results

Consider the following definition:

~~~
#define MAX(a,b) a>b?a:b
~~~

and this piece of code:

~~~
int i = MAX(2,3)+5;
int j = MAX(3,2)+5;
~~~

The compiler substitution leads to this:

~~~c
int i = 2>3?2:3+5;
int j = 3>2?3:2+5;
~~~

Brackets are often the answer:

~~~c
#define MAX(a,b) ((a)>(b)?(a):(b))
~~~

and this code:

~~~c
int i = MAX(2,3)+5;
int j = MAX(3,2)+5;
~~~

becomes

~~~c
int i = ((2)>(3)?(2):(3))+5;
int j = ((3)>(2)?(3):(2))+5;
~~~

resulting in i=8 and j=8. Great! This will even work with something like

~~~c
int i = MAX(x+y,z)+5;
int j = MAX(3.98-2,6.234)+5;
~~~

As before:

~~~c
#define MAX(a,b) ((a)>(b)?(a):(b)) 
~~~

What about this:

~~~c
int i = 2;
int j = 3;
int k = MAX(i++,j++);
~~~

The outcome however becomes  k =4 , i = 3 and j = 5

### Selective compilation

~~~c
#ifdef if a macro is defined

#ifndef if a macro is not defined

#undef undefine a macro

#else otherwise

#elif else if

#endif end of the #ifdef or #ifndef block
~~~

~~~c
#ifndef __UNIX__
/* some C code in here for UNIX systems*/
~~~

~~~c
#else
/* some different C code in here for non-UNIX systems */
~~~

~~~
#endif
~~~

### Useful predefined macros

~~~c
__FILE__ the current file name
__LINE__ the current line number in this file
__DATE__ the date this object code was generated from the source
__TIME__ the time this object code was generated from the source
__STDC__ 1 if this implementation of C conforms to the ANSI/ISO standard; any
other value means it does not
~~~

~~~c
#include <stdio.h>
int main ()
{
printf("Compile date is %s, time is %s\n",__DATE__,__TIME__);
printf("Error in line %d of program %s\n",__LINE__,__FILE__);
return 0;
}
/* Compile date is *current date*, time is *current time*
Error in line 5 of program macros.c"
~~~

### Macro names

- Informal rule : macro name is all capitals

  - C has many informal rules ; this makes your code easier to follow

- System macros start with two underscores

  - so that they do not interfere with your own macros, and so that you can recognise them

  ~~~c
  #include <stdio.h>
  #define STARTMAIN int main () {
  #define ENDMAIN return 0; }
  STARTMAIN
  	printf("Hello World!\n");
  ENDMAIN
  ~~~

### ANSI C Boolean

ANSI C has no Boolean datatype , but we can make one:

~~~c
#define TRUE 1
#define FALSE 0
typedef char BOOLEAN;

int main() {
	BOOLEAN x = TRUE;
	if ( x ) { ... }	
}
~~~

### File pointers

When using a file , you declare a file pointer like this:

~~~c
File *fp
~~~

### Summary

• giving your programs access to useful library functions and values
• controlling what code gets compiled
• defining macros to make your code more readable
• defining macros for values that might change some time in the future

## C Family program structure

- separate code modules 
- compiling and linking
- storage classes
- libraries
- maths example

### C program structure

We want to be able to

- make code more reliable and easier to read
- reuse code
- provide functionality for other C (and C ++ and Objective - C ) programs to use
- share code across platforms

stack program

~~~c
#include <stdio.h>
#include <stdlib.h>

/* structure defintion */
struct stackStruct
{
	char 	data;
	struct stackStruct *next;
};
typedef struct stackStruct STACK;

/* function prototypes */

STACK *newNode (char data);
void push 	   (STACK **, char);
char pop	   (STACK **);
void printStack (STACK *);
void emptyStack (STACK **);

/* main function */

int main() {
STACK *stack = NULL;
push(&stack,'Q');
push(&stack,'C');
push(&stack,'S');
push(&stack};
printStack(&stack);
     }
     
~~~

~~~
util_stack.h /* has the code for the struct for a stack
~~~

My stack program : restructuring

~~~
#include <util_stack.h>
int main() {
STACK *stack = NULL;
push(&stackm'Q');
push(&stack,'C');
push(&stack,'A');
pop(&stack);
printStack(stack);
emptyStack(&stack);
}
~~~

### Program files: stack example

![image-20220207172513967](/home/jojo/Documents/UNI/term2/images/image-20220207172513967.png)

![image-20220207172527032](/home/jojo/Documents/UNI/term2/images/image-20220207172527032.png)

### Shared code: The stack utility

- **stack.h**

- ~~~
  #includes any .h files needed by stack.c
  defines structures, typedefs etc
  defines function prototypes (push , pop , printStack, emptyStack)
  is #include-ed into any program that wants to use the stack functionality
  ~~~

- **stack.c**

~~~
• #include-s stack.h
• fully defines the functions
• does not contain a main function
• is compiled into stack.o, but not linked
~~~

- **stack.o**

  ~~~
  • is eventually linked to the program that wants to use the functionality
  ~~~

![image-20220207182014589](/home/jojo/Documents/UNI/term2/images/image-20220207182014589.png)

### Shared code: main program using  the stack utility

- **myProgram.h**

  ~~~
  • #include-s any .h files needed by myProgram.c
  • #include-s stack.h
  • defines non-stack structures, typedefs etc
  • defines non-stack function prototypes
  • is #include-ed into myProgram.c
  ~~~

- **myProgram.c**

  ~~~
   #include-s myProgram.h
  • contains a main function
  • fully defines the non-stack functions
  • is compiled into myProgram.o, but not linked
  ~~~

- ### myProgram.o and stack.o

  - ​	are linked together into a myProgram executable

- ### Shared code: storage classes

  ![image-20220207182609715](/home/jojo/Documents/UNI/term2/images/image-20220207182609715.png)

### Storage Classes

**auto** (default)

~~~
int i;
~~~



- declared at the start of block
- storage allocated when block entered and automatically when block exited

### register

~~~
register int i:
~~~



- variable is stored in CPU registers (rather than memory for quick access)

**static**

- variable continues to exist even after the block in which it is defined terminates
- value is  retained between repeated calls to the same function
- scope is limited to the block in which it is defined
- function is only visible within its "translation"

~~~
static int paghNum;
~~~

**extern**

- scope is global
- function is visible globally

![image-20220207184707206](/home/jojo/Documents/UNI/term2/images/image-20220207184707206.png)

### Compile Programs 

![image-20220207184732034](/home/jojo/Documents/UNI/term2/images/image-20220207184732034.png)

Solution 1: make the compiler look in the current directory:

~~~c
#include<stdio.h>
#include"stack.h"
~~~

Solution 2: include the current directory (./) in the compiler's include path:

~~~
gcc -ansi -r./ -c stack.c -o stack.o
~~~

### Compile and Link with header files

To compile the two program modules (seperately:)

~~~
gcc -ansi -I./ -c stack.c -o stack.o
gcc -ansi -I./ -c myProgram.c -o myProgram.o
~~~

and then link them together:

~~~
gcc myProgram.o stack.o -o myProgram
~~~

![image-20220207192430287](/home/jojo/Documents/UNI/term2/images/image-20220207192430287.png)



![image-20220207192458264](/home/jojo/Documents/UNI/term2/images/image-20220207192458264.png)

### **Include guards** 

To avoid trying to include the same code multiple times in one executable, each header file needs a #include guard:

~~~
#ifndef __STACK_H
#define __STACK_H /* Must be unique: double underscore followed by file name in capitals*/
/* content of stack header file, stack.h */
#endif
~~~

![image-20220207192703868](/home/jojo/Documents/UNI/term2/images/image-20220207192703868.png)

Linking and libraries

Libraries group together multiple object files (*.o) into a single unit.

### Static libraries (.a)

- Linked with , and become part of, the application at link time.

### Dynamically linked shared object libraries

- Linked to at runtime

### Library example: maths

![image-20220207195315251](/home/jojo/Documents/UNI/term2/images/image-20220207195315251.png)

### <u>Redirection</u> 

• capture the output generated by your programs into text files
• provide keyboard input from a file

There are three standard streams that all programs can use without calling
fopen or fclose:
• stdin input from the keyboard
• stdout output to the terminal; normal program output
• stderr output to the terminal; error and warning messages
unless redirected by the operating system

~~~c
/* stdfiles.c: an example program using standard output streams */
#include <stdio.h>
int main ()
{
printf("This is an ordinary message\n");
fprintf(stderr,"This is an error message\n");
fprintf(stdout,"This is also an normal output message\n");
return 0;
}
~~~

~~~bash
//Run your program from the Linux command line ($ is the Linux prompt)//
$ stdfiles > out.lis 2> err.lis
The first redirection (>) sends the stdout output to a file called out.lis.
The second redirection (2>) sends the stderr output to a file called err.lis.
~~~

~~~
$ cat out.lis
$ cat err.lis
This is an ordinary message
This is also an normal output message
This is an error message
~~~

~~~
You can send both streams to the same output file:
$ stdfiles > both.lis 2>&1
$ cat both.lis
~~~

~~~
This is an error message
This is an ordinary message
This is also an normal output message
~~~

~~~c
#include <stdio.h>
int main ()
{
printf("This is an ordinary message\n");
fflush(stdout);
fprintf(stderr,"This is an error message\n");
fflush(stderr);
fprintf(stdout,"This is also an normal output message\n");
fflush(stdout);
return 0;
}
~~~

Updated program: both streams to the same output file:

~~~
$ stdfiles > both.lis 2>&1
$ cat both.lis
~~~

~~~
This is an ordinary message
This is an error message
This is also an normal output message
~~~

~~~
You can also redirect the input (remember stdin is the keyboard):
$ stdfiles < inputFile.lis
~~~

The stdfiles program is fed the text in the file as if it had been entered by the keyboard

### machine code : Hello World!

~~~
hexdump -C helloWorld
~~~

![image-20220214105914215](/home/jojo/Documents/UNI/term2/images/image-20220214105914215.png)



## UNIX

![image-20220214110036547](/home/jojo/Documents/UNI/term2/images/image-20220214110036547.png)

more info : https://medium.com/@MrJamesFisher/understanding-the-elf-4bd60daac571

### POSIX

Enables devolopers to write portable applications:

- a family of related standards
- for maintaining compatibility between variants of UNIX
  -  and other operating systems
- defines
  - application programming interface (API)
  - command line shells
  - utility interfaces
- describes a set of fundamental services needed for applications
  - an interface , written in  C
  - a command interpreter 
  - common utility programs 
  - standard semantics and syntax

### Open Group

• established in 1995
• to create a single UNIX specication to ensure compatibility across platforms
• platinum members:
• Capgemini
• Hewlett Packard Enterprise
• Huawei Technologies
• IBM
• Oracle Corporation
• Philips

### Varieties of UNIX

Fully certified:
• Oracle: Solaris
• Hewlett Packard: HP-UX
• IBM: AIX
• Apple: MacOS X, version 10.5 onwards
• Inspur: K-UX
“Mostly” compliant:
• most Linux distributions
• Android
• Cygwin

### Elements of UNIX

![image-20220214114848653](/home/jojo/Documents/UNI/term2/images/image-20220214114848653.png)

### Connecting 

#### telnet

- virtual terminal connection
- application layer protocol over internet or local area network
- interactive text - oriented communication
- unencrypted

ssh:

- encrypted version of telnet

### Standard UNIX editors

- **vi** - specified in the POSIX standard ; lightweight
- **ed** - line editor ; very lightweght
- emacs - incredibly flexible (complicated); heavyweight

ALL UNIX systems come with vi and emacs

**vi** -  designed to work over a 300 bits-per-second modem
**emacs** - “an operating system with a text editor attached”

main difference : speed (**vi**) vs flexibility (**emacs**)

### Environment variables

Show the value of the variable called PATH:

~~~
echo $PATH
~~~

Show the values of all defined variables:

~~~
printenv
~~~

Set the value of the variable called ECM2433:

~~~
export ECM2433=~/ecm2433
cd $ECM2433
~~~

Set the command line prompt to the name of the current server:

~~~
export PS1="`hostname` $ "
~~~

**Everything in UNIX is either a file or a process** 

Every process has:

- A unique PID (process Identifier)
- exactly one parent
  -  apart from the system swapper, which has PID 0
  -  swapper is the ancestor of every process
  -  swapper is part of the Linux kernel
- zero or more children
  - a child is created ("spawned") when the system fork command is called.

### UNIX process commands

#### Processes

~~~
ps - process snapshot

top -  real time list of processes

& - run process in the background

jobs - list of the background child processes of current process

bg - put a paused job into the background

fg - bring a background job into foreground

kill - kill a process

nohup - keep a child process running even when the parent process nishes

nice - lower the priority of child processes as you spawn it

renice - lower the priority of current process.
~~~



### Redirection

~~~
| 	pipe
>	redirect stdout to a new file
< redirect stdin from a file
~~~



#### ps command

~~~
$ ps
PID TTY TIME CMD
10653 pts/0 00:00:00 bash
11559 pts/0 00:00:00 ps
~~~

~~~
$ ps -f
(-f show full details)
UID PID PPID C STIME TTY TIME CMD
jtc202 10653 10652 0 20:43 pts/0 00:00:00 -bash
jtc202 11687 10653 0 20:47 pts/0 00:00:00 ps -f
~~~

~~~
$ ps –efH
-e select all processes
-f full-format listing
-H show process hierarchy
root 2458 1 0 2015 ? 00:00:00 /usr/sbin/sshd
root 15208 2458 0 16:43 ? 00:00:00 sshd:jtc202 [priv]
jtc202 15233 15208 0 16:43 ? 00:00:00 sshd:jtc202@pts/0
jtc202 15234 15233 0 16:43 pts/0 00:00:00 -bash
jtc202 20926 15234 0 17:01 pts/0 00:00:00 tempsleep
jtc202 20937 15234 0 17:01 pts/0 00:00:00 ps -efH
~~~

#### top command

![image-20220214130717967](/home/jojo/Documents/UNI/term2/images/image-20220214130717967.png)

### foreground vs background 

- foreground
  - your session waits until the process has finished
- background 
  - you can continue entering commands while the process runs
  - the process is killed if the parent process finishes

To run a program called tempsleep in the background

~~~
$ tempsleep &
[1] 17286
~~~

To put a foreground process into the background

~~~
$ tempsleep
<CTRL-Z>
[1] + Stopped tempsleep
$ jobs
[1] + Stopped tempsleep
$ bg %1
[1] tempsleep&
~~~

### kill command

To force one of your processes to finish

using the job number

~~~
$ jobs -l
[1] + 18561 Running tempsleep
$ kill %1
~~~

using the PID

~~~
$ jobs -l
[1] + 18561 Running tempsleep
$ kill 18561
~~~

### orphans 

To enable a child process to continue running when you log out

~~~
$ nohup tempsleep &
~~~

### nice and renice commands

All processes run with a priority:

![image-20220214133747947](/home/jojo/Documents/UNI/term2/images/image-20220214133747947.png)

You should always run background processes at a lower priority than foreground ones:

~~~
$ nohup nice tempsleep &
$ renice -p <PID>
~~~

You can only renice your own processes; root can renice anything.

### long - running processes

~~~
$ nohup nice myProgram 1 Hello > out.lis 2> err.lis &
~~~

### process state codes

a = show processes for all users
u = display the process's user/owner
x = also show processes not attached to a terminal

![image-20220214134329210](/home/jojo/Documents/UNI/term2/images/image-20220214134329210.png)

**first character**

- D uninterruptible sleep (usually IO)
- R running or runnable (on run queue)
- S interruptible sleep (waiting for an event to complete)
- T stopped by job control signal
- t stopped by debugger during the tracing
- W paging (not valid since the 2.6.xx kernel)
- X dead (should never be seen)
- Z defunct (“zombie”) process, terminated but not reaped by its parent

second character

- < 	high-priority (not nice to other users)
- N     low-priority (nice to other users)
- L      has pages locked into memory (for real-time and custom IO)
- s      is a session leader
- l       is multi-threaded (using CLONE THREAD, like NPTL pthreads do)

+ is in the foreground process group

![image-20220214134628416](/home/jojo/Documents/UNI/term2/images/image-20220214134628416.png)

### make a long-running process

A program called tempsleep.c that just sleeps for 60 seconds

~~~
{
sleep(60);
return 0;
}
~~~

To run it in the foreground:
$ tempsleep
More usefully, to run it in the background:
$ nice tempsleep &

reminder : top command

$ top -u jtc202

-u show only this user's jtc202 processes

![image-20220214143019333](/home/jojo/Documents/UNI/term2/images/image-20220214143019333.png)

### child processes

![image-20220214143036555](/home/jojo/Documents/UNI/term2/images/image-20220214143036555.png)

~~~c
#include <stdio.h>
#include <unistd.h>
int main ()
{
int pid = fork();
if ( pid < 0 )
{ fprintf(stderr,"Fork failed.\n");
return 1;
}
else if ( pid == 0 )
{ /* the child process */ }
else
{ /* the parent process */ }
return 0;
}
~~~



fork command actioned: child process created as a duplicate of the parent

![image-20220214143931501](/home/jojo/Documents/UNI/term2/images/image-20220214143931501.png)

~~~c
if ( pid < 0 )
{ /* error processing */ }
else if ( pid == 0 )
{
printf("I am the child process\n");
printf("My own pid is %d\n", getpid());
printf("My parent's pid is %d\n", getppid());
}
else
{
printf("I am the parent process\n");
printf("My own pid is %d\n", getpid());
printf("My child's pid is %d\n", pid);
}
~~~

getpid() - get child pid

getppid() - get parent pid

### fork: parent waiting for child to finish

~~~c
#include <sys/wait.h> /* include this */
if ( pid < 0 ) { /* error processing */ }
else if ( pid == 0 )
{ printf("Child: pid is %d\n", getpid());
sleep(5);
printf("Child: finished\n");
}
else
{ int wpid;
int status = 0;
printf("Parent: pid is %d\n", getpid());
printf("Parent: child's pid is %d\n", pid);
wpid = (int)waitpid(pid,&status,0); /* one of the children needs to finish */
printf("Parent process: wpid=%d, status=%d\n",wpid,status);
printf("Parent process: finished\n");
}

~~~



### fork: parent waiting for child to finish

~~~c
#include <sys/wait.h>
if ( pid < 0 ) { /* error processing */ }
else if ( pid == 0 )
{ printf("Child: pid is %d\n", getpid());
sleep(5);
printf("Child: finished\n");
}
else
{ int wpid;
int status = 0;
printf("Parent: pid is %d\n", getpid());
printf("Parent: child's pid is %d\n", pid);
wpid = (int)waitpid(0,&status,0);
printf("Parent process: wpid=%d, status=%d\n",wpid,status);
printf("Parent process: finished\n");
}
~~~

fork: parent waiting for child to finish

~~~c
if ( pid < 0 ) { /* error processing */ }
else if ( pid == 0 )
{ printf("Child: pid is %d\n", getpid());
sleep(5);
printf("Child: finished\n");
}
else
{ int wpid;
int status = 0;
printf("Parent: pid is %d\n", getpid());
printf("Parent: child's pid is %d\n", pid);
wpid = (int)waitpid(0,&status,WNOHANG);
printf("Parent process: wpid=%d, status=%d\n",wpid,status);
wpid = (int)waitpid(0,&status,0);
printf("Parent process: wpid=%d, status=%d\n",wpid,status);
wpid = (int)waitpid(0,&status,WNOHANG);
printf("Parent process: wpid=%d, status=%d\n",wpid,status);
printf("Parent process: finished\n");
}
~~~

**exec**

~~~c
A process can replace itself by calling one of the exec functions, which are all
wrappers for the execve function:
#include <unistd.h>
if ( pid < 0 ) { /* error processing */ }
else if ( pid == 0 )
{
char *argv[] = { "ls", "-al", NULL };
execvp(argv[0], &argv[0]);
fprintf(stderr, "exec failed\n");
return -1;
}
else
{ /* parent process */ }

~~~

### pipes: parent-child communications

A pipe in Linux:

~~~
$ ls | grep hello
~~~

![image-20220214151841620](/home/jojo/Documents/UNI/term2/images/image-20220214151841620.png)

The pipe must be opened before the fork, so that parent and child share it:

~~~c
int childpid;
int fd[2]; /* fd = file descriptor */
if ( pipe(fd) )
{ /* an error occurred */ }
childpid = fork();
~~~

### pipes: parent-child communications

~~~c
else if ( pid == 0 )
{ char str[] = "Hello Mum!";
/* child process closes up input side of pipe */
close(fd[0]);
/* Send "str" through the output side of pipe */
write(fd[1], str, (strlen(str)+1));
}
else
{ char buffer[80];
int numBytes;
/* parent process closes up output side of pipe */
close(fd[1]);
/* Read a string from the input side of the pipe */
numBytes = read(fd[0], buffer, sizeof(buffer));
printf("Parent received string: %s (%d bytes)\n",
buffer, numBytes);
}
~~~

### signals: unrelated process communications 

~~~
The kill command enables you to terminate a long-running background process:
$ myLongProcess&
[1] 10748
either by specifying the process number:
$ kill %1
or the PID:
$ kill 10748
~~~

~~~
What the kill command is actually doing is sending a signal to the process.
The command
$ kill 10748
is actually the equivalent of
$ kill –TERM 10748
which is sending the SIGTERM signal (please terminate) to the process
~~~

![image-20220214152302595](/home/jojo/Documents/UNI/term2/images/image-20220214152302595.png)

### signals

~~~c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
void sig_handler (int signo)
{
if (signo == SIGUSR1)
{
printf("received SIGUSR1\n");
if ( signal(SIGUSR1,sig_handler) == SIG_ERR )
printf("\ncan't catch SIGUSR1\n");
}
}
int main ()
{
if ( signal(SIGUSR1,sig_handler) == SIG_ERR )
printf("\ncan't catch SIGUSR1\n");
while(1)
sleep(1);
return 0;
}
~~~

Start the program as a background process:
$ nice mySignal &
[1] 3160
Send it the signal, using the PID:
$ kill -USR1 3160
received SIGUSR1
Send it the signal again, using the job number:
$ kill -USR1 %1
received SIGUSR1
Send it a different (unhandled) signal:
$ kill -USR2 %1
[1] + User signal 2 nice simplesignal &

### communicating between processes

• signals
	• need to know the PID of the process you are signalling
	• no data can be transferred
	• the receiving process does not need to keep checking
• files
	• one process writes a file, the other reads it (need to consider file locking)
	• data can be transferred
	• receiving process has to keep checking
• pipes
	• each process opens one end of a unidirectional “pipe” down which data is sent
	• the processes must be parent & child, or siblings
	• data can be transferred
	• receiving process has to keep checking

## runtime memory

### physical memory addressing

![image-20220221224407947](/home/jojo/Documents/UNI/term2/images/image-20220221224407947.png)

memory could access any part of physical memory , which can cause problems as nefarious or incompetent programmers could overwrite important parts of memory

### virtual address space

In a multi-tasking operating system, e.g. Linux:
• each process runs in its own lump of memory
its **virtual address space**
• each virtual address space starts at memory address zero
• the operating system maps virtual memory addresses to real, physical memory
addresses using **page tables**
• the virtual address space is usually contiguous

### ![image-20220221224510693](/home/jojo/Documents/UNI/term2/images/image-20220221224510693.png)

goes to cpu and goes to physical address , if not in virtual address than in page table. and if not in page table check disk to be page swapped in to memory  that then writes into mem managing then to physical address.

## virtual address space

![image-20220221224530027](/home/jojo/Documents/UNI/term2/images/image-20220221224530027.png)

stack - predicted in compile time

heap - can't be controlled in compile time and happens in run time

virtual address space - doesn't tamper with kernel space

![image-20220221231500806](/home/jojo/Documents/UNI/term2/images/image-20220221231500806.png)

 objdump to see assembly.

and disassembler could recreate same thing but not the same

### virtual memory: stack

![image-20220222011307341](/home/jojo/Documents/UNI/term2/images/image-20220222011307341.png)

creates mainframe

![image-20220222011324454](/home/jojo/Documents/UNI/term2/images/image-20220222011324454.png)

![image-20220222011335573](/home/jojo/Documents/UNI/term2/images/image-20220222011335573.png)

![image-20220222011403906](/home/jojo/Documents/UNI/term2/images/image-20220222011403906.png)

![image-20220222011415371](/home/jojo/Documents/UNI/term2/images/image-20220222011415371.png)

![image-20220222011453251](/home/jojo/Documents/UNI/term2/images/image-20220222011453251.png)

![image-20220222011508177](/home/jojo/Documents/UNI/term2/images/image-20220222011508177.png)

stack in virtual memory that isn't shared

### C++

- classes
  - compare with C structs
- exceptions
  - compare with C jumps
- function overloading
- operator overloading 

### precompilers

![image-20220221232246511](/home/jojo/Documents/UNI/term2/images/image-20220221232246511.png)

takes code and adds extra codes which comes out as standard C code

![image-20220222104819884](/home/jojo/Documents/UNI/term2/images/image-20220222104819884.png)

![image-20220222104916766](/home/jojo/Documents/UNI/term2/images/image-20220222104916766.png)

C can be linked to C++

compiling and linking

![image-20220222104954381](/home/jojo/Documents/UNI/term2/images/image-20220222104954381.png)

### GNU C++ compiler

ANSI standard C compile:

~~~
gcc -ansi -c myProgram.c -o myProgram.o
~~~

C++ compile:

~~~
g++ -std=c++11 -c myCPPProgram.cpp -o myCPPProgram.o
~~~

and link:

~~~c
g++ myCProgram.o myCPPProgram.o -o myCPPProgram
~~~

### C++ standards

![image-20220222105305882](/home/jojo/Documents/UNI/term2/images/image-20220222105305882.png)

### C++ class  vs  C struct

![image-20220221234710810](/home/jojo/Documents/UNI/term2/images/image-20220221234710810.png)

![image-20220221234758570](/home/jojo/Documents/UNI/term2/images/image-20220221234758570.png)

### C++ function overloading 

~~~c++
int i = -3;
float f = -4.6;
printf("abs(%d)=%d\n",myabs(i));
printf("abs(%f)=%f\n",myabs(f)));
int myabs (int i) {
    if(i<0)
        return -1;
    else
        return i;
}

float myabs (float f){
    if (f<0.0)
        return -f;
    else	
        return f;
}

~~~

number of paramters and different data types

### C++ : what is operator overloading?

~~~
int a = 3;
int b = 4;
int x = a + b;

~~~

Over load + operator to add two rectangle objects

~~~
Rectangle operator+ ( const Rectangle &r){
Rectangle rect;
rect.width = this->width + r.width;
rect.height = this -> height + r.height;
return rect;
}
Rectangle rectagle3 = rectangle1 + rectangle2;
~~~

![image-20220222013605039](/home/jojo/Documents/UNI/term2/images/image-20220222013605039.png)

### Hello world!

~~~c
#include<stdio.h>
#include<iostream>
using namespace std; /* avoid specifying std */
int main() {
	printf("Hello world!\n");
	std :: cout << "Hello world!" << std::endl;
	return 0;	
}
~~~

### cout and cerr

~~~c++
#include<stdio.h>
#include<iostream>
using namespace std; /* avoid specifying std */
int main() {
 	cout << "Count:" << elephantCount << "\n"; /* cout goes to stdout and \n here only prints a newline*/
 	cerr << "Count:" << elephantCount << end1; /* cerr goes to stderr and endl prints a newline and flushes the output buffer*/
 	return 0;
}
~~~

### cout formatting

~~~c++
#include<iomanip>
#include<iostream>
using namespace std;
int main() {
	int aNum=42;
	cout << setfill('*') << setw(10) << aNum << ";" << aNum << endl;
	return 0;
}
~~~

### classes: declaration

~~~c++
#define SIZE 100
class Stack {
	int stck[SIZE];
	int index;
	public:
	void push(int);
	int pop(void);
}
~~~

### classes: access specifiers

~~~
class class-name

{ private variables and functions

access-specifier:

variables and functions

access-specifier:

variables and functions};
~~~

- private(default)

  can only be accessed within the class

- public 

  can be accessed by any part of the program

- protected

  to do with inheritance

![image-20220222112341146](/home/jojo/Documents/UNI/term2/images/image-20220222112341146.png)

header file declares classes and cpp implements the class

![image-20220222112615809](/home/jojo/Documents/UNI/term2/images/image-20220222112615809.png)

constructor function implicitly called

![image-20220222112725979](/home/jojo/Documents/UNI/term2/images/image-20220222112725979.png)

![image-20220222112709544](/home/jojo/Documents/UNI/term2/images/image-20220222112709544.png)

### heap allocation

![image-20220222013719954](/home/jojo/Documents/UNI/term2/images/image-20220222013719954.png)

![image-20220222013743847](/home/jojo/Documents/UNI/term2/images/image-20220222013743847.png)

freeing causes fragmentation of data.

![image-20220222015748813](/home/jojo/Documents/UNI/term2/images/image-20220222015748813.png)

![image-20220222015803317](/home/jojo/Documents/UNI/term2/images/image-20220222015803317.png)

### base / stack pointers

You can access the current base and stack pointers programmatically:

~~~
#include <stdint.h>
uint64_t g_bp;
uint64_t g_sp;
#define GETSP __asm__ ("mov %%rsp,%0": "=rm" (g_sp))
#define GETBP __asm__ ("mov %%rbp, %0": "=rm" (g_bp))
On a 64-bit machine:
%rsp is the stack pointer register
%rbp is the base (frame) pointer register
In ANSI C , __asm__ performs assembler instructions.
~~~

![image-20220222020844051](/home/jojo/Documents/UNI/term2/images/image-20220222020844051.png)

### jump

- error catching
- coroutines

### program state

The state of an executing program depends on:

- virtual address space
  - code: executing part
  - data/BSS : static variables
  - stack : function return address , parameters , auto variables
  - heap: dynamic allocated variables
- registers , including
  - sp : stack pointer
  - bp : base pointer
  - pc : program counter - which program statement to execute

### setjmp

~~~c++
#include<stdio.h>
#include<setjmp.h>
int main() 
{
jmp_buf mainbuf;
if (set jmp(mainbuf) == 0){
	printf("register contents stored\n"); /*setjmp stores the registers and returns the value 0 */
	return 0;}
}
longjmp(mainbuf,2); /* longjmp jumps back to setjmp and setjmp returns the value 2*/
printf("after longjmp\n"); 
return 0;
~~~

setValue = 0

setValue = 2

### setjmp/longjmp error handling

use case of jmp

~~~c
jmp_buf 	g_mainbuf; /* only time use global*/
int main (int argc, char *argv[])
{
if (setjmp(g_mainbuf) != 0){
	printf("error\n");
	return 1;
}
funcA(argc);
return 0;
}
~~~

~~~C
void funcA (int x){
	funcB(x);
}

void funcB(int x){
	funcC(x);
}

void funcC (int x){
	if (x ==1)
	longjmp(g_mainbuf,1);
	else 
	printf("x is %d\n",x);
}
~~~

provides a graceful way to shutdown errors

how it works



![image-20220222094557225](/home/jojo/Documents/UNI/term2/images/image-20220222094557225.png)

![image-20220222094608890](/home/jojo/Documents/UNI/term2/images/image-20220222094608890.png)

![image-20220222094619746](/home/jojo/Documents/UNI/term2/images/image-20220222094619746.png)

![image-20220222094632029](/home/jojo/Documents/UNI/term2/images/image-20220222094632029.png)

![image-20220222094640936](/home/jojo/Documents/UNI/term2/images/image-20220222094640936.png)

### subroutines vs coroutines

- subroutine

![image-20220222094712745](/home/jojo/Documents/UNI/term2/images/image-20220222094712745.png)



- coroutine

  ![image-20220222094754222](/home/jojo/Documents/UNI/term2/images/image-20220222094754222.png)

operates in parallel



### concurrency vs parallelism

![image-20220222094841640](/home/jojo/Documents/UNI/term2/images/image-20220222094841640.png)

- concurrency

  - multiple processes accessing one disk 
  - multiple processes sharing one CPU
    - time slicing 
    - context switching
  - parallelism
    - multiple processes running on separate CPU's

  coroutines are concurrent but no parallel

  Coroutines are used are in computer games to maintain a high framerate:

  - having a **computationally heavy routine** that needs to run
  - you do not want that entire routine to run within one frame
    - It would impact the frame rate and make the gameplay look jerky
  - coroutines can **split** the computationally heavy single routine whilst yielding "time" back to the game loop 
    - thereby keeping the frame rate stable
  - the program **switches** between the coroutine and the game loop

So coroutines allow the computationally heavy routine to be split across ,multiple frames rather than requiring it to finish in one

### setjmp/longjmp coroutines

~~~c
jmp_buf g_pingbuf
jmp_buf g_pongbuf
void ping();
void pong();

int main() {
	ping();
	return 0;
}
~~~

~~~c
void pong(){
	while(1){
		printf("  pong\n");
		if(setjmp(g_pongbuf) == 0)
			longjmp(g_pingbuf,1);
	}
	printf("	pong finished\n");
}
~~~

~~~c
void ping() {
	static int i;
    if (setjmp(g_pingbuf) == 0)
        pong();
    for (i = 0; i < 5 ; i++){
        printf("ping %d\n",i);
        sleep(1);
        if (setjmp(g_pingbuf) == 0)
            longjmp(g_pongbuf,1);
    }
    printf("ping finished\n");
	
}
~~~

![image-20220222100152154](/home/jojo/Documents/UNI/term2/images/image-20220222100152154.png)

![image-20220222100158975](/home/jojo/Documents/UNI/term2/images/image-20220222100158975.png)

![image-20220222100207199](/home/jojo/Documents/UNI/term2/images/image-20220222100207199.png)

![image-20220222100728058](/home/jojo/Documents/UNI/term2/images/image-20220222100728058.png)

![image-20220222100743433](/home/jojo/Documents/UNI/term2/images/image-20220222100743433.png)

![image-20220222100756653](/home/jojo/Documents/UNI/term2/images/image-20220222100756653.png)

![image-20220222100214430](/home/jojo/Documents/UNI/term2/images/image-20220222100214430.png)

### coroutines and the stack

Coroutines work because the stack frames of the two routines stay on the stack

![image-20220222100922142](/home/jojo/Documents/UNI/term2/images/image-20220222100922142.png)

![image-20220222100930744](/home/jojo/Documents/UNI/term2/images/image-20220222100930744.png)

![image-20220222100942923](/home/jojo/Documents/UNI/term2/images/image-20220222100942923.png)

![image-20220222100958145](/home/jojo/Documents/UNI/term2/images/image-20220222100958145.png)

### recursion

![image-20220222101131061](/home/jojo/Documents/UNI/term2/images/image-20220222101131061.png)

## C ++ Inheritance

![image-20220301100621586](/home/jojo/Documents/UNI/term2/images/image-20220301100621586.png)



![image-20220301100640011](/home/jojo/Documents/UNI/term2/images/image-20220301100640011.png)



![](/home/jojo/Documents/UNI/term2/images/image-20220301100648101.png)

![image-20220301101755507](/home/jojo/Documents/UNI/term2/images/image-20220301101755507.png)

### Multiple inheritance

- otherwise as a publish and subscribe model or design pattern

One publisher

- creates alerts (or messages)
- alerts might be timed or event-driven

Multiple subscribers

- registers their wish to recieve alerts
- then automatically receive the alerts

### Observer pattern

![image-20220301104216227](/home/jojo/Documents/UNI/term2/images/image-20220301104216227.png)

![image-20220301104229015](/home/jojo/Documents/UNI/term2/images/image-20220301104229015.png)

![image-20220301104244368](/home/jojo/Documents/UNI/term2/images/image-20220301104244368.png)

![image-20220301104737639](/home/jojo/Documents/UNI/term2/images/image-20220301104737639.png)

### coding standards

Every organisation has coding standards

~~~
Two examples for C++:
• https://google.github.io/styleguide/cppguide.html
• https://isocpp.org/wiki/faq/coding-standards
~~~

### reminder: class definitions

![image-20220301105335924](/home/jojo/Documents/UNI/term2/images/image-20220301105335924.png)

### constructors and deconstructions

![image-20220301105348053](/home/jojo/Documents/UNI/term2/images/image-20220301105348053.png)

### parameterised constructors

~~~c++
class NewClass
{
int a,b;
public:
NewClass(int,int); // parameterised constructor
void showValues();
};
NewClass::NewClass(int i, int j)
{
a = i;
b = j;
}
void NewClass::showValues ()
{
cout << "a=" << a;
cout << ", b=" << b << endl;
}
~~~

~~~c++
int main ()
{
NewClass nc(3,4);
nc.showValues();
return 0;
}
a=3, b=4
~~~

### parameterised constructors: overloaded

~~~c++
class NewClass{
	int a,b;
	public:
	NewClass(int,int); // parameterised constructor valid overloading: differing number of args
	NewClass(int);     // parameterised constructor
	void showValues();
}

NewClass::NewClass(int i, int j)
{
a = i;
b = j;
}
NewClass::NewClass(int i)
{
a = i;
b = 0;
}

~~~

~~~c++
int main ()
{
NewClass nc(3,4);
nc.showValues();
NewClass md(2);
md.showValues();
return 0;
}
a=3, b=4
a=2, b=0
~~~

### parameterised constructors : default values

~~~c++
class NewClass
{
int a,b;
public
NewClass(int,int); // parameterised constructor
void showValues();
};
NewClass::NewClass(int i, int j=0)
{
a = i;
b = j;
}
~~~

~~~c++
int main ()
{
NewClass nc(3,4);
nc.show();
NewClass md(2);
md.show();
return 0;
}
a=3, b=4
a=2, b=0
~~~

### function parameters : default values

Only trailing parameters can be defaulted:

~~~
void NewClass::someFunction(int i, int j=0) correct!
void NewClass::someFunction(int i=1, int j=0) correct!
void NewClass::someFunction(int i=1, int j) wrong
~~~

Does not have to be a class member function:

~~~c++
void someOtherFunction(int a, char b='X', float f=0.0, std::string str="Hello!")
~~~

### constructors and destructors

Consider variable Monarch.name

### Constructor:

• malloc memory to pointers

### Destructor:

• free memory allocated to pointers 

• also, e.g., release locks

~~~c++
class Monarch
{
char *name;
int year;
public:
Monarch(char *,int);
~Monarch();
char *getName();
int getYear();
};

~~~

### pointers 

~~~c++
/*can do this*/
int *p = (int *)malloc(sizeof(int)*25);
p[4] = 43;
free(p);
~~~

~~~c++
/* also this*/
MyClass *c = (MyClass *)malloc(sizeof(MyClass));
c->num = 4;
c->memberFunction();
free(c);
~~~

However , the MyClass constructor and destructor functions are not called.

### pointers: new and delete

#### C way:

~~~c++
int *p = (int *) malloc(sizeof(int)*25);
free(p)
~~~

~~~c++
MyClass *c = (MyClass *)malloc(sizeof(MyClass));
free(c);
~~~

~~~c++
MyClass *c = (MyClass *)malloc(sizeof(MyClass)); // malloc allocates memory but does NOT call construtor
free(c); // free - frees memory but does NOT call the constructor

~~~



#### C++ way:

~~~c++
int *p = new int; // a single integer, uninitialised
int *p = new int(43); // a single integer, initialised to value 43
int *p = new int[25]; // an array of 25 integers
delete p; // free the single value p
delete[] p; // free the array p
~~~

~~~c++
MyClass *c = new MyClass; // a single MyClass, uninitialised, new allocates memory then calls constructor
MyClass *c = new MyClass(43); // a single MyClass, initialised with value 43
MyClass *c = new MyClass[25]; // an array of 25 MyClass’es
delete c; // free the single value c
delete[] c; // free the array c , delete calls the destructor then deallocates memory
~~~

You can overload new and delete, either globally or for a specific class For example, you might write a custom delete that overwrites deallocated memory with zeros for data security reasons

### references

~~~c++
void addTen (int x)   //pass by value
{
x+=10;
}
int main ()
{
int num = 4;
cout << "num=" << num << endl;
addTen(num);
cout << "num=" << num << endl;
return 0;
}

/*num=4
num=4*/
~~~

~~~~c++
void addTen (int *x)
{
*x+=10;
}
int main ()
{
int num = 4;
cout << "num=" << num << endl;
addTen(&num);// has pointer , psuedo pass by reference
cout << "num=" << num << endl;
return 0;
}

num=4
num=14
~~~~

pass by reference

~~~c++
void addTen (int &x)
{
x+=10;
}
int main ()
{
int num = 4;
cout << "num=" << num << endl;
addTen(num);
cout << "num=" << num << endl;
return 0;
}

num=4
num=14


~~~

A reference is an alias for a variable:

~~~c++
int num = 43;
int &ref = num;
cout << "num=" << num << "; ref=" << ref << endl;
num = 50;
cout << "num=" << num << "; ref=" << ref << endl;
ref = 99;
cout << "num=" << num << "; ref=" << ref << endl;
~~~

reference as a function return value

~~~c++
char &setValue (char *str)
{
return str[2];
}
int main ()
{
char str[] = "Hello World!";
cout << "str=" << str << endl;
setValue(str) = 'X';  // The function call is appearing on the left hand side of an assignment
cout << "str=" << str << endl;
return 0;
}
~~~

pointers: this

this is a pointer to the current object. Used to avoid ambiguities:

~~~c++
NewClass::NewClass(int a, int b)
{
this->a = a;
this->b = b;
}
~~~

if you want to pass the object to a function:

~~~c++
void func(MyClass&);
void MyClass::doSomething()
{
func(*this);
}

MyClass &MyClass::doSomethingElse()
{
return *this;
}
~~~

copy constructor

A member function that initialises an object using another object of the same class.

Copy constructor declaration(function prototype):

~~~
MyClass(const MyClass &)
~~~

Used like this:

~~~
MyClass c, d;
MyClass e = c; // calls the copy constructor
d = e; // calls an assignment operator not the copy constructor
~~~

Note the following: • if the copy constructor is private, that prevents copying of the objects in that class

If no copy constructor is provided, C++ makes a default one that does a memberwise copy (unlike Java)

~~~c++
class MyClass
{
int x;
char y;
char *str;
};
MyClass a,b;
b = a;

/*
memberwise copy:
b.x = a.x; // ok
b.y = a.y; // ok
b.str = a.str; // probably not ok

probable copy constructor:
b.x = a.x;
b.y = a.y;
b.str = (char *)malloc(strlen(a.str)+1);
if ( b.str==NULL ) {...}
strcpy(b.str,a.str);
*/


~~~

### static member variables

- are shared by all objects of the same class
- can be accessed even if no objects exist

~~~c++
declare variable in MyClass.hpp
class MyClass
{
public:
static int counter;
}

//define intialised in MyClass.cpp
int MyClass::counter{0};
~~~

### Inheritance

- general form
- access specifiers
- constructors and destructors
- an introduction to multiple inheritance
- virtual base classes
- virtual member functions

### reminder : class definition

~~~c++
// MyString.cpp
#include <string.h>
#include <MyString.hpp>
// Constructor
MyString::MyString (const char *str)
{
// Make sure thestring is big enough for the data
if ( (thestring = (char *)malloc(strlen(str)+1)) == NULL )
{ /* error processing */ }
// Now copy the string
strcpy(thestring,str);
}
// Returns the length of this string
int MyString::len()
{ return strlen(thestring); }
~~~

~~~c++
// MyString.hpp
class MyString
{
char *thestring;
public:
MyString(const char *);
int len();
};
~~~

~~~c++
// aprogram.cpp
#include <MyString.hpp>
int main()
{
MyString s("Hello");
printf("length is %d",s.len());
}
~~~

inheritance: general form

General form for class inheritance:

~~~c++
 class derived-class-name : access-specifier base-class-name { /* body of class */ };
~~~

For example:

~~~c++
class MySpecialString: public MyString
{
char type;
public:
MySpecialString(char, const char *);
};
~~~

inheritance: access specifiers

![image-20220301143121663](/home/jojo/Documents/UNI/term2/images/image-20220301143121663.png)

**Protected:** members in a class are similar to private members as they cannot be accessed from outside the class. But they can be accessed by derived classes while private members cannot.

Inheritance: public

~~~c++
class base
{
int i;
protected:
int j;
public:
void set(int a, int b); // i=a; j=b;
void show(); // printf("i=%d, j=%d\n",i,j);
};
class derived: public base
{
int k;
public:
derived(int x); // k=x; i=0; j=0;
void showk(); // printf("k=%d\n",k);
};

/*derived obj(3);
obj.set(1,2); base
obj.show(); base
obj.showk(); derived*/ 

~~~

Inheritance: protected

~~~c++
class base
{
int i;
protected:
int j;
public:
void set(int a, int b); // i=a; j=b;
void show(); // printf("i=%d, j=%d\n",i,j);
};
class derived: protected base
{
int k;
public:
derived(int x); // k=x; i=0; j=0; i is private to base
void showk(); // printf("k=%d\n",k); 
};

/*derived obj(3);
obj.set(1,2); error , base is not accessible base of derived
obj.show(); error
obj.showk(); derived*/
~~~

inheritance: private

~~~c++
class base
{
int i;
protected:
int j;
public:
void set(int a, int b); // i=a; j=b;
void show(); // printf("i=%d, j=%d\n",i,j); I is private to base
};
class derived: private base
{
int k;
public:
derived(int x); // k=x; i=0; j=0; i is private to abse
void showk(); // printf("k=%d\n",k);
};

/*
derived obj(3);
obj.set(1,2); error base is not an accesible base of derived
obj.show();
obj.showk();
*/
~~~

multiple inheritance

~~~c++
class base1
{
protected:
int x;
public:
void showx(); // printf("x=%d\n",x);
};
class base2
{
protected:
int y;
public:
void showy(); // printf("y=%d\n",y);
};
class derived: public base1, public base2
{
public:
void set(int i,int j); // x=i; y=j;
};

/*
int main(){
	derived obj;
	
	obj.set(1,2); derived
	obj.shox();	base1
	obj.showy(); base2

}*/

~~~

inheritance: constructors and destructors

~~~c++
class base
{
public:
base(); // cout << "Constructing base" << endl;
~base(); // cout << "Destructing base" << endl;
};
class derived: public base
{
public:
derived(); // cout << "Constructing derived" << endl;
~derived(); // cout << "Destructing derived" << endl;
};
// This program does nothing but construct and destruct
int main ()
{
derived obj;
return 0;
}

~~~

~~~c++
class base
{
public:
base(); // cout << "Constructing base" << endl;
~base(); // cout << "Destructing base" << endl;
};
class derived: public base
{
public:
derived(); // cout << "Constructing derived" << endl;
~derived(); // cout << "Destructing derived" << endl;
};
// This program does nothing but construct and destruct
int main ()
{
derived obj;
return 0;
}

/*Constructing base
Constructing derived
Destructing derived
Destructing base*/
~~~

### inheritance: constructors and destructors

General rules:
• Constructors are executed in order of derivation.
• Destructors are executed in reverse order of derivation.

~~~~c++
class base
{
public:
base(); // cout << "Constructing base" << endl;
~base(); // cout << "Destructing base" << endl;
};
class derived1: public base
{
public:
derived1(); // cout << "Constructing derived1" << endl;
~derived1(); // cout << "Destructing derived1" << endl;
};
class derived2: public derived1
{
public:
derived2(); // cout << "Constructing derived2" << endl;
~derived2(); // cout << "Destructing derived2" << endl;
};
// This program does nothing but construct and destruct
int main ()
{
derived2 obj;
return 0;
}
/*
chain inheritance
Constructing base
Constructing derived1
Constructing derived2
Destructing derived2
Destructing derived1
Destructing base*/

~~~~

simple inheritance

~~~c++
class base1
{
public:
base1(); // cout << "Constructing base1" << endl;
~base1(); // cout << "Destructing base1" << endl;
};
class base2
{
public:
base2(); // cout << "Constructing base2" << endl;
~base2(); // cout << "Destructing base2" << endl;
};
class derived: public base1, public base2
{
public:
derived(); // cout << "Constructing derived" << endl;
~derived(); // cout << "Destructing derived" << endl;
};
// This program does nothing but construct and destruct
int main ()
{
derived obj;
return 0;
}

/*multple inheritance
Constructing base1
Constructing base2
Constructing derived
Destructing derived
Destructing base2
Destructing base1*/

~~~

~~~c++

class base
{
protected:
int i;
public:
base(int x); // i=x; cout << "Constructing base" << endl;
~base(); // cout << "Destructing base" << endl;
};
class derived: public base
{
int j;
public:
derived(int x, int y);  /* 
erived::derived(int x, int y): base(y)
{
j=x;
cout << "Constructing derived" << endl;
}*/
    
~derived(); // cout << "Destructing derived" << endl;
    /* */
void show(); // printf("i=%d, j=%d\n", i, j);
};
int main ()
{
derived obj(3,4);
obj.show();
return 0;
}
//i=4, j=3

~~~

~~~c++
//multiple inheritance
class base1
{
protected:
int i;
public:
base1(int x); // i=x; cout << "Constructing base1" << endl;
~base1(); // cout << "Destructing base1" << endl;
};
class base2
{
protected:
int j;
public:
base2(int y); // j=y; cout << "Constructing base2" << endl;
~base2(); // cout << "Destructing base2" << endl;
};
class derived: public base1, public base2
{
int k;
public:
derived(int x, int y, int z);
    /*
    derived::derived(int x, int y, int z): base1(y), base2(z)
{
k=x;
cout << "Constructing derived" << endl;
*/
~derived(); // cout << "Destructing derived" << endl;
void show(); // printf("i=%d, j=%d, k=%d\n", i, j, k);
};

int main ()
{
derived obj(3, 4, 5);
obj.show();
return 0;
}
i=4, j=5, k=3

~~~

multiple inheritance: "The diamond problem"

~~~c++
class base
{
public:
int i;
};
class derived1: public base
{
public:
int j;
};
class derived2: public base
{
public:
int k;
};
class derived3: public derived1, public derived2
{
public:
int sum;
};

int main ()
{
derived3 obj;
obj.j = 10;//derived 1
obj.k = 10;//derived 2
obj.i = 10; //which i?
return 0;
}


~~~

solution 1 : apply the scope resolution operator

~~~c++
int main ()
{
derived3 obj;
obj.j = 10;
obj.k = 10;
obj.derived1::i = 10;
return 0;
}

/*apply the scope resolution
operator*/
~~~

solution 2

~~~c++
class base
{
public:
int i;
};
class derived1: virtual public base // VIRTUAL  prevents two copies of base being included in //derived 3
{
public:
int j;
};
class derived2: virtual public base
{
public:
int k;
};
class derived3: public derived1, public derived2
{
public:
int sum;
};
~~~

~~~c++
int main ()
{
derived3 obj;
obj.j = 10;
obj.k = 10;
obj.i = 10;
return 0;
}
~~~

~~~c++
class base
{public:
virtual void print(); /* print() may be overriden in a derived class*/
void show();
};
class derived: public base
{public:
void print(); // <-
void show();
};
int main()
{
derived d;
base *b = &d;
// virtual function, bound at runtime
b->print();
// non-virtual function, bound at compile time
b->show();
}

derived print
base show

~~~



~~~c++
class base
{public:
virtual void print()=0; /*print() must be overridden in a derived class*/
void show();
};
class derived: public base
{public:
void print();/* <-there is no base class definition
for the print() function */
void show();
};
int main()
{
derived d;
base *b = &d;
// virtual function, bound at runtime
b->print();
// non-virtual function, bound at compile time
b->show();
    
    /*compile-time error if the derived
print() function does not exist*/
}
~~~

### multiple inheritance

![image-20220301153226613](/home/jojo/Documents/UNI/term2/images/image-20220301153226613.png)

![image-20220301153242771](/home/jojo/Documents/UNI/term2/images/image-20220301153242771.png)![image-20220301153242904](/home/jojo/Documents/UNI/term2/images/image-20220301153242904.png)

![image-20220301153258092](/home/jojo/Documents/UNI/term2/images/image-20220301153258092.png)

Key features:

- One to many relationships between publisher and subscriber
- change of state at the publisher is automatically notified to any number of subscribers
- weak coupling between publisher and subscribers

![image-20220301153413610](/home/jojo/Documents/UNI/term2/images/image-20220301153413610.png)

### ![image-20220301153504971](/home/jojo/Documents/UNI/term2/images/image-20220301153504971.png)

![image-20220301153518098](/home/jojo/Documents/UNI/term2/images/image-20220301153518098.png)

![image-20220301153525154](/home/jojo/Documents/UNI/term2/images/image-20220301153525154.png)

![image-20220301153627374](/home/jojo/Documents/UNI/term2/images/image-20220301153627374.png)

![image-20220303165416342](/home/jojo/Documents/UNI/term2/images/image-20220303165416342.png)

![image-20220303165428648](/home/jojo/Documents/UNI/term2/images/image-20220303165428648.png)

### friend functions 

In relation to a class , a **friend** function is 

- a non member function
  - i.e. a function that is not a member of the class
- which has access to the private and protected elements of the class
  - i.e.  the class for which it is a **friend**

**Friendship** is <u>not</u>

- inherited 
  - ex your friends children are not your friends
- tranisitive
  - a friend of your friend is not your friend

#### friend function: exampple 1

~~~c++
class MyClass{
	int a , b ;
	public:
	MyClass(int,int);
	friend int sum(MyClass);
};

MyClass::MyClass (int i,int j){
	a = i;
	b = j;
}

int sum (MyClass x) /* sum is not a member of MyClass , or any other class*/
{
	return x.a + x.b; /* but can access the private members of MyClass*/
}

int main() {
    MyClass n(3,4);
    cout << sum(n) << endl;
    return 0;
}
~~~

#### friend function: example 2

Tbe friend function may be a member of another class:

~~~c++
class MyOtherClass; // forward reference;  a sort of "class" prototype
class MyClass
{
    int a,b;
    public:
    	friend int MyOtherClass::sum(MyClass);
    	void setab(int,int);
};

class MyOtherClass
{
    int c;
    public:
    	int sum(MyClass);
};
int MyOtherClass::sum (MyClass x) {...}
~~~

#### friend function: operator overloading

One speicifc use of friend function is in relation to operator overloading 

###### overloading background 

Consider the data class

~~~c++
class MyDate
{
    int year; // 
    unisigned int month;
    unsigned int day;
    public:
    	MyDate::(unsigned int day, unsigned int month, int year){
            this -> day = day;
            this -> month = month;
            this -> year = year;
        }
}

int main(){
    //1st March 2021
    MyDate dt(1,3,2021);
    return 0;
}
~~~

###### operator overloading : background

###### With these declarations:

~~~
MyDate dt1(29,6,2015); //function overloading more than one function with the same name
MyDate dt2(1,3,2021);
int diff;
MyDate dt3;
~~~

could do something like 

~~~
diff = dt2 - dt1; // operator overloading more than one "meaning" of an operator
dt3 = dt2 + 43;
~~~

rather than something like this:

~~~
diff = dt2.difference(dt1);
dt3 = dt2.addDays(43);
~~~

The aim of operator overloading it to make life **easier for user of a class** , not for the developer of the class.

**Easier** means:

- easier to understand the code
- fewer code defects

The following operators cannot be overloaded:

~~~
.
sizeof
?:
::
.*
~~~

all the other can however:

~~~
+
%
()
[]
<=
<<
++
&
new 
delete
~~~

###### operator overloading: +

~~~c++
class MyInteger {
	int i;
	public:
		MyInteger (int i) {
			this -> i = i;
		}
		int operator+(MyInteger);
};
int MyInteger::operator+(MyInteger m){
	return this->i +m.i;
}

int main(){
	MyInteger a(4);
	MyInteger b(3);
	MyInteger c;
	
	c = a + b ;
	
	return 0;
}
~~~

~~~c++
class MyInteger
{
int i;
public:
MyInteger (int i) { this->i = i; }
int operator+(MyInteger);
int operator+(int);
friend int operator+(int, MyInteger);
};
// This function represents <MyInteger> + <MyInteger>
int MyInteger::operator+ (MyInteger m) // c  = a + b
{
return this->i + m.i;
}
// This function represents <MyInteger> + <int>
int MyInteger::operator+ (int a) // c = c + 6
{
return this->i + a;
}

// This function represents <int> + <MyInteger>
int operator+ (int a, MyInteger m) // c = 8 + c
{
return a + m.i;
}
~~~

###### operator overloading

Two considerations:

1. At least one of the operands of an overlaoded operator must be of a user defined type (usually this is a class)

2. Overloaded operators are just function calls , so cannot preserve

   ![image-20220308010820500](/home/jojo/Documents/UNI/term2/image-20220308010820500.png)

the operator , according to its built in schematics

One other consideration:

**Just because you can , doesn't mean you should**

• If you define arithmetic operators, maintain the usual arithmetic identities. For example, if your
class defines x + y and x - y, then x + y - y ought to return an object that is behaviourally
equivalent to x.

You should provide arithmetic operators only when they make logical sense to users.

![image-20220308010958057](/home/jojo/Documents/UNI/term2/image-20220308010958057.png)

~~~c++
class MyArray
{
int data[100];
public:
int &elem(unsigned int i) { if (i > 99) error(); return data[i]; }
};
int main()
{
MyArray a;
a.elem(10) = 42;
a.elem(12) += a.elem(13);
return 0;
} 
~~~

~~~c++
class MyArray
{
int data[100];
public:
int &operator[] (unsigned int i) { if (i > 99) error(); return data[i]; }
};
int main()
{
MyArray a;
a[10] = 42;
a[12] += a[13];
return 0;
}
~~~

The difference between [] and () for subscripting:
• [] allows only one index
• e.g. array[4]
• () allows multiple indices
• e.g. matrix(5,1)

Consider this date class again:

~~~c++
class MyDate
{
int year;
unsigned int month;
unsigned int day;
public:
MyDate(unsigned int,unsigned int,int);
}
MyDate::MyDate (unsigned int day, unsigned int month, int year)
{
this->day = day;
this->month = month;
this->year = year;
}
~~~

~~~c++
int main ()
{
// 1st March 2021
MyDate dt(1,3,2021);
return 0;
}
~~~

It would be very desirable to be able to do this:

~~~
MyDate dt(1,3,2021);
cout << "The date is: " << dt << ". Happy Birthday!" << endl;
~~~

to output a date in a particular format

This requires to overload the << operator

~~~c++
lass MyDate
{
int year;
unsigned int month;
unsigned int day;
public:
MyDate(unsigned int,unsigned int,int);
friend ostream &operator<<(ostream &os, MyDate &dt);
}
ostream &operator<<(ostream &os, MyDate &dt)
{
os << dt.day << '/' << dt.month << '/' << dt.year;
return os;
}
~~~

~~~c++
The overloaded << operator returns a reference to the original ostream object:
ostream &operator<<(ostream &os, MyDate &dt)
{
os << dt.day << '/' << dt.month << '/' << dt.year;
return os;
}
which means you can combine insertions, like this:
cout << "The date is: " << dt << ". Happy Birthday!" << endl;
~~~

### Templates

#### swap example  1

Some overloaded functions are very generic, i.e. they could be applied to almost any datatype:

![image-20220308130316059](/home/jojo/Documents/UNI/term2/image-20220308130316059.png)

~~~c++
void myswap (int &x , int &y){
	int temp = x;
	x = y;
	y = temp;
}

void myswap (float &x,float &y)
{
	float temp = x;
	x = y;
	y = temp;
}

void myswap (MyClass &x, MyClass &y)
{
	MyClass temp = x;
	x = y;
	y = temp;
}
~~~

#### stack Example 2

Our class called Stack is not really "Stack",  it is "IntegerStack"

~~~c++
class Stack 
{
	int stck[SIZE];
	int index;
	public: 
		void push(int); 
		int pop(void);
}
~~~

~~~c++
int main() {
	Stack s;
	s.push(23);
	s.push(42);
}
~~~

#### templates

##### function template

instructions for how to build a family of similar looking functions

~~~c++
template<dataname T>
void myswap (T &x,T &y){
 T temp = x;
 x = y;
 y = temp;
}
~~~

~~~c++
int main ()
{
int a = 1;
int b = 2;
cout << "a=" << a << ", b=" << b << endl;
myswap(a,b);
cout << "a=" << a << ", b=" << b << endl;
string c = "elephants";
string d = "penguin";
cout << "c=" << c << ", d=" << d << endl;
myswap(c,d);
cout << "c=" << c << ", d=" << d << endl;
return 0;
}
~~~

##### class template

how to build a famly of similar looking classes

~~~c++
template<typename T>
class Stack {
	T stck[SIZE];
	int index;
	public:
		static int count;
		Stack();
		Stack(Stack &);
		~Stack();
		void push(T);
		T	 pop(void);
};
~~~

~~~c++
class Stack {
	 int stck[SIZE];
	 int index;
	 public:
	 static int count;
	 Stack();
	 Stack(Stack &);
	 ~Stack();
	 void push(int);
	 int pop(void);
};
~~~

~~~
Stack<int> sl;
sl.push(23);
cout << sl.pop() << endl;

Stack<string> *s2 = new Stack<string>;
s2->push("Hello");
cout << s2 -> pop() <<endl;
delete s2;
~~~

##### standard templates 

Some data structures , such as stacks and queues are used very frequently that C++ provides a set of standard templates through the **standard Template Librarary**

Four main components:

- containers
  - e.g. vectors , queue, stack
- Iterators
  - objects that enable a program to traverse a container
- algorithms
  - e.g. binary search
- functions

### STL: container : stack

After all your C and C++ stack coding , the STL provides a stack template 

![image-20220308210210935](/home/jojo/Documents/UNI/term2/image-20220308210210935.png)

~~~
#include <stack>
std::stack<int> si;
si.push(43);
si.push(99);
std::cout << "Size: " << si.size() << std::endl;
std::cout << "Top : " << si.top() << std::endl;
si.pop();
std::cout << "Top : " << si.top() << std::endl;
std::cout << "Size: " << si.size() << std::endl;
std::stack<float> sf;
sf.push(5.86);
std::stack<MyClass> st;
MyClass m;
st.push(m);
~~~

### Vector

Vectors are sequence containers representing arrays that can change in size

Just like arrays, vectors use conitiguous storage locations for their elements, which means that their elements can also be accessed using offsets on regular pointers to its elements, and just as efficiently as in arrays. But unlike arrays, their size can change dynamically, their storage being handled automatically by the container.

Internally , vectors use dynamically allocate array to store their elements. This array may need to be reallocated in order to grow in size when new elements are inserted , which implies allocating a new array and moving all elements to it. This relatively expensive task in terms of processing time , and thus , vectors do not reallocate each time an element is added to the container.

~~~c++
#include <vector>
std::vector<int> v;
v.push_back(43);
v.push_back(99);
v.push_back(0);
~~~

![image-20220308210723384](/home/jojo/Documents/UNI/term2/image-20220308210723384.png)

### STL : iterator

~~~
std::vector<int> myvector;
std::vector<int>::iterator it;

for (int i=1;i<=5;i++)
	myvector.push_back(i);

std::cout << "myvector contains:";
for (it =myvector.begin();it!myvector.end();it++)
	std::cout << ''<< *it;
std::cout << std::endl;
~~~

## Exceptions

![image-20220314123305721](/home/jojo/Documents/UNI/term2/image-20220314123305721.png)

![image-20220314123321570](/home/jojo/Documents/UNI/term2/image-20220314123321570.png)

![image-20220314123504913](/home/jojo/Documents/UNI/term2/image-20220314123504913.png)

### ![image-20220314123516356](/home/jojo/Documents/UNI/term2/image-20220314123516356.png)

### Nesting

![image-20220314123733102](/home/jojo/Documents/UNI/term2/image-20220314123733102.png)

#### Limiting

![image-20220314123851216](/home/jojo/Documents/UNI/term2/image-20220314123851216.png)

### Exception objects

![image-20220314123923714](/home/jojo/Documents/UNI/term2/image-20220314123923714.png)

![image-20220314124919138](/home/jojo/Documents/UNI/term2/image-20220314124919138.png)

![image-20220314125151361](/home/jojo/Documents/UNI/term2/image-20220314125151361.png)

catch more important one first

### Standard excpetions

![image-20220314125216434](/home/jojo/Documents/UNI/term2/image-20220314125216434.png)

![image-20220314125248730](/home/jojo/Documents/UNI/term2/image-20220314125248730.png)

### type identification info at run time

![image-20220314125356402](/home/jojo/Documents/UNI/term2/image-20220314125356402.png)

### exception objects and type id

![image-20220314125921251](/home/jojo/Documents/UNI/term2/image-20220314125921251.png)

## new datatypes/ operations 

### endianness

![image-20220314134054829](/home/jojo/Documents/UNI/term2/image-20220314134054829.png)

![image-20220314134117549](/home/jojo/Documents/UNI/term2/image-20220314134117549.png)

![image-20220314134225021](/home/jojo/Documents/UNI/term2/image-20220314134225021.png)

![image-20220314134338743](/home/jojo/Documents/UNI/term2/image-20220314134338743.png)

### Bit Field

![image-20220314134441918](/home/jojo/Documents/UNI/term2/image-20220314134441918.png)

![image-20220314134845112](/home/jojo/Documents/UNI/term2/image-20220314134845112.png)

### unions



![image-20220314135009281](/home/jojo/Documents/UNI/term2/image-20220314135009281.png)

![image-20220314135119296](/home/jojo/Documents/UNI/term2/image-20220314135119296.png)

![image-20220314135146777](/home/jojo/Documents/UNI/term2/image-20220314135146777.png)

![image-20220314135250336](/home/jojo/Documents/UNI/term2/image-20220314135250336.png)

by setting one variable, you change the value of a different value!

### endian-ness part 2 - pointers

![image-20220314135338507](/home/jojo/Documents/UNI/term2/image-20220314135338507.png)

![image-20220314135344761](/home/jojo/Documents/UNI/term2/image-20220314135344761.png)

![image-20220314140148570](/home/jojo/Documents/UNI/term2/image-20220314140148570.png)

![image-20220314140205126](/home/jojo/Documents/UNI/term2/image-20220314140205126.png)

### bitwise operations

![image-20220314141033412](/home/jojo/Documents/UNI/term2/image-20220314141033412.png)

#### shifts

![image-20220314141053206](/home/jojo/Documents/UNI/term2/image-20220314141053206.png)

#### setting  a bit

![image-20220314141110480](/home/jojo/Documents/UNI/term2/image-20220314141110480.png)

### variable number of parameters

![image-20220314141629959](/home/jojo/Documents/UNI/term2/image-20220314141629959.png)

![image-20220314141857613](/home/jojo/Documents/UNI/term2/image-20220314141857613.png)

## File Reading

### standrad streams

![image-20220314142409105](/home/jojo/Documents/UNI/term2/image-20220314142409105.png)

### stream classes

![image-20220314142445456](/home/jojo/Documents/UNI/term2/image-20220314142445456.png)

### opening file 

![image-20220314142611774](/home/jojo/Documents/UNI/term2/image-20220314142611774.png)

### opening and closing 

![image-20220314142633016](/home/jojo/Documents/UNI/term2/image-20220314142633016.png)

### writing

![image-20220314143816576](/home/jojo/Documents/UNI/term2/image-20220314143816576.png)

### reading

![image-20220314143829498](/home/jojo/Documents/UNI/term2/image-20220314143829498.png)

### ignore()

![image-20220314143841565](/home/jojo/Documents/UNI/term2/image-20220314143841565.png)

### stream state flags

![image-20220314143855831](/home/jojo/Documents/UNI/term2/image-20220314143855831.png)

### writing to a stream

![image-20220314143956081](/home/jojo/Documents/UNI/term2/image-20220314143956081.png)

### reading from a stream

![image-20220314144013097](/home/jojo/Documents/UNI/term2/image-20220314144013097.png)

![image-20220314144101945](/home/jojo/Documents/UNI/term2/image-20220314144101945.png)

![image-20220314144112891](/home/jojo/Documents/UNI/term2/image-20220314144112891.png)

### sstream

![image-20220314144123350](/home/jojo/Documents/UNI/term2/image-20220314144123350.png)

### reading from a stream

![image-20220314144137658](/home/jojo/Documents/UNI/term2/image-20220314144137658.png)

### overloading the insertion operator

![image-20220314144235587](/home/jojo/Documents/UNI/term2/image-20220314144235587.png)

### exceptions

![image-20220314144246067](/home/jojo/Documents/UNI/term2/image-20220314144246067.png)

### stream state flags

![image-20220314144258810](/home/jojo/Documents/UNI/term2/image-20220314144258810.png)
