import json

def convert_to_winlogbeat_json(event_data):
    try:
        winlogbeat_json = {
            "@timestamp": event_data.pop("UtcTime", ""),
            "winlog": {
                "event_id": event_data.pop("Event ID", ""),
                "message": event_data.pop("Message", ""),
            }
        }
        for key, value in event_data.items():
            winlogbeat_json[key.lower().replace(" ", "_")] = value
        return winlogbeat_json
    except KeyError as e:
        print(f"Key error: {e} in event data: {event_data}")
        return {}

def read_events_from_file(file_path):
    events = []
    with open(file_path, 'r') as file:
        event_data = {}
        for line in file:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                event_data[key.strip()] = value.strip()
            elif event_data:
                events.append(event_data)
                event_data = {}
        if event_data:  # Add the last event
            events.append(event_data)
    return events

def main():
    input_file_path = "sysmon_logs.txt"
    output_file_path = "winlogbeat_events.json"

    events = read_events_from_file(input_file_path)
    winlogbeat_events = [convert_to_winlogbeat_json(event) for event in events]

    with open(output_file_path, 'w') as file:
        json.dump(winlogbeat_events, file, indent=4)

    print(f"Conversion completed. Winlogbeat-formatted JSON saved to: {output_file_path}")

if __name__ == "__main__":
    main()
