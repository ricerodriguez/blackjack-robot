
#include <msp430g2553.h>

#include "lcdLib.h"

char name[] = { "Name1"};
char string [] = {"               \r\n"};
char data[] = {'a',0,'b',0};
char player = '0';
int cash[] ={500,500,500,500};
int bet = 0;
int state=0;
int playC=3;
int flag = 1;
int i=0;
int c=0;
int initFlag = 0;
int currentBet =0;
void idle();
void setBet();
void play();


void main(void)

{


     WDTCTL = WDTPW + WDTHOLD;// Stop Watchdog




 P1REN = BIT3+BIT4+BIT5;                   // Enable internal pull-up/down resistors
 P1OUT = BIT3 +BIT4+BIT5;                   //Select pull-up mode for P1.3
 P1IE = BIT3+BIT4+BIT5;                       // P1.3 interrupt enabled

__enable_interrupt();

lcdInit();// Initialize LCD
__delay_cycles(500000);
lcdSetText("hi",0,1);

while(1){

    if(flag)
    {
        flag=0;
        switch(state){
        case 0:
            idle();
            break;
        case 1:
            play();
            break;
        case 2:
            if(playC==3) //if the move selected requires a bet to be set
                setBet();
            else
            {
                state=4;
                flag=1;
            }
            break;
        case 3:
            val();
        case 4:
            send();

        }
    }

}
}



void idle()
{
    lcdClear();
    lcdSetText(name, 0,0);
    lcdSetText("Bet:",9,0);
    lcdSetInt(bet,13,0);
    lcdSetText("Cash:",0,1);
    lcdSetInt(cash[player-'0'],5,1);
}
void play()
{
    lcdClear();
    lcdSetText("Select your Move",0,0);
    switch (playC){
    case 0:
        lcdSetText("Move1",0,1);
        break;
    case 1:
        lcdSetText("Move2",0,1);
        break;
    case 2:
        lcdSetText("Move3",0,1);
        break;
    case 3:
        lcdSetText("Move4",0,1);
        break;
    }
}

void setBet()
{
    lcdClear();
    if(player == '0')
    {
        lcdSetText("Set your Bet",0,0);
        lcdSetInt(bet,0,1);

    }
    else
    {
        lcdSetText("The Current Bet",0,0);
        lcdSetText("is: ",0,0);
        lcdSetInt(currentBet,4,1);
        cash[player-'0']=cash[player-'0']-currentBet;
    }
}

void val()
{
    if(bet < currentBet)
    {
        lcdClear();
        lcdSetText("Invalid Bet",0,0);
        lcdSetText("OK",6,1);
        state=1;
    }
    else
        state++;
    flag=1;

}

void send()
{
    currentBet=bet;
    data[0] = 'a';
    data[1] = playC;
    data[2] = 'b';
    data[3] = currentBet;
    UC0IE |= UCA0TXIE; // Enable USCI_A0 TX interrupt
    state++;
    flag=1;
}

void btnUpState()
{
    switch(state)
    {
    case 1:
        if(playC<3)
            playC = playC+1;
        else
            playC = 0;
        break;
    case 2:
        if(bet<cash)
            bet=bet+1;
        break;
    }
    flag=1;
}
void btnDwnState()
{
    switch(state)
    {
    case 1:
        if(playC>0)
            playC = playC-1;
        else
            playC = 3;
        break;
    case 2:
        if(bet>0)
            bet=bet-1;
        break;
    }
    flag=1;
}

void btnSelState()
{
    if(state<5)
        state++;
    else
        state=0;
    flag=1;
}

#pragma vector=PORT1_VECTOR
__interrupt void port1_ISR(void)
{
  __delay_cycles(250000);
  if(P1IFG&BIT3)
      btnSelState();
  if(P1IFG&BIT4)
      btnDwnState();
  if(P1IFG&BIT5)
      btnUpState();
  P1IFG=0;
}
/*
#pragma vector=USCIAB0TX_VECTOR
__interrupt void USCI0TX_ISR(void)
{

 //  P3OUT |= DE;
    i = 0;
   UCA0TXBUF = data[i++]; // TX next character
   if (i == sizeof data - 1) // TX over?
      UC0IE &= ~UCA0TXIE; // Disable USCI_A0 TX interrupt
   //P1OUT &= ~TXLED;
   //P3OUT &= ~DE;
}

#pragma vector=USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void)
{

    // P1OUT |= RXLED;
    if(initflag == 0)
    {
       name[c][i++] == UCA0RXBUF; //builds a string with the initials and bet amount
       if (UCA0RXBUF == ' ') // starts after creating name
        {
           c+=c;
           i=0;
        }
       if(name[c][i-2]==' ' && UCA0RXBUF == ' ')
           initflag=1;
    }
    else
        player = UCA0RXBUF;
    //P1OUT &= ~RXLED;
}
*/
