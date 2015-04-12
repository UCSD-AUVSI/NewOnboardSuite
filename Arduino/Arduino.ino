/*==========================================================================================
   Arduino code for camera triggering, gimbal angle reading, and gimbal settings
   For UCSD AUVSI 2015 Competition
   
   The arduino waits for the string "1\n" which causes it to start timed camera triggering.
   
   When triggering it will continuously shoot images at 1 Hz until it receives a stop message
   "0\n" over serial from the OBC.
   
   Immediately after the digitalWrite(HIGH) to trigger image capture, it sends a serial string
   back to the OBC telling it that it took a picture; this should contain gimbal angles as well.
   The OBC will then match the time it receives these messages with telemetry and images.
   
   todo: use AnalogRead with pins for gimbal controller, convert voltages to angles, and
         send back to OBC when an image is taken
*/
 
/*==========================================================================================
   ARDUINO UNO PINS
*/

#define _OBCSerial      Serial  // USB serial interface to OBC
#define LED             13      // LED Pin
#define	SHOOT_PIN       12      // Trigger Pin


/*==========================================================================================
   SETTINGS
*/

#define INTERRUPT_TIMER_HALF_PERIOD_MILLISECONDS  500

#define FLAG_SHOOT (1<<0)
#define FLAG_TRIGGER_TIMER_STARTED (1<<1)


/*==========================================================================================
   VARIABLES (NOT SETTINGS)
*/

uint8_t flags = 0;


/*==========================================================================================
   SETUP
*/

void setup()  {
    _OBCSerial.begin(19200);
    
    pinMode(LED,OUTPUT);
    pinMode(SHOOT_PIN, OUTPUT);
}

/*==========================================================================================
   CAMERA SHOOT IMAGE
*/

char shootmsg[256];

void triggerShoot() {
    digitalWrite(SHOOT_PIN, flags & FLAG_SHOOT);
    if(flags & FLAG_SHOOT) {
        memset(shootmsg,0,256);
        sprintf(shootmsg, "shot\n"); //todo: if this Arduino is reading gimbal angles, put them in this message
        _OBCSerial.print(shootmsg);
    }
    flags ^= FLAG_SHOOT;
}

/*==========================================================================================
   LOOP
*/
String inputString = "";
int waitloops = 0;

void loop() {
    // Check for confirm start trigger
    while(_OBCSerial.available()) {
        char inputChar = _OBCSerial.read();
        inputString += inputChar;
        if(inputChar == '\n') {	// Require newline message deliminator
            if(inputString.equals("1\n")) {    // Message is "1"
                flags |= FLAG_TRIGGER_TIMER_STARTED; //enable triggering
                String stringReceived="received ";
                _OBCSerial.print(stringReceived+inputString);
                inputString = "";
            }
            if(inputString.equals("0\n")) {    // Message is "0"
                flags &= (~FLAG_TRIGGER_TIMER_STARTED); //disable triggering
                String stringReceived="received ";
                _OBCSerial.print(stringReceived+inputString);
                inputString = "";
            }
        }
    }
    
    waitloops++;
    if(waitloops >= INTERRUPT_TIMER_HALF_PERIOD_MILLISECONDS) {
        if(flags & FLAG_TRIGGER_TIMER_STARTED) {
            triggerShoot();
        }
        waitloops = 0;
    }
    delay(1);
}






