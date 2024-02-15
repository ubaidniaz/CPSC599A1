import serial
import mido
from mido import Message

# Adjust these to match your setup
serial_port = 'COM7'  # Serial port Arduino is connected to (e.g., COM7 on Windows)
midi_port_name = 'Microsoft GS Wavetable Synth 1'  # Name of your MIDI output port

# Initialize the serial connection
ser = serial.Serial(serial_port, 9600)

# Function to open the MIDI output port
def open_midi_output():
    try:
        outport = mido.open_output(midi_port_name)
        print(f"MIDI port '{midi_port_name}' opened successfully.")
        return outport
    except IOError as e:
        print(f"Could not open MIDI output port: {midi_port_name}. Error: {e}")
        return None

# Function to process and play notes and modulation from serial data
def process_serial_data(outport):
    last_note_played = None
    last_volume_val = -1  # Initialize with an impossible value to ensure the first read is processed

    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            note_val, button_state, volume_val = parse_serial_data(data)

            # Update volume for every read, ensuring it's always current
            if volume_val != last_volume_val:
                outport.send(Message('control_change', channel=0, control=7, value=volume_val))
                last_volume_val = volume_val

            # Play or stop the note based on button state
            if button_state == 1 and note_val != last_note_played:  # Button pressed, new note
                if last_note_played is not None:
                    outport.send(Message('note_off', note=last_note_played, velocity=64))
                outport.send(Message('note_on', note=note_val, velocity=64))
                last_note_played = note_val
            elif button_state == 0 and last_note_played is not None:  # Button released, stop note
                outport.send(Message('note_off', note=last_note_played, velocity=64))
                last_note_played = None



def parse_serial_data(data):
    """Extracts note, button state, and modulation value from the serial data."""
    try:
        # Find indices for 'N', 'B', and 'M' to accurately extract parts
        n_index = data.index('N') + 1
        b_index = data.index('B')
        m_index = data.index('M') + 1

        note_val = int(data[n_index:b_index])  # Extract note value between 'N' and 'B'
        button_state = int(data[b_index + 1:m_index - 1])  # Extract button state between 'B' and 'M'
        mod_val = int(data[m_index:])  # Extract modulation value after 'M'

        return note_val, button_state, mod_val
    except ValueError as e:
        print(f"Error parsing data: {data} with error: {e}")
        return 0, 0, 0  # Return default values in case of parsing error
    except Exception as e:
        print(f"Unexpected error parsing data: {data} with error: {e}")
        return 0, 0, 0  # Handle any unexpected errors gracefully


# Main function to setup and run our MIDI controller
def main():
    outport = open_midi_output()
    if outport:
        process_serial_data(outport)
    else:
        print("Failed to open MIDI port. Exiting...")

if __name__ == "__main__":
    main()
