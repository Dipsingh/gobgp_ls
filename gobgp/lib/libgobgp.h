/* Created by "go tool cgo" - DO NOT EDIT. */

/* package command-line-arguments */

/* Start of preamble from import "C" comments.  */


#line 18 "/Users/dipsingh/GOlangProjects/src/github.com/dipsingh/gobgp/gobgp/lib/path.go"
 typedef struct {
     char *value;
     int len;
 } buf;

 typedef struct path_t {
     buf   nlri;
     buf** path_attributes;
     int   path_attributes_len;
     int   path_attributes_cap;
 } path;
 extern path* new_path();
 extern void free_path(path*);
 extern int append_path_attribute(path*, int, char*);
 extern buf* get_path_attribute(path*, int);



/* End of preamble from import "C" comments.  */


/* Start of boilerplate cgo prologue.  */

#ifndef GO_CGO_PROLOGUE_H
#define GO_CGO_PROLOGUE_H

typedef signed char GoInt8;
typedef unsigned char GoUint8;
typedef short GoInt16;
typedef unsigned short GoUint16;
typedef int GoInt32;
typedef unsigned int GoUint32;
typedef long long GoInt64;
typedef unsigned long long GoUint64;
typedef GoInt64 GoInt;
typedef GoUint64 GoUint;
typedef __SIZE_TYPE__ GoUintptr;
typedef float GoFloat32;
typedef double GoFloat64;
typedef float _Complex GoComplex64;
typedef double _Complex GoComplex128;

/*
  static assertion to make sure the file is being used on architecture
  at least with matching size of GoInt.
*/
typedef char _check_for_64_bit_pointer_matching_GoInt[sizeof(void*)==64/8 ? 1:-1];

typedef struct { const char *p; GoInt n; } GoString;
typedef void *GoMap;
typedef void *GoChan;
typedef struct { void *t; void *v; } GoInterface;
typedef struct { void *data; GoInt len; GoInt cap; } GoSlice;

#endif

/* End of boilerplate cgo prologue.  */

#ifdef __cplusplus
extern "C" {
#endif


extern int get_route_family(char* p0);

extern path* serialize_path(int p0, char* p1);

extern char* decode_path(path* p0);

extern char* decode_capabilities(buf* p0);

#ifdef __cplusplus
}
#endif
