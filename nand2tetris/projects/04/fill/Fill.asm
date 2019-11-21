// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


(LOOP)
    @SCREEN
    D=A
    @aux
    M=D 

    (KEYBOARD)
        @KBD
        D=M

        @PRINTBLACK
        D;JGT          
        @PRINTWHITE
        D;JEQ  

        (PRINTBLACK)
            @aux2
            M=-1
            @FLIPCOLOR
            0;JMP
        (PRINTWHITE)
            @aux2
            M=0
            @FLIPCOLOR
            0;JMP

        (FLIPCOLOR)
            @aux2 
            D=M 

            @aux
            A=M 
            M=D 

            @aux
            D=M+1 
            @KBD
            D=A-D 

            @aux
            M=M+1
            A=M

            @FLIPCOLOR
            D;JGT

        @LOOP
        0;JMP
