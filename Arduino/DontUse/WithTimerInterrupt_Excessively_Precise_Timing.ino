/**
 * This program is the Telemtry Synchronization Code for the 2014 AUVSI
 * competition.
 * 
 * 
 */
 
/*==========================================================================================
   ARDUINO UNO PINS
*/

#define _OBCSerial      Serial  // OBC Tx/Rx Interface
#define LED             13      // LED Pin
#define	SHOOT_PIN       13      // Trigger Pin


/*==========================================================================================
   SETTINGS
*/

#define SHOOT_PERIOD    1       // Shooting Period (in seconds)

#define INTERRUPT_TIMER_HALF_PERIOD_MILLISECONDS  500

#define FLAGS_SHOOT_BIT (1<<0)


/*==========================================================================================
   VARIABLES (NOT SETTINGS)
*/

uint8_t flags = 0;

uint8_t ShootPinBitOffset;
#if SHOOT_PIN <= 7
#define PINREGISTERBYTE_WRITE_FOR_SHOOT PORTD
#else
#define PINREGISTERBYTE_WRITE_FOR_SHOOT PORTB
#endif


/*==========================================================================================
  Fast scheduled ISR ("InterruptServiceRoutine") for camera triggering at precise intervals
*/
ISR(TIMER1_COMPA_vect) {
    PINREGISTERBYTE_WRITE_FOR_SHOOT |= (~(1<<ShootPinBitOffset)) & ((flags & FLAGS_SHOOT_BIT) != 0) << ShootPinBitOffset;
    flags ^= FLAGS_SHOOT_BIT; //XOR to swap 1 and 0 every half-period
}


/*==========================================================================================
  DIRECT PORT ACCESS FOR MAXIMUM SPEED DIGITAL I/O
*/

// Direct-port-access equivalent of: pinMode(pin, INPUT); ...also returns the offset of the bit used for that pin
uint8_t SetDirectPortAccessPin_READ(uint8_t pin) {
  if(pin <= 7) {
    DDRD &= (~(1<<pin)); //e.g. if pin is 2, first 4 bits: shift 0001 to 0100, then flip 1011, then &= with DDRD to set pin 2 to 0 i.e. INPUT
    return pin;     //return the offset of the bit we just set
  } else if(pin <= 13) {
    DDRB &= (~(1<<(pin-8))); //same as above, but the 0th bit of DDRB here is really the 8th Arduino pin
    return (pin-8);     //return the offset of the bit we just set
  }
  return 0;
}

// Direct-port-access equivalent of: pinMode(pin, OUTPUT); ...also returns the offset of the bit used for that pin
uint8_t SetDirectPortAccessPin_WRITE(uint8_t pin) {
  if(pin <= 7) {
    DDRD |= (1<<pin); //e.g. if pin is 2, first 4 bits: shift 0001 to 0100, then |= with DDRD to set pin 2 to 1 i.e. OUTPUT
    return pin;     //return the offset of the bit we just set
  } else if(pin <= 13) {
    DDRB |= (1<<(pin-8)); //same as above, but the 0th bit of DDRB here is really the 8th Arduino pin
    return (pin-8);     //return the offset of the bit we just set
  }
  return 0;
}


/*==========================================================================================
   SETUP
*/

void setup()  {
    //_OBCSerial.begin(57600);
    
    //pinMode(LED,OUTPUT);
    //pinMode(SHOOT_PIN, OUTPUT);
    
//------------ Setup Timer Interrupt for precise triggering
    noInterrupts(); //disable interrupts
    
    ShootPinBitOffset = SetDirectPortAccessPin_WRITE(SHOOT_PIN);
    
    //timer0 manages pins 5,6
    //timer1 manages pins 9,10
    //timer2 manages pins 3,11
    
    // Use Timer1 for timer interrupt
    TCCR1A = 0; //clear this entire register
    TCCR1B = 0; //clear this entire register
    
    // compare match register -- what value to trigger timer counter interrupt on
    //    prescalar is 1024x, ATMega328P clock rate is 16 MHz so 16000 cycles happen in 1 millisecond
    OCR1A = (16000*INTERRUPT_TIMER_HALF_PERIOD_MILLISECONDS/1024)-1;
    
    TCCR1B |= (1 << WGM12);   // CTC mode (_Clear _Timer counter TCNT1 on _Compare match TCNT1 == OCR1A)
    TCCR1B |= (1 << CS10) | (1 << CS12);    // 1024x prescaler (see ATMega328P documentation page 137)
    TIMSK1 |= (1 << OCIE1A);  // enable timer compare interrupt
    
    TCNT1  = 0; //initialize timer counter value to 0
    
    interrupts(); //re-enable interrupts
//------------ END Setup Timer Interrupt for precise triggering
}

/*==========================================================================================
   LOOP
*/

void loop()  {
    uint16_t len;
    
    // Check for confirm start trigger
    while(_OBCSerial.available()){
        uint8_t inputChar = (uint8_t)_OBCSerial.read();
        inputString += inputChar;
        if(inputChar == '\n'){	// Require newline message deliminator
            if(inputString.equals("1\n") || inputChar == '1'){	// Message is "1"
                // Initialize trigger IRQ
                triggerTimer.begin(triggerShoot, 500000 * SHOOT_PERIOD);
            }
            if(inputString.equals("0\n") || inputChar == '0'){	// Message is "0"
                triggerTimer.end();	// Disable trigger
            }
            inputString = "";	// Clear message buffer
        }
    }
}

