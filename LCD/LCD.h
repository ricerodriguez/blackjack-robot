//##############################################################################
//    filename:        LCD.h
//##############################################################################
//    header file LCD library for HD44780, HD47780, ST7036 ...
//##############################################################################
//
//      Author:            	V.SchK
//      Company:        	HS-Ulm
//
//      Revision:        	1.0
// 	Date:         		June. 2012
//     	Assembled using		C18 3.41+
//
//   	todo	- add comments ;-)
//             	-
//
//##############################################################################
#ifndef _LCD_H
#define _LCD_H 

#include "lcd_config.h" // pin and power configuration file

#ifdef __18CXX      // MPLAB C18 compiler
  #define const const rom
#endif

union LCDv8bit {
    char all;
    struct {
        unsigned LN : 4;
        unsigned HN : 4;
    };
    struct {
        unsigned bit0 : 1;
        unsigned bit1 : 1;
        unsigned bit2 : 1;
        unsigned bit3 : 1;
        unsigned bit4 : 1;
        unsigned bit5 : 1;
        unsigned bit6 : 1;
        unsigned bit7 : 1;
    };
};

#define LCD_RD      1   // read/write select
#define LCD_WR      0
#define LCD_CMD     0   // register selct
#define LCD_DATA    1

#define LCD_BUSY    1   // busy flag logic

#define LCD_ENABLE()    LCD_E = 1;
#define LCD_DISABLE()   LCD_E = 0;
#define LCD_STROBE()    LCD_E = 1; LCD_DELAY_1US(); LCD_E = 0;


    
#define LINE_OFFSET 0x80  // offset for second line if a 2 line display
#define ROW_0 0x00
#define ROW_1 0x40 
#define ROW_2 0x14
#define ROW_3 0x54     
 
void LCD_Init(void);
#define LCD_Clear() LCD_Command(CLEAR_DISPLAY);
void LCD_Write_Nibble(unsigned char value);
void LCD_Write(unsigned char value);
#define LCD_Command    while(LCD_Busy()){;} LCD_RS = LCD_CMD; LCD_Write
#define LCD_Data       while(LCD_Busy()){;} LCD_RS = LCD_DATA; LCD_Write

#define LCD_CharOut             LCD_Data
#define LCD_SetCursor(r,c)      LCD_Command(CURSOR_ADDR + (LINE_OFFSET * r) + c)

void LCD_TextOut(unsigned char row, unsigned char col, unsigned char *text);
void LCD_ConstTextOut(unsigned char row, unsigned char col, const char *text);

#define LCD_ValueOut(a,b,c) LCD_ValueOut_00(a,b,c,1)
void LCD_ValueOut_00(unsigned char row, unsigned char col, short value,
                     unsigned char min_dig);

//unsigned char LCD_Read(void);
unsigned char LCD_Busy(void);
void LCD_signalsTest(void);

// Instruction Set defines (HD44780 compatible)
//                              RS  R/W |   D7  D6  D5  D4  D3  D2  D1  D0
// Clear display                0   0   |   0   0   0   0   0   0   0   1
    #define CLEAR_DISPLAY       0x01
// Return home                  0   0   |   0   0   0   0   0   0   1   -
    #define RETURN_HOME         0x02
// Entry mode set               0   0   |   0   0   0   0   0   1   I/D S
    #define ENTRY_MODE          0x04
    #define CURSOR_INC          0x02
    #define CURSOR_DEC          0x00
    #define DSHIFT_ON           0x01
    #define DSHIFT_OFF          0x00
// Display ctrl                 0   0   |   0   0   0   0   1   D   C   B
    #define DISPLAY_CTRL        0x08
    #define DISPLAY_ON          0x04
    #define DISPLAY_OFF         0x00
    #define CURSOR_ON           0x02
    #define CURSOR_OFF          0x00
    #define BLINK_ON            0x01
    #define BLINK_OFF           0x00
// Cursor / Display shift       0   0   |   0   0   0   1   S/C R/L -   -
    #define DISPLAY_SHIFT_R     0x1C
    #define DISPLAY_SHIFT_L     0x18
    #define CURSOR_MOVE_R       0x14
    #define CURSOR_MOVE_L       0x14

//                              RS  R/W |   D7  D6  D5  D4  D3  D2  D1  D0
// Function Set                 0   0   |   0   0   1   DL  N   F   *   *
//      DL: 1 = 8-Bit   / 0 = 4-Bit interface
//      N:  1 = 2 lines / 0 = 1 line
//      F:  1 = 5x11    / 0 = 5x8 dots  (double hight bit in extended mode !!!)
    #define LCD_RESET           0x30
    #define FOUR_BIT            0x20  // 4-bit Interface
    #define EIGHT_BIT           0x30  // 8-bit Interface not used !!!
    #define FOUR_BIT_ONE_LINE   0x20
    #define FOUR_BIT_TWO_LINE   0x28
//******************************************************************************
// Extended Function Set        0   0   |   0   0   1   DL  N   F   IT1 IT0
//******************************************************************************
    #define EXT_INSTR_TBL_0     0x00
    #define EXT_INSTR_TBL_1     0x01
    #define EXT_INSTR_TBL_2     0x02
// Bias Set                     0   0   |   0   0   0   1   BS  1   0   FX
    #define EXT1_BIAS_1_4       0x1C
    #define EXT1_BIAS_1_5       0x14
// ICON address                 0   0   |   0   1   0   0   a   a   a   a
    #define EXT1_ICON_ADDR      0x40
// Power/ICON Cntrl/Contrast    0   0   |   0   1   0   1   Ion Bon C5  C4
    #define EXT1_BOOST_ICON_C   0x50
    #define ICON_ON             0x08
    #define BOOST_ON            0x04
    #define BOOST_OFF           0
// Follower Ctrl                0   0   |   0   1   1   0   Fon R_2 R_1 R_0
    #define EXT1_FOLLOWER       0x60
    #define FOLLOWER_ON         0x08
    #define FOLLOWER_OFF        0
// Contrast                     0   0   |   0   1   1   1   C3  C2  C1  C0
    #define EXT1_CONTRAST       0x70

// Double height Position       0   0   |   0   0   0   1   UD  -   -   -
    #define EXT2_DHP_TOP        0x18
    #define EXT2_DHP_BOT        0x10
//******************************************************************************

// Set CGRAM address            0   0   |   0   1   a   a   a   a   a   a
    #define CGRAM_ADDR          0x40
// Set DDRAM address            0   0   |   1   a   a   a   a   a   a   a
    #define CURSOR_ADDR         0x80

// Read busy flag (and address) 0   1   |   BF  a   a   a   a   a   a   a

#endif //_LCD_LIB_BUSY_H
