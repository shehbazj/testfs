/* Copyright 2015 Peter Goodman (peter@trailofbits.com), all rights reserved. */

#ifndef FSLICE_H_
#define FSLICE_H_
#include <stddef.h>

#define PRINT_FUNC_VAR	// Prints caller function name and source
				// and destination variable names for
				// bzero, memcpy and strcpy functions 

#ifdef PRINT_FUNC_VAR
#define _bzero(a,b) \
	bzero(a,b); \
	fprintf(stderr, "#%s:"#a"\n", __func__); 

#define _memcpy(a,b,c) \
	memcpy(a,b,c); \
	fprintf(stderr, "#%s:"#a"\n#%s:"#b"\n", __func__ ,__func__); 

#define _strcpy(a,b) \
	strcpy(a,b); \
	fprintf(stderr, "#%s:"#a"\n#%s:"#b"\n",__func__,__func__); 
#else
#define _bzero(a,b) \
	bzero(a,b);

#define _memcpy(a,b,c) \
	memcpy(a,b,c);

#define _strcpy(a,b) \
	strcpy(a,b);
#endif

__attribute__((weak))
extern void __fslice_read_block(void *addr, size_t size, int nr);

#define fslice_read_block(a,s,nr) \
  if (__fslice_read_block) __fslice_read_block(a,s,nr)

__attribute__((weak))
extern void __fslice_write_block(void *addr, size_t size, int nr);

#define fslice_write_block(a,s,nr) \
  if (__fslice_write_block) __fslice_write_block(a,s,nr)

__attribute__((weak))
extern void __fslice_name(void *name, int len);

#define fslice_name(a,n) \
  if (__fslice_name) __fslice_name(a,n)

__attribute__((weak))
extern void __fslice_data(void *content, int len);

#define fslice_data(a,n) \
  if (__fslice_data) __fslice_data(a,n)

__attribute__((weak))
extern void __fslice_clear();

#define fslice_clear() \
  if (__fslice_clear) __fslice_clear()

#endif  // FSLICE_H_
