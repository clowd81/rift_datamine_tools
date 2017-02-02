.586              ;Target processor.  Use instructions for Pentium class machines
.MODEL FLAT, C    ;Use the flat memory model. Use C calling conventions
.STACK            ;Define a stack segment of 1KB (Not required for this example)
.DATA             ;Create a near data segment.  Local variables are declared after
                  ;this directive (Not required for this example)
.CODE    


; char __thiscall huffmandecode(struct_this *this, byte	*buffer1, int a3, byte *a4, unsigned int size)
huffmandecode	proc near		

index		= dword	ptr -4
_t			= dword ptr  8
buffer1		= dword	ptr  0Ch
unused		= dword	ptr  10h
arg_8		= dword	ptr  14h
ssize		= dword	ptr  18h

		push ebp
		mov	 ebp, esp
		push esi
		mov	 esi, [ebp+_t]
		xor	 eax, eax	
		cmp	 [ebp+ssize], 0	
		mov	 [ebp+index], eax
		mov	 [esi+8], eax
		mov	 eax, [ebp+buffer1]
		mov	 dword ptr [esi+0Ch], 20h
		mov	 [esi+4], eax
		jbe	 loc_10C39B8	

		push	ebx
		push	edi


loc_10C392A:				
		mov	ecx, [esi+0Ch]
		cmp	ecx, 8		
		jb	short loc_10C3951 

		mov	edi, [esi+8]
		mov	edx, [esi+4]


loc_10C3938:				
		sub	ecx, 8		
		mov	[esi+0Ch], ecx
		movzx	eax, byte ptr [edx] 
		shl	eax, cl		
		or	edi, eax	
		inc	edx		
		mov	[esi+8], edi
		mov	[esi+4], edx
		cmp	ecx, 8		
		jnb	short loc_10C3938


loc_10C3951:				
		mov	ebx, [esi]
		mov	edi, [esi+8]
		mov	edx, edi
		mov	ecx, [ebx+1Ch]
		mov	eax, [ebx+4]
		shr	edx, cl		
		mov	edx, [eax+edx*4]
		test	edx, edx	
		js	short loc_10C3974 

		mov	ecx, [ebx+10h]	; Appears to be	a nop?
		mov	ecx, [ecx+edx*4]
		shl	edi, cl		
		mov	[esi+8], edi
		jmp	short loc_10C3997 

; ---------------------------------------------------------------------------

loc_10C3974:				
		mov	ecx, [ebx+20h]
		shl	edi, cl		
		mov	[esi+8], edi


loc_10C397C:				
		mov	ecx, edi
		mov	eax, edx
		shr	ecx, 31		
		add	edi, edi	
		shl	eax, 2	
		mov	ecx, [ebx+ecx*4+8]
		sub	ecx, eax	
		mov	edx, [ecx]
		mov	[esi+8], edi
		test	edx, edx	
		js	short loc_10C397C


loc_10C3997:				
		mov	eax, [ebx+10h]
		mov	ebx, [ebp+index]
		mov	eax, [eax+edx*4]
		add	[esi+0Ch], eax	
		mov	eax, [ebp+arg_8]
		mov	[ebx+eax], dl
		inc	ebx		
		mov	[ebp+index], ebx
		cmp	ebx, [ebp+ssize]	
		jb	loc_10C392A	

		pop	edi
		pop	ebx


loc_10C39B8:				
		mov	al, 1
		pop	esi
		mov	esp, ebp
		pop	ebp
		ret

huffmandecode	endp



END