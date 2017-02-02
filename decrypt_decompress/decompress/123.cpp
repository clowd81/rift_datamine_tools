#include <string>
#include <stdio.h>
#include <iostream>
#include <windows.h>
//#include "funcs.h"
using namespace std;

struct  __declspec(align(1)) struct_v4
{
  BYTE *dword0;
  BYTE *dword4;
  BYTE *dword8;
  BYTE *dwordC;
  BYTE *dword10;
  BYTE *dword14;
  DWORD _256;
  DWORD _23;
  DWORD nine;
  BYTE byte24;
};

struct __declspec(align(4)) struct_this
{
  struct_v4 *lookup;
  BYTE *ptrToNextByte;
  unsigned int byteSoFar;
  DWORD bitCount;
};


extern "C" {
	void* mmalloc(size_t size);
	struct_v4 *	ProcessCDSHeader(struct_v4 *t, int _256, byte *cdsHeader);
	char huffmandecode(struct_this *this_, byte	*buffer1, int a3, byte *a4, unsigned int size);
   }


void processStruct(struct_v4 *t)
{
	byte *frequencyData = (byte*)malloc(1024);
	FILE* handle = fopen("C:\\workspace\\rift_extractor\\cds_freq.dat", "rb");
	fread(frequencyData, 1024, 1, handle);
	fclose(handle);
	ProcessCDSHeader(t, 256, frequencyData);
}

void *allocatedMemory = 0;

void* mmalloc(size_t size)
{
	allocatedMemory = malloc(size);
	return allocatedMemory;
}

BOOL WINAPI DllMain (HINSTANCE hinstDLL, DWORD     fdwReason, LPVOID    lpvReserved)
{
  return TRUE;
}

extern "C"__declspec(dllexport)  void decompressData(byte* frequencyData, byte* dataInput, int compressedSize, byte* dataOutput, int decompressedSize)
{
	struct_v4 t;
	memset(&t, 0, sizeof(t));
	ProcessCDSHeader(&t, 256, frequencyData);

	struct_this _this;
	memset(&_this, 0, sizeof(_this));
	_this.lookup = &t;
	huffmandecode(&_this, dataInput, compressedSize, dataOutput,decompressedSize);

	free(allocatedMemory);
	return;
}

