#include "msp430g2553.h"
#include "lcdLib.h"


#define TXD BIT2
#define RXD BIT1

char string[] = {"                     "};
char init0[] = {"I1"};
char init1[] = {"I2"};
char init2[] = {"I3"};
char init3[] = {"I4"};
char init4[] = {"I5"};

unsigned int i=0; //Counter
unsigned int max = 0;
int flag = 0;
unsigned int player = 0;
int initflag=0;
int playc = 0;
int hitflag=0;
unsigned int cash [] = {100,100,100,100,100};
unsigned int bet [] = {10,10,10,10,10};
int state = -1;
void idle();
void setBet();
void play();
void send();
void val();
int main(void)
{
   WDTCTL = WDTPW + WDTHOLD; // Stop WDT
   DCOCTL = 0; // Select lowest DCOx and MODx settings
   BCSCTL1 = CALBC1_1MHZ; // Set DCO
   DCOCTL = CALDCO_1MHZ;
   P2DIR |= 0xFF; // All P2.x outputs
   P2OUT &= 0x00; // All P2.x reset
   P1OUT &= 0x00;
  // P1DIR |= ~(BIT3+BIT4+BIT5);
   UCA0CTL1 |= UCSSEL_2; // SMCLK
   UCA0BR0 = 0x08; // 1MHz 115200
   UCA0BR1 = 0x00; // 1MHz 115200
   P1SEL |= RXD + TXD ; // P1.1 = RXD, P1.2=TXD
   P1SEL2 |= RXD + TXD ; // P1.1 = RXD, P1.2=TXD
   UCA0MCTL = UCBRS2 + UCBRS0; // Modulation UCBRSx = 5
   UCA0CTL1 &= ~UCSWRST; // **Initialize USCI state machine**
   UC0IE |= UCA0RXIE; // Enable USCI_A0 RX interrupt
   lcdInit();
   __delay_cycles(500000);
   lcdSetText("Initializing",0,0);
   P1REN = BIT3+BIT4+BIT5;                   // Enable internal pull-up/down resistors
   P1OUT = BIT3 +BIT4+BIT5;                   //Select pull-up mode for P1.3
   P1IE = BIT3+BIT4+BIT5;                       // P1.3 interrupt enabled
   __delay_cycles(500000);
   __bis_SR_register( GIE); //   __bis_SR_register(CPUOFF + GIE);


   while(1){

       if(flag)
       {
           flag=0;
           switch(state){
           case 0:
               playc=0;
               idle();
               break;
           case 3:
               play();

               break;
           case 1:
                   setBet();
               break;
           case 2:
               val();

               break;
           case 4:

               hitflag=0;
               send();

               cash[player]=cash[player]-bet[player];
                 if(playc==1)
                    cash[player]=cash[player]-bet[player];

               break;

           }
       }
}
}



void idle()
{
    lcdClear();
    switch(player){
    case 0:
        lcdSetText(init0,0,0);
        break;
    case 1:
            lcdSetText(init1,0,0);
            break;
    case 2:
            lcdSetText(init2,0,0);
            break;
    case 3:
            lcdSetText(init3,0,0);
            break;
    case 4:
            lcdSetText(init4,0,0);
            break;
    }

    lcdSetText("Bet:",9,0);
    lcdSetInt(bet[player],13,0);
    lcdSetText("Cash:",0,1);
    lcdSetInt(cash[player],5,1);
}
void play()
{
    lcdClear();
    lcdSetText("Select your Move",0,0);
    switch (playc){
    case 0:
        lcdSetText("HIT",0,1);

        break;
    case 1:
        if(hitflag==0)
        lcdSetText("DOUBLE",0,1);
        else
        {
            playc=2;
            flag=1;
        }
        break;
    case 2:
        lcdSetText("STAY",0,1);
        break;
    }
}

void setBet()
{

    lcdClear();
    lcdSetText("Set the bet",0,0);
    lcdSetInt(bet[player],0,1);
}

void val()
{
    if(bet[player] > cash[player])
    {
        lcdClear();
        lcdSetText("Invalid Bet",0,0);
        state=1;
    }
    else
        state++;
    flag=1;

}

void send()
{
    UC0IE |= UCA0TXIE;
    switch(player){
        case 0:
            UCA0TXBUF='0';
            break;
        case 1:
                UCA0TXBUF='1';
                break;
        case 2:
                UCA0TXBUF='2';
                break;
        case 3:
                UCA0TXBUF='3';
                break;
        case 4:
                UCA0TXBUF='4';
                break;
        }

    UC0IE |= UCA0TXIE;
    switch(playc){
    case 0:
        UCA0TXBUF='0';
        break;
    case 1:
            UCA0TXBUF='1';
            break;
    case 2:
            UCA0TXBUF='2';
            break;
    }
   __delay_cycles(500);
    UC0IE|= UCA0TXIE;
    UCA0TXBUF = '\r\n';

    state=0;
    player++;
    if(player>4)
        player=0;
    flag=1;
}

void btnUpState()
{
    switch(state)
    {
    case 3:
        if(playc<2)
            playc = playc+1;
        else
            playc = 0;
        break;
    case 1:
        if(bet[player]<cash[player])
            bet[player]=bet[player]+1;
        break;
    }
    flag=1;
}
void btnDwnState()
{
    switch(state)
    {
    case 3:
        if(playc>0)
            playc = playc-1;
        else
            playc = 2;
        break;
    case 1:
        if(bet[player]>0)
            bet[player]=bet[player]-1;
        break;
    }
    flag=1;
}

void btnSelState()
{

    if((playc==2 | playc == 1)&state==3)
       state=4;
    else if(playc==0 & state==3)
    {

        UC0IE |= UCA0TXIE;
            switch(player){
                case 0:
                    UCA0TXBUF='0';
                    break;
                case 1:
                        UCA0TXBUF='1';
                        break;
                case 2:
                        UCA0TXBUF='2';
                        break;
                case 3:
                        UCA0TXBUF='3';
                        break;
                case 4:
                        UCA0TXBUF='4';
                        break;
                }
        __delay_cycles(500);
        UC0IE |= UCA0TXIE;
        UCA0TXBUF = '0';
        __delay_cycles(500);
        UC0IE |= UCA0TXIE;
        UCA0TXBUF = '\r\n';
        state=3;
        hitflag=1;
    }
    else
        state++;
    flag=1;
}

#pragma vector=USCIAB0TX_VECTOR
__interrupt void USCI0TX_ISR(void)
{
     UC0IE &= ~UCA0TXIE; // Disable USCI_A0 TX interrupt
 }

#pragma vector=USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void)
{
  // P1OUT |= RXLED;
   string[i++] = UCA0RXBUF; // TX next character
    if (UCA0RXBUF == '?' && initflag==0) // 'a' received?
    {
       i = 0;
       initflag=1;
       init0[0]=string[4];
       init0[1]=string[5];
       init1[0]=string[6];
       init1[1]=string[7];
       init2[0]=string[8];
       init2[1]=string[9];
       init3[0]=string[10];
       init3[1]=string[11];
       init4[0]=string[12];
       init4[1]=string[13];
       //UC0IE |= UCA0TXIE; // Enable USCI_A0 TX interrupt

    }
       //UC0IE |= UCA0TXIE;
       //UCA0TXBUF = player+'0' ;
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
