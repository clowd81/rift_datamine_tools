.586              ;Target processor.  Use instructions for Pentium class machines
.MODEL FLAT, C    ;Use the flat memory model. Use C calling conventions
.STACK            ;Define a stack segment of 1KB (Not required for this example)
.DATA             ;Create a near data segment.  Local variables are declared after
                  ;this directive (Not required for this example)
.CODE    

EXTERN mmalloc:PROC

; Attributes: bp-based frame

; char __cdecl huffmanBuild(int	a1, DWORD *a2, int a3, int a4, int a5, int a6, signed int a7)
huffmanBuild proc near

var_80=	dword ptr -80h
arg_0= dword ptr  8
arg_4= dword ptr  0Ch
arg_8= dword ptr  10h
arg_C= dword ptr  14h
arg_10=	dword ptr  18h
arg_14=	dword ptr  1Ch
arg_18=	dword ptr  20h

push	ebp
mov	ebp, esp
sub	esp, 80h
push	ebx
mov	ebx, [ebp+arg_4]
push	esi
xor	esi, esi
mov	[ebp+var_80], 1
push	edi
mov	edx, esi

loc_14902D3:
mov	ecx, [ebp+esi*4+var_80]
mov	eax, edx
and	eax, 1
mov	eax, [ebx+eax*4]
mov	edi, [eax+ecx*4]
jmp	short loc_1490317

loc_14902E4:
inc	esi
cmp	esi, [ebp+arg_0]
jnz	short loc_14902F9
cmp	edx, [ebp+arg_18]
jge	loc_149038C
mov	eax, [ebp+arg_8]
mov	[eax+edx*4], edi

loc_14902F9:
add	edx, edx
cmp	esi, 20h
jge	loc_149038C
mov	ecx, [ebx]
mov	eax, edi
neg	eax
mov	[ebp+esi*4+var_80], eax
mov	eax, edi
shl	eax, 2
sub	ecx, eax
mov	edi, [ecx]

loc_1490317:
test	edi, edi
js	short loc_14902E4
cmp	edi, [ebp+arg_14]
jge	short loc_149038C
mov	eax, [ebp+arg_C]
mov	ecx, [ebp+arg_10]
mov	[eax+edi*4], edx
lea	eax, [esi+1]
mov	[ecx+edi*4], eax
cmp	eax, [ebp+arg_0]
jg	short loc_1490378
jnz	short loc_1490343
cmp	edx, [ebp+arg_18]
jge	short loc_149038C
mov	eax, [ebp+arg_8]
mov	[eax+edx*4], edi
jmp	short loc_1490378

loc_1490343:
mov	ecx, [ebp+arg_0]
mov	ebx, edx
sub	ecx, eax
xor	eax, eax
inc	eax
shl	ebx, cl
shl	eax, cl
test	eax, eax
jz	short loc_149036E
lea	ecx, [eax+ebx]
mov	ebx, [ebp+arg_8]
lea	ebx, [ebx+ecx*4]

loc_149035E:
dec	eax
lea	ebx, [ebx-4]
dec	ecx
cmp	ecx, [ebp+arg_18]
jge	short loc_149038C
mov	[ebx], edi
test	eax, eax
jnz	short loc_149035E

loc_149036E:
mov	ebx, [ebp+arg_4]
jmp	short loc_1490378

loc_1490373:
sar	edx, 1
dec	esi
js	short loc_149037D

loc_1490378:
test	dl, 1
jnz	short loc_1490373

loc_149037D:
or	edx, 1
test	esi, esi
jns	loc_14902D3
mov	al, 1
jmp	short loc_149038E

loc_149038C:
xor	al, al

loc_149038E:
pop	edi
pop	esi
pop	ebx
mov	esp, ebp
pop	ebp
retn
huffmanBuild endp



; Attributes: bp-based frame

; struct_v4 *ProcessCDSHeader(struct_v4 *t, int _256, byte *cdsHeader)
ProcessCDSHeader proc near

_t= dword ptr	 8
_256= dword ptr	 0Ch
cdsHeader= dword ptr  10h

push	ebp
mov	ebp, esp
push	ebx
mov	ecx, [ebp+_t]
mov	ebx, [ebp+_256]
xor	edx, edx
push	esi
push	edi
mov	edi, ecx
inc	edx
push	2
pop	ecx
push	4
pop	esi
mov	[edi+24h], dl
mov	[edi+18h], ebx
mov	[edi+20h], ecx
cmp	ebx, esi
jbe	short loc_1427F90

loc_1427F84:
inc	ecx
mov	eax, edx
shl	eax, cl
cmp	eax, ebx
jb	short loc_1427F84
mov	[edi+20h], ecx

loc_1427F90:
inc	dword ptr [edi+20h]
mov	ecx, [edi+20h]
shl	edx, cl
push	20h
pop	eax
sub	eax, ecx
mov	[ebp+_256], edx
mov	[edi+1Ch], eax
xor	ecx, ecx
lea	eax, [edx+ebx*4]
mul	esi
seto	cl
neg	ecx
or	ecx, eax
push	ecx
call	mmalloc
mov	ecx, [ebp+_256]
lea	esi, [edi+8]
mov	[edi], eax
mov	[edi+4], eax
lea	ecx, [eax+ecx*4]
mov	[esi], ecx
mov	eax, [edi+18h]
lea	eax, [ecx+eax*4]
mov	[edi+0Ch], eax
mov	ecx, [edi+18h]
lea	eax, [eax+ecx*4]
mov	[edi+10h], eax
lea	eax, [eax+ecx*4]
mov	[edi+14h], eax
 push	dword ptr [edi+0Ch]
 push	dword ptr [esi]
 push	[ebp+cdsHeader]
 push	ebx
 call	processFreqTable
 push	[ebp+_256]
 push	dword ptr [edi+18h]
 push	dword ptr [edi+10h]
 push	dword ptr [edi+14h]
 push	dword ptr [edi+4]
 push	esi
 push	dword ptr [edi+20h]
 call	huffmanBuild
 mov	[edi+24h], al
mov	eax, 0
pop	edi
pop	esi
pop	ebx
mov	esp, ebp
pop	ebp
ret
ProcessCDSHeader endp





; Attributes: bp-based frame

; int __cdecl processFreqTable(signed int _256,	byte *cdsheader, int a3, int a4)
processFreqTable proc near

var_30=	dword ptr -30h
var_2C=	dword ptr -2Ch
var_28=	dword ptr -28h
var_24=	dword ptr -24h
var_20=	dword ptr -20h
var_1C=	dword ptr -1Ch
var_18=	dword ptr -18h
var_14=	dword ptr -14h
var_10=	dword ptr -10h
var_C= dword ptr -0Ch
var_8= dword ptr -8
var_4= dword ptr -4
_256= dword ptr	 8
cdsheader= dword ptr  0Ch
arg_8= dword ptr  10h
arg_C= dword ptr  14h

push	ebp
mov	ebp, esp
sub	esp, 30h
mov	edx, [ebp+_256]
xor	eax, eax
sar	edx, 1
push	ebx
mov	ebx, [ebp+arg_8]
inc	edx
push	esi
push	edi
mov	edi, [ebp+arg_C]
add	ebx, 0FFFFFFFCh
mov	[ebp+var_28], eax
add	edi, 0FFFFFFFCh
mov	[ebp+var_24], eax
lea	eax, [edx-1]
mov	ecx, eax
mov	[ebp+var_4], edx
mov	[ebp+var_10], edi
mov	[ebp+var_20], eax
cmp	ecx, [ebp+_256]
jge	short loc_A76A47
lea	esi, [edi+4]
mov	edx, ebx
sub	edx, edi
lea	esi, [esi+ecx*4]
mov	edi, [ebp+cdsheader]

loc_A76A30:
mov	[edx+esi], ecx
mov	eax, [edi+ecx*4]
inc	ecx
mov	[esi], eax
lea	esi, [esi+4]
cmp	ecx, [ebp+_256]
jl	short loc_A76A30
mov	edx, [ebp+var_4]
mov	edi, [ebp+var_10]

loc_A76A47:
sub	[ebp+arg_8], ebx
lea	esi, [ebx+ecx*4]
mov	eax, ecx
mov	[ebp+var_C], edi
mov	edi, [ebp+arg_C]
neg	eax
sub	[ebp+var_C], ebx
mov	[ebp+var_14], eax
mov	eax, [ebp+cdsheader]
mov	[ebp+var_2C], esi
lea	eax, [eax+edx*4]
add	eax, 0FFFFFFFCh
sub	edi, ebx
mov	[ebp+var_30], edi
mov	edi, [ebp+var_10]
mov	[ebp+var_1C], eax

loc_A76A74:
cmp	edx, 1
jle	short loc_A76A95
mov	edx, [ebp+var_20]
sub	eax, 4
mov	[ebp+var_1C], eax
mov	[ebp+var_4], edx
lea	eax, [edx-1]
mov	[ebp+var_20], eax
mov	[ebp+var_8], eax
mov	eax, [ebp+var_1C]
mov	eax, [eax]
jmp	short loc_A76AE9

loc_A76A95:
mov	eax, [ebp+var_24]
inc	eax
mov	[ebp+var_24], eax
test	al, 1
jz	short loc_A76AD1
mov	eax, [ebp+var_C]
dec	ecx
mov	edi, [ebp+arg_8]
mov	eax, [eax+esi]
mov	[ebp+_256], eax
mov	eax, [esi]
sub	esi, 4
inc	[ebp+var_14]
mov	[ebp+var_8], eax
mov	eax, [ebx+4]
mov	[edi+esi], eax
mov	edi, [ebp+var_10]
mov	[ebp+var_2C], esi
cmp	ecx, 1
jz	short loc_A76B42
mov	eax, [edi+4]
mov	[ebp+var_28], eax
jmp	short loc_A76AEC

loc_A76AD1:
mov	edx, [ebp+var_30]
mov	eax, [ebx+4]
mov	[edx+esi], eax
mov	eax, [ebp+var_14]
mov	edx, [ebp+var_4]
mov	[ebp+var_8], eax
mov	eax, [edi+4]
add	eax, [ebp+var_28]

loc_A76AE9:
mov	[ebp+_256], eax

loc_A76AEC:
lea	esi, [edx+edx]
mov	[ebp+var_18], edx
cmp	esi, ecx
jg	short loc_A76B28
mov	edx, [ebp+_256]

loc_A76AF9:
jge	short loc_A76B05
mov	eax, [edi+esi*4]
cmp	eax, [edi+esi*4+4]
jle	short loc_A76B05
inc	esi

loc_A76B05:
cmp	edx, [edi+esi*4]
jle	short loc_A76B25
mov	edx, [ebp+var_18]
mov	eax, [ebx+esi*4]
mov	[ebp+var_18], esi
mov	[ebx+edx*4], eax
mov	eax, [edi+esi*4]
add	esi, esi
mov	[edi+edx*4], eax
mov	edx, [ebp+_256]
cmp	esi, ecx
jle	short loc_A76AF9

loc_A76B25:
mov	edx, [ebp+var_4]

loc_A76B28:
mov	esi, [ebp+var_18]
mov	eax, [ebp+var_8]
mov	[ebx+esi*4], eax
mov	eax, [ebp+_256]
mov	[edi+esi*4], eax
mov	esi, [ebp+var_2C]
mov	eax, [ebp+var_1C]
jmp	loc_A76A74

loc_A76B42:
mov	ecx, [ebp+arg_C]
mov	eax, [ebp+var_8]
pop	edi
pop	esi
mov	[ecx+4], eax
pop	ebx
mov	esp, ebp
pop	ebp
retn
processFreqTable endp

end




