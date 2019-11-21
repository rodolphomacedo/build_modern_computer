// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// If RAM[0] == 0
@R0
D=M
@STOP
    D;JEQ

// RAM[1] == 0
@R1
D=M
@STOP
    D;JEQ

// Multiplication R0 as base
@R0
D=M-1
@i
M=D

@R2
M=0

(LOOP)
    @R1
    D=M
    @R2
    M=M+D
    
    @i
    D=M
    @END
    D;JEQ
    @i
    M=D-1
    @LOOP
    0;JMP
    
(STOP) 
    @R2
    M=0
    @END
    0;JMP


(END)
    @END
    0;JMP
