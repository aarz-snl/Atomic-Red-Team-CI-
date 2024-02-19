import json


def convert_to_winlogbeat_json(event_data):
    winlogbeat_json = {
        "@timestamp": event_data.pop("Time Created"),
        "winlog": {
            "event_id": event_data.pop("Event ID"),
            "message": event_data.pop("Message"),
        }
    }
    for key, value in event_data.items():
        winlogbeat_json[key.lower().replace(" ", "_")] = value
    return winlogbeat_json

def read_events_from_file(file_path):
    events = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        event_data = {}
        for line in lines:
            if line.strip():
                parts = line.strip().split(': ', 1)
                if len(parts) == 2:
                    key, value = parts
                    event_data[key] = value
                else:
                    print(f"Skipping line: {line.strip()}")
            else:
                if event_data:
                    events.append(event_data)
                event_data = {}
        if event_data:
            events.append(event_data)
    return events

def main():
    input_file_path = "sysmon_logs.txt"
    output_file_path = "winlogbeat_events.json"

    events = read_events_from_file(input_file_path)

    winlogbeat_events = []
    for event in events:
        winlogbeat_json = convert_to_winlogbeat_json(event)
        winlogbeat_events.append(winlogbeat_json)

    with open(output_file_path, 'w') as file:
        for event in winlogbeat_events:
            file.write(json.dumps(event) + '\n')

    print("Conversion completed. Winlogbeat-formatted JSON saved to:", output_file_path)

if __name__ == "__main__":
    main()
