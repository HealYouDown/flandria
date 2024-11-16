
;Dick's Data Dumper
;(c) 2021 Rich Whitehouse

	include USERDEFS.INC

CART_MODE			equ 0

FONT_VRAM_OFFSET	equ $0000
PAL_CRAM_OFFSET		equ $0000
	
PRINT_VRAM_OFFSET	equ $C204

LINE_CLEAR_SIZE		equ $14 ;in words

COMMAND_TIMEOUT		equ $F000

COMMAND_TRANSFER	equ $1337F4C3 ;followed by another 2 30-bit ints - address and size
COMMAND_POKE32		equ $13370032
COMMAND_POKE16		equ $13370016
COMMAND_POKE08		equ $13370008

CTRL_P0_DATA		equ $A10003
CTRL_P0_RW			equ $A10009
CTRL_P1_DATA		equ $A10005
CTRL_P1_RW			equ $A1000B

	IF CART_MODE=1
	ORG $000000
	ELSE
	ORG $FF0000
	ENDIF

	include USERMAC.INC

	IF CART_MODE=1
	dc.l			StackInitial
	dc.l			UserMain
	
	dc.l			SpinOnInterrupt ;bus error
	dc.l			SpinOnInterrupt ;address error
	dc.l			SpinOnInterrupt ;illegal op
	dc.l			SpinOnInterrupt ;div by 0
	dc.l			SpinOnInterrupt ;chk
	dc.l			SpinOnInterrupt ;trapv
	dc.l			SpinOnInterrupt ;privelege violation
	dc.l			SpinOnInterrupt ;trace
	dc.l			SpinOnInterrupt ;line a
	dc.l			SpinOnInterrupt ;line f
	
	;motorola reserved
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt

	dc.l			SpinOnInterrupt ;spurious
	dc.l			SpinOnInterrupt ;l1
	dc.l			SpinOnInterrupt ;l2
	dc.l			SpinOnInterrupt ;l3
	dc.l			UserHBlank
	dc.l			SpinOnInterrupt ;l5
	dc.l			UserVBlank
	dc.l			SpinOnInterrupt ;l7
	
	;traps
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	
	;motorola reserved
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	dc.l			SpinOnInterrupt
	
CartHeader:
	dc.b			"SEGA GENESIS    "
	dc.b			"(C)DICK 2021.SEP"
	dc.b			"DATA DUMPER TEST"
	dc.b			"                "
	dc.b			"                "
	dc.b			"DATA DUMPER TEST"
	dc.b			"                "
	dc.b			"                "
	dc.b			"GM MK-0000 -00"
	dc.w			$0000 ;checksum
	dc.b			"J               "
	dc.l			$000000 ;rom start
	dc.l			$07FFFF ;rom end
	dc.l			$FF0000 ;ram start
	dc.l			$FFFFFF ;ram end
	dc.b			"                "
	dc.b			"                "
	dc.b			"                "
	dc.b			"                "
	dc.b			"U               "
	ENDIF
	
UserMain:
	IF CART_MODE=1
	
	;can't rely on bios to have done initial cpu setup
	lea		StackInitial,sp
	move.w	#$2000,SR
	
	;clear all of the ram we're using for our initial state, since initial memory isn't copied in as part of the binary as with the scd user bin
	lea		ClearRamStart,a0
	move.w	#((ClearRamEnd-ClearRamStart)+3)/4,d0
	bsr MemClear32

	ELSE
	
	lea		UserVBlank,a1
	jsr SCD_SET_VINT
	
	;we have control of word ram coming in here. pass it back over, we don't need it for anything.
	move.b	#2,SCD_MEMORY_WPROT
	
	ENDIF
	
	;p0 th to write
	move.b	#$40,$A10009

	;p1 th to write
	move.b	#$40,CTRL_P1_RW
	
	;probably only really necessary in cart mode since the bios sets expected states for us
	move.l	#$80048230,VDP_CTRL
	move.l	#$83288407,VDP_CTRL
	move.l	#$855C8700,VDP_CTRL
	move.l	#$8A008B00,VDP_CTRL
	move.l	#$8C818D2F,VDP_CTRL
	move.l	#$8F029011,VDP_CTRL
	move.l	#$91009200,VDP_CTRL
	
	;make sure hscroll is 0
	VRAM_WRITE_PREP $BC00
	move.w	#$0000,VDP_DATA
	move.w	#$0000,VDP_DATA
	;and make sure vscroll is 0
	VSRAM_WRITE_PREP $0000
	move.w	#$0000,VDP_DATA
	move.w	#$0000,VDP_DATA
	
	;and the bit the bios hasn't done for us, enable vint
	move.w	#$8164,VDP_CTRL

	bsr WaitForVBlank

	IF CART_MODE=1
	;in cart mode, we don't already have the bios font in vram, so load it up along with a palette
	lea		FontData,a0
	move.w	#$800,d0
	VRAM_WRITE_PREP FONT_VRAM_OFFSET
	bsr CopyToVdp
	lea		PalData,a0
	move.w	#$40,d0
	CRAM_WRITE_PREP PAL_CRAM_OFFSET
	bsr CopyToVdp
	ENDIF
	
	CLEAR_LINE_AND_PRINT TitleMessage,2,2
	CLEAR_LINE_AND_PRINT StatusWaiting,2,4
	
@mainLoop:
	bsr WaitForVBlank
	bsr ReadPorts
	
	;display port 1 pins
	move.b	LastReadHigh1,d0
	bsr PinsToString
	CLEAR_LINE_AND_PRINT StringBuffer,2,10

	;move.b	LastReadLow1,d0
	;bsr PinsToString
	;CLEAR_LINE_AND_PRINT StringBuffer,2,11
	
	bra @mainLoop


	;32 bits in d2, 8 bits in d1
ReadPort40:
	bsr ReadPort30
	move.l	d1,-(sp)

	move.w	#0,d3
	bsr ReadPortMultipleOf10
	move.l	d1,d3

	move.l	(sp)+,d2
	lsl.l	#2,d2
	andi.l	#3,d3
	or.l	d3,d2

	lsr.l	#2,d1

	rts


	;read 30 bits, expecting to start with tr on
	;upon exit, d1 will contain the command data
ReadPort30:
	move.w	#2,d3
	;just fall through
	
ReadPortMultipleOf10:
	moveq	#0,d1
@readAnother10:
	move.w	#COMMAND_TIMEOUT,d2

	;set th to 0
	move.b	#$0,CTRL_P1_DATA
	;wait for tr to switch off
@waitLoop0:
	move.b	CTRL_P1_DATA,d0
	btst	#5,d0
	dbeq d2,@waitLoop0
	bne @timeout
	andi.b	#$1F,d0
	lsl.l	#5,d1
	or.b	d0,d1
	
	;set th to 1
	move.b	#$40,CTRL_P1_DATA
	;wait for tr to switch on
@waitLoop1:
	move.b	CTRL_P1_DATA,d0
	btst	#5,d0
	dbne d2,@waitLoop1
	beq @timeout
	andi.b	#$1F,d0
	lsl.l	#5,d1
	or.b	d0,d1
	
	dbra d3,@readAnother10

	bra @exit
@timeout:
	move.l	#$81980085,d1
@exit:
	rts


DATA_TRANSFER macro
	lsr.w	#1,d0
	scs.b	d3
	andi.b	#$10,d3
	move.b	\1,d4
	lsr.l	#4,\1
	andi.b	#$0F,d4
	or.b	d4,d3
	move.b	d3,CTRL_P1_DATA
@waitForTrBitT\@:
	btst.b	#5,CTRL_P1_DATA
	dbne d5,@waitForTrBitT\@
	beq @transferTimeout
	endm
	
DATA_TRANSFER_ALT macro
	lsr.w	#1,d0
	scs.b	d3
	andi.b	#$10,d3
	move.b	\1,d4
	lsr.l	#4,\1
	andi.b	#$0F,d4
	or.b	d4,d3
	ori.b	#$40,d3
	move.b	d3,CTRL_P1_DATA
@waitForTrBitT\@:
	btst.b	#5,CTRL_P1_DATA
	dbeq d5,@waitForTrBitT\@
	bne @transferTimeout
	endm
	
DataTransfer:
	CLEAR_LINE_AND_PRINT StatusInTransfer,2,4
	move.l	TransferAddress,d0
	bsr D0ToString
	PRINT_XY StringBuffer,21,4
	move.l	TransferSize,d0
	bsr D0ToString
	PRINT_XY StringBuffer,30,4
	
	;only tr is read now, used for receive ack
	move.b	#$5F,CTRL_P1_RW
	move.b	#$40,CTRL_P1_DATA

	;wait a while for the other side to change pin states
	move.w	#15,d0
	bsr WaitFrames

	;wait for the other side to set tr to 0
	move.w	#COMMAND_TIMEOUT,d5
@waitForTrBit:
	btst.b	#5,CTRL_P1_DATA
	dbeq d5,@waitForTrBit
	bne @transferTimeout
	
	move.l	TransferAddress,a0
	move.l	a0,a1
	add.l	TransferSize,a1
	
@transferLoop:
	moveq	#0,d0

	move.l	(a0)+,d1
	add.l	d1,d0
	move.l	(a0)+,d2
	add.l	d2,d0

	;we're packing the checksum for these 8 bytes into the tl bits
	move.l	d0,d3
	swap	d3
	add.w	d3,d0
	
	move.w	#COMMAND_TIMEOUT,d5
	DATA_TRANSFER d1
	DATA_TRANSFER_ALT d1
	DATA_TRANSFER d1
	DATA_TRANSFER_ALT d1
	DATA_TRANSFER d1
	DATA_TRANSFER_ALT d1
	DATA_TRANSFER d1
	DATA_TRANSFER_ALT d1

	move.w	#COMMAND_TIMEOUT,d5
	DATA_TRANSFER d2
	DATA_TRANSFER_ALT d2
	DATA_TRANSFER d2
	DATA_TRANSFER_ALT d2
	DATA_TRANSFER d2
	DATA_TRANSFER_ALT d2
	DATA_TRANSFER d2
	DATA_TRANSFER_ALT d2

	cmp.l	a0,a1
	bne @transferLoop

	bsr WaitForVBlank
	CLEAR_LINE_AND_PRINT StatusTransferComplete,2,4
	bra @transferCleanup

@transferTimeout:
	bsr WaitForVBlank
	CLEAR_LINE_AND_PRINT StatusTransferTimeout,2,4
	
@transferCleanup:
	;transfer finished, back to normal read mode
	move.b	#$40,CTRL_P1_RW
	
	move.w	#15,d0
	bsr WaitFrames

	rts


UserVBlank:
	st.b	VBlankFlag
	rte


UserHBlank:
	rts


WaitForVBlank:
	clr.b	VBlankFlag
@stillWaiting:
	tst.b	VBlankFlag
	beq		@stillWaiting
	rts

	
	;d0.w=number of frames to wait
WaitFrames:
	bra @enterWaitLoop
@moreToWait:
	bsr WaitForVBlank
@enterWaitLoop:
	dbra d0,@moreToWait
	rts


DirectPrint:
	lea		VDP_DATA,a1
	moveq	#0,d0
@nextChar:
	move.b	(a0)+,d0
	beq @exit
	move.w	d0,(a1)
	bra @nextChar
	
@exit:
	rts
	
	;expects destination already written to VDP_CTRL
	;d0.w=number of words to copy
	;a0=source data
CopyToVdp:
	lea		VDP_DATA,a1	
	bra @enterCopyLoop
@moreToCopy:
	move.w	(a0)+,(a1)
@enterCopyLoop:
	dbra d0,@moreToCopy
	rts


	;a0=start of memory to clear
	;d0=number of dwords to clear
MemClear32
	bra @enterClearLoop
@moreToClear:
	move.l	#0,(a0)+
@enterClearLoop:
	dbra d0,@moreToClear
	rts
	
	
	;d0.w=number of dwords to clear
VramClear:
	lea		VDP_DATA,a1	
	bra @enterClearLoop
@moreToClear:
	move.l	#0,(a1)
@enterClearLoop:
	dbra d0,@moreToClear
	rts


ReadPorts:
	IF CART_MODE=0 ;z80 isn't running in cart mode
	move.w	#$100,$A11100
@waitForBusRequest:
	btst	#0,$A11100
	bne @waitForBusRequest
	ENDIF

	READ_CONTROLLER 0
	;in this case, port 1 shouldn't be a controller, it should be our arduino connection
	;READ_CONTROLLER 1
	move.b	#$40,CTRL_P1_DATA
	;no delay, we're just hammering the port with th set to see when someone says hi on the other side
	move.b	CTRL_P1_DATA,d0
	move.b	d0,LastReadHigh1
	andi.b	#$3F,d0
	cmp.b	#$2A,d0 ;somewhat arbitrary, but important that tr is off
	bne @noCommand
	
	move.b	#$0,CTRL_P1_DATA ;ack
	CLEAR_LINE_AND_PRINT StatusGotCommand,2,4
	
	;got a command, let's parse it
	bsr ReadPort30
	
	cmpi.l	#COMMAND_TRANSFER,d1
	beq @transferCommand
	
	cmpi.l	#COMMAND_POKE32,d1
	beq @poke32Command

	cmpi.l	#COMMAND_POKE16,d1
	beq @poke16Command

	cmpi.l	#COMMAND_POKE08,d1
	beq @poke08Command
	
	move.l	d1,d0
	bsr D0ToString
	bsr WaitForVBlank
	CLEAR_LINE_AND_PRINT StatusBadCommand,2,4
	PRINT_XY StringBuffer,20,4
	move.w	#60,d0
	bsr WaitFrames
	bra @noCommand

@poke08Command
	CLEAR_LINE_AND_PRINT StatusPokeCommand,2,4
	bsr ReadPort40
	move.l	d2,d3
	move.l	d1,d4
	
	bsr DisplayPokes
	
	move.l	d3,a0
	move.b	d4,(a0)
	
	bra @noCommand

	;could pack these pokes a bit more efficiently, but it's not too important since these are just one-off commands
@poke16Command
	CLEAR_LINE_AND_PRINT StatusPokeCommand,2,4
	bsr ReadPort40
	move.l	d2,-(sp)
	bsr ReadPort30
	move.l	d1,d4
	move.l	(sp)+,d3
	
	bsr DisplayPokes
	
	move.l	d3,a0
	move.w	d4,(a0)
	
	bra @noCommand

@poke32Command
	CLEAR_LINE_AND_PRINT StatusPokeCommand,2,4
	bsr ReadPort40
	move.l	d2,-(sp)
	bsr ReadPort40
	move.l	d2,d4
	move.l	(sp)+,d3
	
	bsr DisplayPokes
	
	move.l	d3,a0
	move.l	d4,(a0)
	
	bra @noCommand
	
@transferCommand:
	CLEAR_LINE_AND_PRINT StatusGotTransfer,2,4
	bsr ReadPort30
	lsl.l	#2,d1
	move.l	d1,TransferAddress
	bsr ReadPort30
	;align transfer size
	addi.l	#$3F,d1
	andi.l	#$FFFFFFC0,d1
	move.l	d1,TransferSize
	
	bsr WaitForVBlank
	
	bsr DataTransfer
	
@noCommand:
	IF CART_MODE=0
	move.w	#0,$A11100
	ENDIF

	rts

	
DisplayPokes:
	move.l	d3,d0
	bsr D0ToString
	PRINT_XY StringBuffer,21,4
	move.l	d4,d0
	bsr D0ToString
	PRINT_XY StringBuffer,30,4
	rts


	;d0=pin bits
PinsToString:
	lea		StringBuffer,a0
	lea		PinLabels,a1

	move.w	#6,d1
	
@pinLoop:
	lsr.b	#1,d0
	bcc @noPin
	move.w	(a1)+,(a0)+
	dbra d1,@pinLoop
	bra @terminateString
@noPin:	
	move.w	#"  ",(a0)+
	lea		2(a1),a1
	dbra d1,@pinLoop

@terminateString
	move.b	#0,(a0)
	
	rts


GET_CHAR_BITS macro
	move.b	d0,d1
	andi.b	#$0F,d1
	cmpi.b	#$0A,d1
	blt.b	@noHexAdjust\@
	addi.b	#7,d1
@noHexAdjust\@:
	addi.b	#"0",d1
	move.b	d1,\1(a0)
	lsr.l	#4,d0
	endm
	
D0ToString:
	lea		StringBuffer,a0
	GET_CHAR_BITS 7
	GET_CHAR_BITS 6
	GET_CHAR_BITS 5
	GET_CHAR_BITS 4
	GET_CHAR_BITS 3
	GET_CHAR_BITS 2
	GET_CHAR_BITS 1
	GET_CHAR_BITS 0
	move.b	#0,8(a0)
	rts


	;d0=color
SetScreenDebugColor:
	CRAM_WRITE_PREP 0
	move.w	d0,VDP_DATA
	rts


SpinOnInterrupt:
	move.w	#$000E,d0
	bsr SetScreenDebugColor
@poopBackAndForthForever:
	bra @poopBackAndForthForever
	

	;data
TitleMessage:				dc.b "Dick's Data Dumper v1.0",0
StatusWaiting:				dc.b "Waiting for connection",0
StatusGotCommand:			dc.b "Command received",0
StatusGotTransfer:			dc.b "Beginning transfer",0
StatusInTransfer:			dc.b "Transferring data:",0
StatusTransferComplete:		dc.b "Transfer complete",0
StatusTransferTimeout:		dc.b "Transfer timed out",0
StatusPokeCommand:			dc.b "Poke command:",0
StatusBadCommand:			dc.b "Invalid command:",0

	EVEN
PinLabels:					dc.b "D0D1D2D3TLTRTH"

	EVEN
FontData:
	incbin CR_FONT.BIN
PalData:
	incbin CR_PAL.BIN

	IF CART_MODE=1
	ORG $FF0000
ClearRamStart:
	ENDIF
	
	EVEN
LastInput0:					ds.b 1
LastInput1:					ds.b 1
InputDelta0:				ds.b 1
InputDelta1:				ds.b 1
LastReadHigh0:				ds.b 1
LastReadHigh1:				ds.b 1
LastReadLow0:				ds.b 1
LastReadLow1:				ds.b 1
VBlankFlag:					ds.b 1
	EVEN
TransferAddress:			ds.l 1
TransferSize:				ds.l 1
StringBuffer:				ds.b 64
	IF CART_MODE=1

	EVEN
ClearRamEnd:
	ds.l					1

StackSpace:
	ds.b					256
StackInitial:
	ds.l					1
	
	ENDIF
